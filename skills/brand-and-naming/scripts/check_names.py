#!/usr/bin/env python3
"""Screen app-name candidates: domains, App Store collisions, and look-alikes.

What it checks, per candidate name:
  * Domains: RDAP lookups (the public successor to WHOIS) for each TLD.
        registered        the registry returned a record
        likely-available  the registry said "not found". Premium or reserved names
                          can also answer this way, so confirm at a registrar.
        unknown           the lookup failed, timed out or was blocked. NEVER read
                          this as available.
  * App Store: the public iTunes Search API (software). Lists existing apps whose
    name equals or closely resembles the candidate.
  * Look-alikes: string similarity against --competitors and against the other
    candidates, to catch names too close to an incumbent (or to each other).

What it cannot check, and says so: trademarks, Google Play names, social handles,
and meaning in other languages. Those stay manual (see SKILL.md). This is not
legal advice.

Usage:
    python3 scripts/check_names.py --names "Stride,Plainrun,Kilo" --competitors "Strava,Runna"
    python3 scripts/check_names.py --names-file names.txt --tlds com,app,io --json
    python3 scripts/check_names.py --names "Stride" --offline     # no network; everything unknown
"""

import argparse
import difflib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "name-screen/1.0 (+naming research script)"


def slug(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def fetch_json_status(url, timeout=8):
    """Return (http_status or None, parsed_json or None). None status = network failure."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rdap+json, application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
            try:
                return r.status, json.loads(body)
            except json.JSONDecodeError:
                return r.status, None
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return None, None


def check_domain(domain, fetch=fetch_json_status):
    status, _ = fetch("https://rdap.org/domain/" + urllib.parse.quote(domain))
    if status == 200:
        return "registered"
    if status == 404:
        return "likely-available"
    return "unknown"


def similar(a, b):
    a, b = slug(a), slug(b)
    if not a or not b:
        return 0.0
    r = difflib.SequenceMatcher(None, a, b).ratio()
    if a.startswith(b) or b.startswith(a):
        r = max(r, 0.85)
    return round(r, 2)


def check_app_store(name, country="us", fetch=fetch_json_status, threshold=0.8):
    """Return {"status": "checked"|"unknown", "matches": [...]}."""
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(
        {"term": name, "entity": "software", "limit": 15, "country": country})
    status, data = fetch(url)
    if status != 200 or not isinstance(data, dict):
        return {"status": "unknown", "matches": []}
    matches = []
    for r in data.get("results", []):
        tn = r.get("trackName", "")
        # compare against the part before a subtitle separator too ("Strava: Run & Ride")
        head = re.split(r"\s[-:|–—]\s|:\s", tn)[0]
        score = max(similar(name, tn), similar(name, head))
        if score >= threshold:
            matches.append({"app": tn, "seller": r.get("sellerName", ""), "similarity": score,
                            "url": r.get("trackViewUrl", "")})
    matches.sort(key=lambda m: -m["similarity"])
    return {"status": "checked", "matches": matches[:5]}


def screen(names, tlds, competitors, country="us", offline=False, fetch=fetch_json_status):
    results = []
    for n in names:
        s = slug(n)
        row = {"name": n, "slug": s, "length": len(s), "domains": {}, "app_store": None, "lookalikes": []}
        for t in tlds:
            row["domains"][f"{s}.{t}"] = "unknown" if offline else check_domain(f"{s}.{t}", fetch)
        row["app_store"] = ({"status": "unknown", "matches": []} if offline
                            else check_app_store(n, country, fetch))
        for c in competitors:
            sim = similar(n, c)
            if sim >= 0.7:
                row["lookalikes"].append({"with": c, "similarity": sim, "kind": "competitor"})
        for other in names:
            if other != n and similar(n, other) >= 0.8:
                row["lookalikes"].append({"with": other, "similarity": similar(n, other), "kind": "candidate"})
        row["verdict"] = verdict(row)
        results.append(row)
    return results


def verdict(row):
    """A coarse, conservative label. Only 'clear' when everything checked came back clean."""
    if any(l["kind"] == "competitor" for l in row["lookalikes"]):
        return "too-close-to-competitor"
    exact = [m for m in (row["app_store"] or {}).get("matches", []) if m["similarity"] >= 0.95]
    if exact:
        return "app-store-collision"
    vals = list(row["domains"].values())
    if vals and all(v == "registered" for v in vals):
        return "all-domains-taken"
    if (row["app_store"] or {}).get("status") != "checked" or "unknown" in vals:
        return "incomplete-check"
    if (row["app_store"] or {}).get("matches"):
        return "close-matches-review"
    return "clear-so-far"


def to_markdown(results, tlds):
    head = "| Name | Len | " + " | ".join("." + t for t in tlds) + " | App Store | Look-alikes | Verdict |"
    out = [head, "|---|---|" + "---|" * len(tlds) + "---|---|---|"]
    for r in results:
        doms = [r["domains"].get(f"{r['slug']}.{t}", "?") for t in tlds]
        a = r["app_store"]
        if a["status"] != "checked":
            store = "unknown"
        elif a["matches"]:
            store = "; ".join(f"{m['app']} ({m['similarity']})" for m in a["matches"][:2])
        else:
            store = "no close match"
        look = "; ".join(f"{l['with']} ({l['similarity']})" for l in r["lookalikes"]) or "-"
        out.append(f"| {r['name']} | {r['length']} | " + " | ".join(doms) + f" | {store} | {look} | {r['verdict']} |")
    out += ["", "Not checked here: trademarks, Google Play, social handles, other-language meanings, premium domain pricing.",
            "`unknown` means the lookup failed. It is not a sign the name is free."]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--names", help="comma-separated candidate names")
    ap.add_argument("--names-file", help="one name per line")
    ap.add_argument("--tlds", default="com,app,io", help="comma-separated (default com,app,io)")
    ap.add_argument("--competitors", default="", help="comma-separated incumbent names to avoid resembling")
    ap.add_argument("--country", default="us", help="App Store storefront (default us)")
    ap.add_argument("--offline", action="store_true", help="skip network lookups (everything unknown)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    names = [n.strip() for n in (a.names or "").split(",") if n.strip()]
    if a.names_file:
        names += [l.strip() for l in open(a.names_file, encoding="utf-8") if l.strip() and not l.startswith("#")]
    if not names:
        ap.error("give --names or --names-file")
    tlds = [t.strip().lstrip(".") for t in a.tlds.split(",") if t.strip()]
    comps = [c.strip() for c in a.competitors.split(",") if c.strip()]
    res = screen(names, tlds, comps, a.country, a.offline)
    print(json.dumps(res, indent=2) if a.json else to_markdown(res, tlds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
