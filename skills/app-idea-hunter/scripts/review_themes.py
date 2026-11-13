#!/usr/bin/env python3
"""Find recurring complaints in low-star app reviews.

Input: a JSON list of reviews (any scraper) with a text field and a rating field.
Field names are detected: text from one of review/text/body/content/title+body,
rating from rating/score/stars. Only reviews at or below --max-rating are used.

It counts (a) wish/request phrases and (b) topic keywords, and prints each theme
with how many distinct reviews mention it and two short examples. Counts are of
reviews, not of mentions, so one long rant cannot dominate.

Usage:
    python3 scripts/review_themes.py reviews.json
    python3 scripts/review_themes.py reviews.json --max-rating 3 --json
    python3 scripts/review_themes.py reviews.json --topics "subscription,ads,bug,sync,battery"
"""

import argparse
import json
import re
import sys
from collections import defaultdict

TEXT_KEYS = ("review", "text", "body", "content", "reviewText")
RATING_KEYS = ("rating", "score", "stars")

# Phrases that signal an unmet need. Each is a regex.
WISH_PATTERNS = {
    "wish it had": r"\bi wish\b|\bwish (?:it|they|there)\b",
    "why can't / why doesn't": r"\bwhy (?:can'?t|cannot|doesn'?t|does not|won'?t|isn'?t)\b",
    "should have / should be able": r"\bshould (?:have|be able|let|allow)\b",
    "missing / lacks": r"\b(?:missing|lacks?|no way to|no option to|can'?t even)\b",
    "used to be better": r"\bused to\b|\bsince the (?:update|latest)\b|\bgot worse\b|\bruined\b",
    "would pay / happy to pay": r"\bwould (?:gladly )?pay\b|\bhappy to pay\b|\bone[- ]time\b",
    "switching / cancelling": r"\bswitch(?:ing|ed)? to\b|\bcancel(?:l?ed|ling)?\b|\buninstall(?:ed|ing)?\b",
}

DEFAULT_TOPICS = [
    "subscription", "paywall", "price", "ads", "bug", "crash", "sync", "gps",
    "battery", "login", "lost", "accuracy", "watch", "support", "update",
]


def pick(d, keys):
    for k in keys:
        if d.get(k) not in (None, ""):
            return d[k]
    return None


def load_reviews(items, max_rating):
    out = []
    for r in items:
        text = pick(r, TEXT_KEYS)
        if text is None:
            title, body = r.get("title"), r.get("body")
            text = " ".join(x for x in (title, body) if x)
        rating = pick(r, RATING_KEYS)
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            continue
        if text and rating <= max_rating:
            out.append({"text": str(text), "rating": rating})
    return out


def analyse(reviews, topics=None):
    topics = topics or DEFAULT_TOPICS
    wish = defaultdict(list)
    topic = defaultdict(list)
    for i, r in enumerate(reviews):
        low = r["text"].lower()
        for name, pat in WISH_PATTERNS.items():
            if re.search(pat, low):
                wish[name].append(i)
        for t in topics:
            if re.search(rf"\b{re.escape(t.lower())}", low):
                topic[t].append(i)

    def pack(bucket):
        rows = []
        for name, idx in bucket.items():
            examples = [reviews[j]["text"].strip().replace("\n", " ")[:140] for j in idx[:2]]
            rows.append({
                "theme": name,
                "reviews": len(idx),
                "share": round(len(idx) / len(reviews), 3) if reviews else 0,
                "examples": examples,
            })
        return sorted(rows, key=lambda r: -r["reviews"])

    return {"reviews_used": len(reviews), "wishes": pack(wish), "topics": pack(topic)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--max-rating", type=float, default=3)
    ap.add_argument("--topics", default="", help="comma list overriding the default topic words")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        with open(args.path) as f:
            items = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"error: cannot read {args.path}: {e}")
    if isinstance(items, dict):
        items = items.get("items") or items.get("reviews") or []

    reviews = load_reviews(items, args.max_rating)
    if not reviews:
        raise SystemExit("error: no usable reviews (need a text field and a rating at or below --max-rating)")
    topics = [t for t in args.topics.split(",") if t.strip()] or None
    out = analyse(reviews, topics)

    if args.json:
        json.dump(out, sys.stdout, indent=2)
        print()
        return

    print(f"\n{out['reviews_used']} reviews at or below {args.max_rating:g} stars\n")
    for title, rows in (("Unmet-need phrases", out["wishes"]), ("Topics", out["topics"])):
        print(title)
        for r in rows[:8]:
            print(f"  {r['reviews']:>4} ({r['share']:.0%})  {r['theme']}")
            for e in r["examples"]:
                print(f"        - {e}")
        print()


if __name__ == "__main__":
    main()
