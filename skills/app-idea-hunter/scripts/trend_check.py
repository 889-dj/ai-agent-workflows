#!/usr/bin/env python3
"""Classify a Google Trends series and flag a shared-artifact curve.

Why: in two real hunts, unrelated search terms ("subscription tracker",
"running app") returned almost the same curve - flat to mid-2025, a step up, a
peak, then a drop. When different terms share one shape, the shape is probably a
data artifact, not demand. This script makes that check routine.

Input JSON: {"series": {"term a": [weekly values...], "term b": [...], "control": [...]}}
or a list of the same weekly timeline rows Apify returns for one term
(interestOverTime_timelineData). Values are 0-100.

Output: per term, a shape (rising / flat / declining / spiky / seasonal), the
ratio of the latest level to the earlier baseline, and a list of term pairs whose
curves correlate above --artifact-threshold (default 0.9).

Usage:
    python3 scripts/trend_check.py series.json
    python3 scripts/trend_check.py series.json --json
"""

import argparse
import json
import math
import sys


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def pearson(a, b):
    n = min(len(a), len(b))
    if n < 8:
        return None
    a, b = a[-n:], b[-n:]
    ma, mb = mean(a), mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    if da == 0 or db == 0:
        return None
    return num / (da * db)


def detrend(series):
    """Subtract a straight-line fit so a steady rise or fall is not mistaken for a season."""
    n = len(series)
    if n < 3:
        return list(series)
    xs = list(range(n))
    mx, my = mean(xs), mean(series)
    den = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, series)) / den if den else 0.0
    return [y - (my + slope * (x - mx)) for x, y in zip(xs, series)]


def yearly_pattern(series, period=52):
    """Correlation of the last year with the year before it, after removing the trend.

    Also requires a real wave: the detrended residual must swing by at least 15% of
    the average level, otherwise noise around a flat line could look 'seasonal'."""
    if len(series) < period * 2:
        return None
    resid = detrend(series)
    level = mean(series) or 1.0
    if (max(resid) - min(resid)) < 0.15 * level:
        return None
    return pearson(resid[-period:], resid[-2 * period:-period])


def classify(series):
    """Return (shape, details). Pure function of the weekly values."""
    s = [float(x) for x in series if x is not None]
    if len(s) < 26:
        return "unknown", {"reason": "fewer than 26 points"}

    n = len(s)
    peak = max(s)
    peak_idx = s.index(peak)
    baseline = mean(s[: n // 2])        # earlier half
    recent = mean(s[-8:])               # last two months
    prior = mean(s[-34:-8]) if n >= 34 else mean(s[: n - 8])
    first_q, last_q = mean(s[: n // 4]), mean(s[-(n // 4):])

    season = yearly_pattern(s)
    spike_ratio = peak / (baseline or 1)
    off_peak = recent / (peak or 1)
    trend_ratio = last_q / (first_q or 1)
    details = {
        "baseline": round(baseline, 1), "recent": round(recent, 1), "peak": peak,
        "peak_position": round(peak_idx / (n - 1), 2),
        "recent_vs_baseline": round(recent / (baseline or 1), 2),
        "recent_vs_peak": round(off_peak, 2),
        "last_quarter_vs_first_quarter": round(trend_ratio, 2),
        "year_over_year_correlation": None if season is None else round(season, 2),
    }

    if season is not None and season >= 0.6 and spike_ratio < 3:
        return "seasonal", details
    # A big peak that has since fallen well below it, but stays above baseline.
    if spike_ratio >= 2.5 and off_peak <= 0.5:
        return "spiky", details
    if trend_ratio >= 1.25:
        return "rising", details
    if trend_ratio <= 0.75:
        return "declining", details
    return "flat", details


def extract_series(obj):
    """Accept {"series": {...}} or Apify timeline rows for a single term."""
    if isinstance(obj, dict) and "series" in obj:
        return {k: [float(x) for x in v] for k, v in obj["series"].items()}
    rows = obj
    if isinstance(obj, dict):
        rows = obj.get("interestOverTime_timelineData") or []
    if rows and isinstance(rows, list) and isinstance(rows[0], dict):
        vals = []
        for r in rows:
            v = r.get("value")
            vals.append(float(v[0] if isinstance(v, list) else v))
        return {"term": vals}
    raise ValueError("unrecognised input shape")


def analyse(series_map, threshold=0.9):
    shapes = {k: classify(v) for k, v in series_map.items()}
    shared = []
    keys = list(series_map)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            r = pearson(series_map[keys[i]], series_map[keys[j]])
            if r is not None and r >= threshold:
                shared.append({"terms": [keys[i], keys[j]], "correlation": round(r, 3)})
    verdicts = {}
    for k, (shape, d) in shapes.items():
        in_pair = any(k in p["terms"] for p in shared)
        verdicts[k] = {
            "shape": shape,
            "details": d,
            "shared_artifact_suspected": in_pair,
            "score_as": "spiky" if (in_pair and shape in {"rising", "spiky"}) else shape,
        }
    return {"terms": verdicts, "shared_curves": shared,
            "note": "A shared curve across unrelated terms is treated as an artifact: score as spiky and rely on related queries and other signals."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--artifact-threshold", type=float, default=0.9)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        with open(args.path) as f:
            obj = json.load(f)
        series_map = extract_series(obj)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        raise SystemExit(f"error: {e}")

    out = analyse(series_map, args.artifact_threshold)
    if args.json:
        json.dump(out, sys.stdout, indent=2)
        print()
        return
    print()
    for k, v in out["terms"].items():
        flag = "  ! shares a curve with another term" if v["shared_artifact_suspected"] else ""
        print(f"{k}: shape={v['shape']}  score_as={v['score_as']}{flag}")
        d = v["details"]
        if "baseline" in d:
            print(f"    baseline {d['baseline']} -> recent {d['recent']} (peak {d['peak']}, "
                  f"recent/peak {d['recent_vs_peak']})")
    for p in out["shared_curves"]:
        print(f"\nShared curve: {p['terms'][0]} ~ {p['terms'][1]} (r={p['correlation']})")
    print(f"\n{out['note']}\n")


if __name__ == "__main__":
    main()
