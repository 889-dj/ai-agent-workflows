#!/usr/bin/env python3
"""Turn App Store scraper output into a proxy-signal table (no revenue guesses).

Reads a JSON list of apps (fields as returned by automation-lab/apple-app-store-
scraper: appName, developer, formattedPrice, rating, ratingCount,
ratingCountCurrentVersion, currentVersionDate) and reports, per app, a usage
tier and a recent-activity share, then an overall signal strength for the niche.

It never converts ratings into dollars. See references/revenue.md.

Usage:
    python3 scripts/incumbent_signals.py apps.json
    python3 scripts/incumbent_signals.py apps.json --giants "Nike,Strava,Apple" --paywall-known "Strava,Runna"
    python3 scripts/incumbent_signals.py apps.json --json
"""

import argparse
import json
import sys


def usage_tier(rating_count):
    n = rating_count or 0
    if n >= 100_000:
        return "large"
    if n >= 10_000:
        return "mid"
    if n >= 1_000:
        return "small"
    return "tiny"


def recent_share(app):
    total = app.get("ratingCount") or 0
    cur = app.get("ratingCountCurrentVersion")
    if not total or cur is None:
        return None
    return round(min(cur / total, 1.0), 3)


def is_giant(app, giants):
    hay = f"{app.get('developer', '')} {app.get('appName', '')}".lower()
    return any(g.strip().lower() in hay for g in giants if g.strip())


def analyse(apps, giants=(), paywall_known=()):
    rows = []
    for a in apps:
        giant = is_giant(a, giants)
        paywall = is_giant(a, paywall_known)
        rows.append({
            "app": a.get("appName"),
            "developer": a.get("developer"),
            "ratings": a.get("ratingCount") or 0,
            "tier": usage_tier(a.get("ratingCount")),
            "recent_share": recent_share(a),
            "giant": giant,
            "paywall_known": paywall,
        })
    # Independents at mid size or larger are the best sign for a solo builder.
    indie_mid = [r for r in rows if not r["giant"] and r["tier"] in {"mid", "large"}]
    if len(indie_mid) >= 3:
        strength = "strong"
    elif len(indie_mid) >= 1:
        strength = "moderate"
    else:
        strength = "weak"
    return {
        "signal_strength": strength,
        "independents_mid_or_larger": len(indie_mid),
        "apps": rows,
        "note": "Proxy only. This says money probably exists, not how much.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--giants", default="", help="comma list of developer/app name fragments to treat as giants")
    ap.add_argument("--paywall-known", default="", help="comma list of apps you verified have a paid tier")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        with open(args.path) as f:
            apps = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"error: cannot read {args.path}: {e}")
    if isinstance(apps, dict):
        apps = apps.get("items") or apps.get("apps") or []
    if not apps:
        raise SystemExit("error: no apps in input")

    out = analyse(apps, args.giants.split(","), args.paywall_known.split(","))
    if args.json:
        json.dump(out, sys.stdout, indent=2)
        print()
        return

    print(f"\nProxy signal strength: {out['signal_strength'].upper()} "
          f"({out['independents_mid_or_larger']} independents at mid size or larger)\n")
    print(f"{'App':<38}{'Ratings':>10}  {'Tier':<6}{'Recent':>8}  Flags")
    print("-" * 78)
    for r in sorted(out["apps"], key=lambda r: -r["ratings"]):
        flags = ", ".join(f for f, on in (("giant", r["giant"]), ("paywall", r["paywall_known"])) if on)
        recent = "--" if r["recent_share"] is None else f"{r['recent_share']:.0%}"
        print(f"{(r['app'] or '?')[:37]:<38}{r['ratings']:>10}  {r['tier']:<6}{recent:>8}  {flags}")
    print(f"\n{out['note']}\n")


if __name__ == "__main__":
    main()
