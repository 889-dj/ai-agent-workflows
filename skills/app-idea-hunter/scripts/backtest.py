#!/usr/bin/env python3
"""Prediction log and backtest for the app-idea-hunter scoring weights.

The weights in scoring.md are judgement, not fact. This keeps a log of every
prediction and, once the real outcome is known, shows whether high scores really
went with good outcomes and which axes carried the signal.

Two commands:

  add     append the candidates from a scores.json to the log as `pending`
            python3 scripts/backtest.py add hunt/scores.json log/predictions.json --as-of 2026-11-13

  report  compare predictions with resolved outcomes
            python3 scripts/backtest.py report log/predictions.json
            python3 scripts/backtest.py report log/predictions.json --json

To resolve a case, edit it in the log: set outcome.result to success / partial /
failure, and fill outcome.evidence (a link or note) and outcome.resolved_on.

Outcome meaning (use the same yardstick every time, and write it down):
  success  paying users and it is growing or sustaining (or a comparable product did)
  partial  some traction but not enough to justify the build
  failure  no traction, or it was abandoned

Selection bias is real: ideas you never built have no outcome. Where you can,
resolve a case from an outside observation (a similar app that launched and
either took off or did not) and say so in outcome.evidence.
"""

import argparse
import datetime
import json
import os
import sys

AXES = ["pain", "money", "demand", "marketability", "feasibility"]
OUTCOME_VALUE = {"success": 2, "partial": 1, "failure": 0}
MIN_RESOLVED = 8   # below this the numbers are anecdotes, and the report says so


def rank(values):
    """Average ranks (1-based), ties share the mean rank."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def band(total):
    if total >= 80:
        return "BUILD"
    if total >= 65:
        return "STRONG"
    if total >= 50:
        return "PARKING LOT"
    return "KILL"


def total_of(case):
    s = case.get("scores") or {}
    return sum(v for v in s.values() if isinstance(v, (int, float)))


def add(scores_path, log_path, as_of):
    with open(scores_path) as f:
        cands = (json.load(f) or {}).get("candidates") or []
    log = {"cases": []}
    if os.path.exists(log_path):
        with open(log_path) as f:
            log = json.load(f)
    existing = {(c["name"], c["as_of"]) for c in log["cases"]}
    added = 0
    for c in cands:
        key = (c["name"], as_of)
        if key in existing:
            continue
        total = sum(v for v in (c.get("scores") or {}).values() if isinstance(v, (int, float)))
        log["cases"].append({
            "name": c["name"],
            "as_of": as_of,
            "wedge": c.get("wedge"),
            "pmf_tier": c.get("pmf_tier"),
            "scores": c.get("scores"),
            "confidence": c.get("confidence"),
            "total": total,
            "predicted_band": band(total),
            "outcome": {"result": "pending", "evidence": "", "resolved_on": ""},
        })
        added += 1
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)
        f.write("\n")
    return added


def report(log):
    cases = log.get("cases") or []
    resolved = [c for c in cases if (c.get("outcome") or {}).get("result") in OUTCOME_VALUE]
    pending = [c for c in cases if (c.get("outcome") or {}).get("result") == "pending"]
    out = {"cases": len(cases), "resolved": len(resolved), "pending": len(pending),
           "enough_data": len(resolved) >= MIN_RESOLVED}
    if not resolved:
        out["message"] = "No resolved outcomes yet. Resolve cases in the log, then rerun."
        return out

    totals = [c.get("total", total_of(c)) for c in resolved]
    results = [OUTCOME_VALUE[c["outcome"]["result"]] for c in resolved]
    out["total_vs_outcome_spearman"] = _r(spearman(totals, results))

    pos = [c for c, t in zip(resolved, totals) if band(t) in {"BUILD", "STRONG"}]
    neg = [c for c, t in zip(resolved, totals) if band(t) in {"PARKING LOT", "KILL"}]
    out["predicted_positive"] = {
        "n": len(pos),
        "worked_out": sum(1 for c in pos if OUTCOME_VALUE[c["outcome"]["result"]] >= 1),
    }
    out["predicted_negative"] = {
        "n": len(neg),
        "failed_as_predicted": sum(1 for c in neg if OUTCOME_VALUE[c["outcome"]["result"]] == 0),
    }

    per_axis = {}
    for a in AXES:
        pairs = [((c.get("scores") or {}).get(a), OUTCOME_VALUE[c["outcome"]["result"]]) for c in resolved]
        pairs = [(x, y) for x, y in pairs if isinstance(x, (int, float))]
        per_axis[a] = {"n": len(pairs), "spearman": _r(spearman([p[0] for p in pairs], [p[1] for p in pairs]))}
    out["per_axis"] = per_axis

    notes = []
    if not out["enough_data"]:
        notes.append(f"only {len(resolved)} resolved cases (need at least {MIN_RESOLVED}); treat every number as an anecdote, not evidence")
    ranked = [(a, v["spearman"]) for a, v in per_axis.items() if v["spearman"] is not None]
    if out["enough_data"] and ranked:
        weakest = min(ranked, key=lambda x: x[1])
        strongest = max(ranked, key=lambda x: x[1])
        notes.append(f"strongest predictor so far: {strongest[0]} ({strongest[1]:+.2f}); weakest: {weakest[0]} ({weakest[1]:+.2f}). "
                     "Consider shifting weight only after many more cases.")
    out["notes"] = notes
    return out


def _r(x):
    return None if x is None else round(x, 3)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("scores")
    a.add_argument("log")
    a.add_argument("--as-of", default=datetime.date.today().isoformat())
    r = sub.add_parser("report")
    r.add_argument("log")
    r.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.cmd == "add":
        try:
            n = add(args.scores, args.log, args.as_of)
        except (OSError, json.JSONDecodeError, KeyError) as e:
            raise SystemExit(f"error: {e}")
        print(f"Added {n} pending case(s) to {args.log}")
        return

    try:
        with open(args.log) as f:
            log = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"error: cannot read {args.log}: {e}")
    out = report(log)
    if args.json:
        json.dump(out, sys.stdout, indent=2)
        print()
        return
    print(f"\nCases {out['cases']} · resolved {out['resolved']} · pending {out['pending']}")
    if "message" in out:
        print(out["message"] + "\n")
        return
    print(f"Total vs outcome (Spearman): {out['total_vs_outcome_spearman']}")
    p, n = out["predicted_positive"], out["predicted_negative"]
    print(f"Predicted build/strong: {p['worked_out']}/{p['n']} worked out")
    print(f"Predicted parked/killed: {n['failed_as_predicted']}/{n['n']} failed as predicted")
    print("Per axis (Spearman vs outcome):")
    for k, v in out["per_axis"].items():
        print(f"  {k:<14} {v['spearman']}  (n={v['n']})")
    for note in out["notes"]:
        print(f"  ! {note}")
    print()


if __name__ == "__main__":
    main()
