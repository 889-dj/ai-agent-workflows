#!/usr/bin/env python3
"""Tests for pain_table.py. Run: python3 scripts/test_pain_table.py"""

import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pain_table as pt  # noqa: E402

TODAY = datetime.date(2026, 11, 13)


def th(i, label="own_problem", community="a", date="2026-10-01", asked=False, up=10):
    return {"url": f"https://x/{i}", "community": community, "date": date,
            "label": label, "asked_for_tool": asked, "upvotes": up}


def grade(threads):
    return pt.analyse({"candidate": "c", "threads": threads}, today=TODAY)


class PainTableTests(unittest.TestCase):
    def test_empty_is_t0(self):
        self.assertEqual(grade([])["suggested_grade"], "T0")

    def test_only_noise_is_t0(self):
        self.assertEqual(grade([th(1, "noise"), th(2, "noise")])["suggested_grade"], "T0")

    def test_bar_met_is_t2(self):
        ts = [th(i, community="a" if i % 2 else "b", asked=(i == 1)) for i in range(1, 6)]
        out = grade(ts)
        self.assertEqual(out["suggested_grade"], "T2")
        self.assertTrue(all(v["met"] for v in out["bar"].values()))

    def test_two_paying_or_hacking_is_t3(self):
        ts = [th(1, "paying", "a", asked=True), th(2, "hacking", "b"), th(3), th(4), th(5, community="b")]
        self.assertEqual(grade(ts)["suggested_grade"], "T3")

    def test_one_community_fails_bar(self):
        ts = [th(i, asked=(i == 1)) for i in range(1, 7)]
        out = grade(ts)
        self.assertEqual(out["suggested_grade"], "T1")
        self.assertFalse(out["bar"]["communities"]["met"])

    def test_stale_threads_fail_recency(self):
        ts = [th(i, community="a" if i % 2 else "b", date="2024-01-01", asked=(i == 1)) for i in range(1, 7)]
        self.assertFalse(grade(ts)["bar"]["recent"]["met"])

    def test_no_tool_ask_fails_bar(self):
        ts = [th(i, community="a" if i % 2 else "b") for i in range(1, 7)]
        self.assertFalse(grade(ts)["bar"]["asked_for_tool"]["met"])

    def test_contented_majority_is_t1(self):
        ts = [th(1), th(2, "contented"), th(3, "contented")]
        self.assertEqual(grade(ts)["suggested_grade"], "T1")

    def test_duplicates_count_once(self):
        ts = [th(1, asked=True)] * 6
        self.assertEqual(grade(ts)["qualifying"], 1)

    def test_promo_and_scam_not_counted(self):
        ts = [th(i, "promo") for i in range(1, 4)] + [th(9, "scam")]
        self.assertEqual(grade(ts)["qualifying"], 0)

    def test_defender_warning(self):
        ts = [th(1, up=10, asked=True), th(2, "defender", up=34)]
        self.assertTrue(any("defender" in w for w in grade(ts)["warnings"]))

    def test_low_topical_yield_warns(self):
        ts = [th(1)] + [th(i, "noise") for i in range(2, 9)]
        self.assertTrue(any("on topic" in w for w in grade(ts)["warnings"]))

    def test_bad_label_rejected(self):
        with self.assertRaises(ValueError):
            grade([th(1, "great")])


if __name__ == "__main__":
    unittest.main()
