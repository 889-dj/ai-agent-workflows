#!/usr/bin/env python3
"""Score and rank app-idea candidates for the app-idea-hunter skill.

Reads hunt/scores.json (schema in references/scoring.md), applies the hard kill
gates, validates that the hand-entered axis scores agree with the structured
evidence fields, sums the axes, and prints a ranked scorecard plus a kill list.

Usage:
    python3 scripts/score.py hunt/scores.json
    python3 scripts/score.py hunt/scores.json --json   # machine-readable
"""

import argparse
import json
import sys

MAX = {"pain": 25, "money": 25, "demand": 20, "marketability": 20, "feasibility": 10}

TIERS = {"T0", "T1", "T2", "T3"}
DEAD_TIERS = {"T0", "T1"}

# money_evidence: how well the "someone is paid here" claim is backed.
#   verified  - attested figures (TrustMRR, marketplace listing with revenue)
#   estimated - incumbents with estimated revenue (Sensor Tower etc.)
#   listed    - incumbents + visible pricing, no revenue data
#   unknown   - data could not be reached (NOT the same as none; never kills)
#   none      - looked properly, nobody is earning (kills)
MONEY = {"verified", "estimated", "listed", "unknown", "none"}

TRENDS = {"rising_both", "rising_one", "spiky", "seasonal", "flat", "declining", "unknown"}
DEAD_TRENDS = {"flat", "declining"}

# Ceiling on the demand axis implied by the trend (12 trend pts + 8 keyword pts).
DEMAND_CAP = {
    "rising_both": 20, "rising_one": 16, "spiky": 13, "seasonal": 13,
    "flat": 8, "declining": 8, "unknown": 20,
}
# Ceiling on the pain axis implied by the PMF tier.
PAIN_CAP = {"T0": 0, "T1": 0, "T2": 18, "T3": 25}


def fail(msg):
    raise SystemExit(f"error: {msg}")


def as_bool(c, key):
    """Accept real booleans and the strings 'true'/'false'; reject anything else."""
    v = c.get(key, False)
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.strip().lower() in {"true", "false"}:
        return v.strip().lower() == "true"
    fail(f"'{c.get('name')}': '{key}' must be true or false, got {v!r}")


def validate(c):
    """Check enums and cross-field consistency. Returns a list of warnings."""
    name = c.get("name")
    warns = []

    tier = (c.get("pmf_tier") or "").upper() or None
    if tier is not None and tier not in TIERS:
        fail(f"'{name}': pmf_tier must be one of {sorted(TIERS)}, got {c.get('pmf_tier')!r}")

    money = c.get("money_evidence")
    if money is None:
        warns.append("money_evidence missing - treated as 'unknown', not 'none'")
    elif str(money).lower() not in MONEY:
        fail(f"'{name}': money_evidence must be one of {sorted(MONEY)}, got {money!r}")

    trend = (c.get("trend") or "unknown").lower()
    if trend not in TRENDS:
        fail(f"'{name}': trend must be one of {sorted(TRENDS)}, got {c.get('trend')!r}")

    scores = c.get("scores") or {}
    for axis, v in scores.items():
        if axis not in MAX:
            fail(f"'{name}': unknown axis '{axis}' (valid: {', '.join(MAX)})")
        if v is None:
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            fail(f"'{name}': axis '{axis}' must be a number or null, got {v!r}")
        if v < 0 or v > MAX[axis]:
            fail(f"'{name}': axis '{axis}' is {v}, must be 0-{MAX[axis]}")

    pain = scores.get("pain")
    if tier and pain is not None and pain > PAIN_CAP[tier]:
        fail(f"'{name}': pain {pain} is above the {PAIN_CAP[tier]} ceiling for tier {tier}")

    demand = scores.get("demand")
    if demand is not None and demand > DEMAND_CAP[trend]:
        fail(f"'{name}': demand {demand} is above the {DEMAND_CAP[trend]} ceiling for trend '{trend}'")

    mkt = scores.get("marketability")
    if "first_video" in c and not as_bool(c, "first_video") and mkt is not None and mkt > 10:
        fail(f"'{name}': marketability {mkt} exceeds 10, but no first-video sentence could be written")

    build, budget = c.get("build_days"), c.get("budget_days")
    if build is None or budget is None:
        warns.append("build_days/budget_days missing - budget gate not checked")

    return warns


def gate_failures(c):
    """Return (hard_failures, overrides). Overrides are gates waived with a reason."""
    failed, overrides = [], []
    tier = (c.get("pmf_tier") or "").upper()
    money = (c.get("money_evidence") or "unknown").lower()
    trend = (c.get("trend") or "unknown").lower()

    if tier in DEAD_TIERS:
        failed.append(f"Reddit PMF gate ({tier}: pain not real or not sharp)")
    elif tier not in {"T2", "T3"}:
        failed.append("Reddit PMF gate (not graded - Phase 5 incomplete)")

    if money == "none":
        if tier == "T3":
            overrides.append(
                "Money gate waived: T3 shows people already paying/hacking, but no "
                "incumbent revenue was found - verify before building"
            )
        else:
            failed.append("No money in the niche (silence is a graveyard)")

    if trend in DEAD_TRENDS:
        failed.append("Trend flat or declining")

    build, budget = c.get("build_days"), c.get("budget_days")
    if isinstance(build, (int, float)) and isinstance(budget, (int, float)) and budget > 0:
        if build > budget * 1.5:
            failed.append(f"Build {build}d exceeds budget {budget}d by >50% (cut scope to revive)")

    if as_bool(c, "hazard"):
        failed.append("Store-policy or safety hazard")

    return failed, overrides


def total(c):
    """Sum the axes. Returns (score, list_of_missing_axes)."""
    scores = dict(c.get("scores") or {})
    # A one-giant category is a harder market for a solo builder: -5 on money.
    if as_bool(c, "giant_category") and scores.get("money") is not None:
        scores["money"] = max(0, scores["money"] - 5)
    s, missing = 0, []
    for axis in MAX:
        v = scores.get(axis)
        if v is None:
            missing.append(axis)
        else:
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


def build_rows(cands):
    names = [c.get("name") for c in cands]
    for n in names:
        if not n:
            fail("every candidate needs a 'name'")
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        fail(f"duplicate candidate names: {', '.join(sorted(dupes))}")

    live, dead = [], []
    for c in cands:
        warns = validate(c)
        fails, overrides = gate_failures(c)
        score, missing = total(c)
        row = {
            "name": c["name"],
            "pmf_tier": c.get("pmf_tier"),
            "axes": {a: (c.get("scores") or {}).get(a) for a in MAX},
            "total": score,
            "missing_axes": missing,
            "warnings": warns + overrides,
            "notes": c.get("notes", ""),
        }
        if fails:
            row["gates_failed"] = fails
            dead.append(row)
        else:
            row["verdict"] = verdict(score, missing)
            live.append(row)

    # Complete candidates first. Observed demand beats inferred demand: T3 gets a
    # 5-point sort bonus so it outranks T2 inside a 5-point band.
    live.sort(
        key=lambda r: (not r["missing_axes"], r["total"] + (5 if (r["pmf_tier"] or "").upper() == "T3" else 0)),
        reverse=True,
    )
    return live, dead


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args()

    try:
        with open(args.path) as f:
            data = json.load(f)
    except FileNotFoundError:
        fail(f"No such file: {args.path}")
    except json.JSONDecodeError as e:
        fail(f"{args.path} is not valid JSON: {e}")

    cands = data.get("candidates")
    if not cands:
        fail("scores.json has no 'candidates' array")

    live, dead = build_rows(cands)

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
            for w in r["warnings"]:
                print(f"   ! {w}")
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
