#!/usr/bin/env python3
"""Validate a competitor teardown and render its comparison matrix.

The rule this enforces: no source, no finding. Every finding needs a lens, a claim,
an evidence level, and (unless the evidence level is "unknown") an https URL and a
date. An "unknown" finding must say which lookup would settle it. A lens nobody
looked at is reported as NOT COVERED, which is different from "looked, found nothing".

Input (teardown.json):
{
  "product": "Plain Run",
  "competitors": [
    {"name": "Strava", "findings": [
      {"lens": "pricing", "claim": "Individual plan price", "value": "$79.99/yr",
       "evidence": "reported", "url": "https://example.com/page", "date": "2026-11-13"},
      {"lens": "traction", "claim": "Monthly revenue", "evidence": "unknown",
       "lookup": "Sensor Tower or Appfigures estimate for the app"}
    ]}
  ]
}

evidence: verified (first-party page or store listing read directly)
          reported (a secondary source states it)
          estimated (a tool or inference; say how in "note")
          unknown (could not be established)
lens:     positioning, onboarding, paywall, pricing, reviews, traction, changes, ui

Usage:
    python3 scripts/teardown_check.py teardown.json            # check + markdown matrix
    python3 scripts/teardown_check.py teardown.json --check    # check only (exit 1 on errors)
    python3 scripts/teardown_check.py teardown.json --json     # machine-readable summary
"""

import argparse
import json
import re
import sys
from datetime import date

LENSES = ["positioning", "onboarding", "paywall", "pricing", "reviews", "traction", "changes", "ui"]
EVIDENCE = ["verified", "reported", "estimated", "unknown"]
TAG = {"verified": "V", "reported": "R", "estimated": "E", "unknown": "?"}
URL_RE = re.compile(r"^https://[^\s/]+\.[^\s/]+")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check(data, today=None):
    """Return (errors, warnings, coverage). coverage[name][lens] = number of findings."""
    errors, warnings, coverage = [], [], {}
    today = today or date.today().isoformat()
    comps = data.get("competitors")
    if not isinstance(comps, list) or not comps:
        return ["competitors: need at least one competitor"], warnings, coverage
    for ci, comp in enumerate(comps):
        name = comp.get("name") or f"#{ci + 1}"
        coverage[name] = {lens: 0 for lens in LENSES}
        findings = comp.get("findings") or []
        if not findings:
            errors.append(f"{name}: no findings")
        for fi, f in enumerate(findings):
            where = f"{name} finding {fi + 1}"
            lens, ev = f.get("lens"), f.get("evidence")
            if lens not in LENSES:
                errors.append(f"{where}: lens {lens!r} not one of {LENSES}")
            else:
                coverage[name][lens] += 1
            if not str(f.get("claim", "")).strip():
                errors.append(f"{where}: empty claim")
            if ev not in EVIDENCE:
                errors.append(f"{where}: evidence {ev!r} not one of {EVIDENCE}")
                continue
            if ev == "unknown":
                if not str(f.get("lookup", "")).strip():
                    errors.append(f"{where}: unknown evidence must say which lookup would settle it ('lookup')")
                if f.get("value"):
                    errors.append(f"{where}: unknown evidence cannot carry a value")
                continue
            if not str(f.get("value", "")).strip() and lens not in ("onboarding", "ui", "positioning", "changes"):
                warnings.append(f"{where}: no value recorded for {lens}")
            url = str(f.get("url", ""))
            if not URL_RE.match(url):
                errors.append(f"{where}: needs an https URL (no source, no finding)")
            d = str(f.get("date", ""))
            if not DATE_RE.match(d):
                errors.append(f"{where}: needs a date as YYYY-MM-DD")
            elif d > today:
                errors.append(f"{where}: date {d} is in the future")
            if ev == "estimated" and not str(f.get("note", "")).strip():
                errors.append(f"{where}: estimated evidence must say how in 'note'")
    return errors, warnings, coverage


def render(data, coverage):
    comps = data["competitors"]
    names = [c.get("name") or f"#{i + 1}" for i, c in enumerate(comps)]
    out = [f"# Competitor matrix: {data.get('product', '')}".rstrip(": "), "",
           "Tags: [V] verified, [R] reported, [E] estimated, [?] unknown. NOT COVERED means nobody looked.", ""]
    out.append("| Lens | " + " | ".join(names) + " |")
    out.append("|---|" + "---|" * len(names))
    for lens in LENSES:
        cells = []
        for c, name in zip(comps, names):
            fs = [f for f in c.get("findings", []) if f.get("lens") == lens]
            if not fs:
                cells.append("NOT COVERED")
                continue
            parts = []
            for f in fs:
                val = f.get("value") or f.get("claim")
                parts.append(f"{val} [{TAG.get(f.get('evidence'), '?')}]")
            cells.append("<br>".join(parts))
        out.append(f"| {lens} | " + " | ".join(cells) + " |")
    out += ["", "## Sources", ""]
    for c, name in zip(comps, names):
        for f in c.get("findings", []):
            if f.get("url"):
                out.append(f"- {name} / {f.get('lens')}: {f['url']} ({f.get('date', 'undated')}, {f.get('evidence')})")
    unk = [(n, f) for c, n in zip(comps, names) for f in c.get("findings", []) if f.get("evidence") == "unknown"]
    if unk:
        out += ["", "## Still unknown (how to settle)", ""]
        out += [f"- {n} / {f.get('lens')}: {f.get('claim')} -> {f.get('lookup')}" for n, f in unk]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--check", action="store_true", help="validate only")
    ap.add_argument("--json", action="store_true", help="emit a JSON summary")
    a = ap.parse_args(argv)
    try:
        data = json.load(open(a.path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read {a.path}: {e}", file=sys.stderr)
        return 2
    errors, warnings, coverage = check(data)
    if a.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "coverage": coverage}, indent=2))
    else:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        for w in warnings:
            print("warning:", w, file=sys.stderr)
        if not a.check and not errors:
            print(render(data, coverage))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
