#!/usr/bin/env python3
"""Score and rank app-idea candidates for the app-idea-hunter skill.

Reads hunt/scores.json (schema in references/scoring.md), applies the hard kill
gates, sums the weighted axes, and prints a ranked scorecard plus a kill list.

Usage:
    python3 scripts/score.py hunt/scores.json
    python3 scripts/score.py hunt/scores.json --json   # machine-readable
"""

import argparse
import json
import sys

MAX = {"pain": 25, "money": 25, "demand": 20, "marketability": 20, "feasibility": 10}
DEAD_TIERS = {"T0", "T1"}
DEAD_TRENDS = {"flat", "declining"}


def gate_failures(c):
    """Return the list of hard gates this candidate fails."""
    failed = []
    tier = (c.get("pmf_tier") or "").upper()

    if tier in DEAD_TIERS:
        failed.append(f"Reddit PMF gate ({tier}: pain not real or not sharp)")
    elif tier not in {"T2", "T3"}:
        failed.append("Reddit PMF gate (not graded - Phase 5 incomplete)")

    if (c.get("money_evidence") or "none").lower() == "none":
        failed.append("No money in the niche (silence is a graveyard)")

    if (c.get("trend") or "").lower() in DEAD_TRENDS:
        failed.append("Trend flat or declining")

    build, budget = c.get("build_days"), c.get("budget_days")
    if isinstance(build, (int, float)) and isinstance(budget, (int, float)) and budget > 0:
        if build > budget * 1.5:
            failed.append(f"Build {build}d exceeds budget {budget}d by >50% (cut scope to revive)")

    if c.get("hazard"):
        failed.append("Store-policy or safety hazard")

    return failed


def total(c):
    """Sum the axes. Returns (score, list_of_missing_axes)."""
    s, missing = 0, []
    for axis, cap in MAX.items():
        v = (c.get("scores") or {}).get(axis)
        if v is None:
            missing.append(axis)
            continue
        if not isinstance(v, (int, float)):
            raise SystemExit(f"'{c.get('name')}': axis '{axis}' must be a number or null, got {v!r}")
        if v < 0 or v > cap:
            raise SystemExit(f"'{c.get('name')}': axis '{axis}' is {v}, must be 0-{cap}")
        s += v
    return s, missing


def verdict(score, missing):
    if missing:
        return "INCOMPLETE"
    if score >= 80:
        return "BUILD"
    if score >= 65:
        return "STRONG - one thin axis"
    if score >= 50:
        return "PARKING LOT"
    return "KILL (score)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args()

    try:
        with open(args.path) as f:
            data = json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"No such file: {args.path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"{args.path} is not valid JSON: {e}")

    cands = data.get("candidates")
    if not cands:
        raise SystemExit("scores.json has no 'candidates' array")

    live, dead = [], []
    for c in cands:
        if not c.get("name"):
            raise SystemExit("every candidate needs a 'name'")
        fails = gate_failures(c)
        score, missing = total(c)
        row = {
            "name": c["name"],
            "pmf_tier": c.get("pmf_tier"),
            "axes": {a: (c.get("scores") or {}).get(a) for a in MAX},
            "total": score,
            "missing_axes": missing,
            "notes": c.get("notes", ""),
        }
        if fails:
            row["gates_failed"] = fails
            dead.append(row)
        else:
            row["verdict"] = verdict(score, missing)
            live.append(row)

    # Observed demand beats inferred demand: T3 outranks T2 inside a 5-point band.
    live.sort(key=lambda r: (r["total"] + (5 if r["pmf_tier"] == "T3" else 0)), reverse=True)

    if args.json:
        json.dump({"survivors": live, "killed": dead}, sys.stdout, indent=2)
        print()
        return

    print(f"\n{len(cands)} scored -> {len(live)} survived, {len(dead)} killed\n")

    if live:
        hdr = f"{'#':<3}{'Idea':<34}{'PMF':<5}{'Pain':>5}{'Money':>7}{'Dem':>6}{'Mkt':>6}{'Feas':>6}{'Total':>7}  Verdict"
        print(hdr)
        print("-" * len(hdr))
        for i, r in enumerate(live, 1):
            a = r["axes"]
            cell = lambda v: "--" if v is None else str(v)
            print(
                f"{i:<3}{r['name'][:33]:<34}{r['pmf_tier'] or '?':<5}"
                f"{cell(a['pain']):>5}{cell(a['money']):>7}{cell(a['demand']):>6}"
                f"{cell(a['marketability']):>6}{cell(a['feasibility']):>6}"
                f"{r['total']:>7}  {r['verdict']}"
            )
            if r["missing_axes"]:
                print(f"   ^ unscored: {', '.join(r['missing_axes'])} - fill these before trusting the rank")
    else:
        print("Nothing survived the gates. That is a finding, not a failure -")
        print("report the kill list and widen the harvest.\n")

    if dead:
        print("\nKilled\n" + "-" * 6)
        for r in dead:
            print(f"  {r['name']}")
            for g in r["gates_failed"]:
                print(f"      x {g}")
    print()


if __name__ == "__main__":
    main()
