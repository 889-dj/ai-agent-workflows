#!/usr/bin/env python3
"""Tests for review_themes.py. Run: python3 scripts/test_review_themes.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_themes as rt  # noqa: E402


class ThemeTests(unittest.TestCase):
    def test_filters_by_rating(self):
        items = [{"review": "bad", "rating": 1}, {"review": "great", "rating": 5}, {"review": "meh", "rating": 3}]
        self.assertEqual(len(rt.load_reviews(items, 3)), 2)

    def test_field_name_detection(self):
        items = [{"text": "a", "score": 2}, {"title": "t", "body": "b", "stars": "1"}, {"content": "c", "rating": 1}]
        self.assertEqual(len(rt.load_reviews(items, 3)), 3)

    def test_skips_rows_without_rating_or_text(self):
        items = [{"review": "x"}, {"rating": 1}, {"review": "", "rating": 1}]
        self.assertEqual(rt.load_reviews(items, 3), [])

    def test_counts_distinct_reviews_not_mentions(self):
        reviews = [{"text": "subscription subscription subscription", "rating": 1}, {"text": "nice", "rating": 1}]
        out = rt.analyse(reviews, ["subscription"])
        row = out["topics"][0]
        self.assertEqual(row["reviews"], 1)

    def test_wish_phrases(self):
        reviews = [
            {"text": "I wish it had a widget", "rating": 2},
            {"text": "Why can't I export my runs?", "rating": 1},
            {"text": "I would gladly pay a one-time fee", "rating": 3},
            {"text": "Switching to another app", "rating": 1},
        ]
        names = {r["theme"] for r in rt.analyse(reviews)["wishes"]}
        self.assertIn("wish it had", names)
        self.assertIn("why can't / why doesn't", names)
        self.assertIn("would pay / happy to pay", names)
        self.assertIn("switching / cancelling", names)

    def test_share_and_sorting(self):
        reviews = [{"text": "ads ads", "rating": 1}, {"text": "ads", "rating": 1}, {"text": "bug", "rating": 1}]
        rows = rt.analyse(reviews, ["ads", "bug"])["topics"]
        self.assertEqual(rows[0]["theme"], "ads")
        self.assertAlmostEqual(rows[0]["share"], 0.667, places=2)

    def test_word_boundary(self):
        reviews = [{"text": "I have to pay a lot", "rating": 1}]
        self.assertEqual(rt.analyse(reviews, ["ad"])["topics"], [])


if __name__ == "__main__":
    unittest.main()
