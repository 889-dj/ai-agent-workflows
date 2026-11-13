#!/usr/bin/env python3
"""Turn labelled Reddit threads into a reproducible PMF evidence table and a
SUGGESTED grade (T0-T3). A human or the orchestrator confirms the grade.

Input: a JSON file {"candidate": "...", "threads": [ ... ]} where each thread is

    {
      "url": "https://www.reddit.com/r/...",
      "community": "Strava",
      "date": "2026-10-09",
      "label": "own_problem",          # see LABELS
      "asked_for_tool": false,         # someone explicitly asks what to use
      "upvotes": 316,
      "comments": 149,
      "note": "short paraphrase"
    }

LABELS
  own_problem   a person describes the problem as theirs (counts toward the bar)
  paying        pays for a tool they dislike, or paid and regretted it (T3 signal)
  hacking       spreadsheet / DIY / manual routine to cope (T3 signal)
  contented     mentions it but is happy with their workaround (pushes toward T1)
  defender      argues the complaint is unreasonable (counter-evidence)
  promo         product promotion or ad (excluded)
  scam          fraud or spam (excluded)
  noise         off topic (excluded; counts toward the on-topic rate)

Usage:
    python3 scripts/pain_table.py hunt/pmf-<candidate>.json
    python3 scripts/pain_table.py hunt/pmf-<candidate>.json --json
"""

import argparse
import datetime
import json
import sys

LABELS = {"own_problem", "paying", "hacking", "contented", "defender", "promo", "scam", "noise"}
QUALIFYING = {"own_problem", "paying", "hacking"}
EXCLUDED = {"promo", "scam", "noise"}

BAR = {"threads": 5, "communities": 2, "recent_days": 183}


def parse_date(s):
    try:
        return datetime.date.fromisoformat(str(s)[:10])
    except (ValueError, TypeError):
        return None


def analyse(data, today=None):
    today = today or datetime.date.today()
    threads = data.get("threads") or []
    errors = []
    for i, t in enumerate(threads):
        if t.get("label") not in LABELS:
            errors.append(f"thread {i + 1}: label must be one of {sorted(LABELS)}, got {t.get('label')!r}")
        if not t.get("url"):
            errors.append(f"thread {i + 1}: missing url")
    if errors:
        raise ValueError("; ".join(errors))

    # A thread may appear twice (cross-post or duplicate fetch): count each url once.
    seen, uniq = set(), []
    for t in threads:
        if t["url"] in seen:
            continue
        seen.add(t["url"])
        uniq.append(t)

    qualifying = [t for t in uniq if t["label"] in QUALIFYING]
    defenders = [t for t in uniq if t["label"] == "defender"]
    contented = [t for t in uniq if t["label"] == "contented"]
    excluded = [t for t in uniq if t["label"] in EXCLUDED]
    on_topic = len(uniq) - len([t for t in uniq if t["label"] == "noise"])

    communities = {str(t.get("community", "")).lower() for t in qualifying if t.get("community")}
    recent = [
        t for t in qualifying
        if (d := parse_date(t.get("date"))) and (today - d).days <= BAR["recent_days"]
    ]
    asked = [t for t in qualifying if t.get("asked_for_tool")]
    t3_signals = [t for t in qualifying if t["label"] in {"paying", "hacking"}]

    bar = {
        "threads": (len(qualifying), BAR["threads"], len(qualifying) >= BAR["threads"]),
        "communities": (len(communities), BAR["communities"], len(communities) >= BAR["communities"]),
        "recent": (len(recent), 1, len(recent) >= 1),
        "asked_for_tool": (len(asked), 1, len(asked) >= 1),
    }
    bar_met = all(v[2] for v in bar.values())

    defender_weight = sum(t.get("upvotes") or 0 for t in defenders)
    pain_weight = sum(t.get("upvotes") or 0 for t in qualifying)

    reasons = []
    if not qualifying and not contented:
        grade = "T0"
        reasons.append("no qualifying threads found")
    elif not qualifying or (contented and len(contented) > len(qualifying)):
        grade = "T1"
        reasons.append("complaints exist but people are content with their workaround")
    elif not bar_met:
        grade = "T1"
        missing = [k for k, v in bar.items() if not v[2]]
        reasons.append("evidence bar not met: " + ", ".join(missing))
    elif len(t3_signals) >= 2:
        grade = "T3"
        reasons.append(f"{len(t3_signals)} threads show people paying for or hacking around the problem")
    else:
        grade = "T2"
        reasons.append("bar met; recurring complaint and people asking for a tool")

    warnings = []
    if defenders and defender_weight and pain_weight and defender_weight >= 0.5 * pain_weight:
        warnings.append("defender threads carry at least half the upvotes of the pain threads; pain may be weaker than it looks")
    if on_topic and uniq and (on_topic / len(uniq)) < 0.4:
        warnings.append(f"only {on_topic}/{len(uniq)} rows were on topic; the query may be poor, not the niche")
    if len(set(t["url"] for t in qualifying)) != len(qualifying):
        warnings.append("duplicate qualifying threads")

    return {
        "candidate": data.get("candidate"),
        "suggested_grade": grade,
        "reasons": reasons,
        "bar": {k: {"have": v[0], "need": v[1], "met": v[2]} for k, v in bar.items()},
        "rows": len(uniq),
        "on_topic_rate": round(on_topic / len(uniq), 2) if uniq else None,
        "qualifying": len(qualifying),
        "defenders": len(defenders),
        "excluded": len(excluded),
        "warnings": warnings,
        "confirm": "Suggested only. Read the deep-read notes and confirm the grade.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        with open(args.path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"error: cannot read {args.path}: {e}")
    try:
        out = analyse(data)
    except ValueError as e:
        raise SystemExit(f"error: {e}")

    if args.json:
        json.dump(out, sys.stdout, indent=2)
        print()
        return

    print(f"\nCandidate: {out['candidate']}")
    print(f"Suggested grade: {out['suggested_grade']}   ({'; '.join(out['reasons'])})\n")
    print("Evidence bar")
    for k, v in out["bar"].items():
        print(f"  [{'x' if v['met'] else ' '}] {k:<15} {v['have']}/{v['need']}")
    rate = "n/a" if out["on_topic_rate"] is None else f"{out['on_topic_rate']:.0%}"
    print(f"\nRows {out['rows']} · on-topic {rate} · qualifying {out['qualifying']} · "
          f"defenders {out['defenders']} · excluded {out['excluded']}")
    for w in out["warnings"]:
        print(f"  ! {w}")
    print(f"\n{out['confirm']}\n")


if __name__ == "__main__":
    main()
