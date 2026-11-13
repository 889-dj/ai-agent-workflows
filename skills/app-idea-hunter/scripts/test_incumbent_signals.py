#!/usr/bin/env python3
"""Tests for incumbent_signals.py. Run: python3 scripts/test_incumbent_signals.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import incumbent_signals as sig  # noqa: E402


def app(name, dev, ratings, cur=None):
    return {"appName": name, "developer": dev, "ratingCount": ratings, "ratingCountCurrentVersion": cur}


class SignalTests(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual(sig.usage_tier(250_000), "large")
        self.assertEqual(sig.usage_tier(10_000), "mid")
        self.assertEqual(sig.usage_tier(1_000), "small")
        self.assertEqual(sig.usage_tier(999), "tiny")
        self.assertEqual(sig.usage_tier(None), "tiny")

    def test_strong_needs_three_independents(self):
        apps = [app("A", "x", 50_000), app("B", "y", 20_000), app("C", "z", 15_000), app("Big", "Nike", 400_000)]
        out = sig.analyse(apps, giants=["Nike"])
        self.assertEqual(out["signal_strength"], "strong")
        self.assertEqual(out["independents_mid_or_larger"], 3)

    def test_giants_do_not_count(self):
        apps = [app("Big", "Nike", 400_000), app("Tiny", "x", 50)]
        self.assertEqual(sig.analyse(apps, giants=["Nike"])["signal_strength"], "weak")

    def test_moderate(self):
        apps = [app("A", "x", 30_000), app("B", "y", 100)]
        self.assertEqual(sig.analyse(apps)["signal_strength"], "moderate")

    def test_recent_share_handles_missing_and_caps(self):
        self.assertIsNone(sig.recent_share(app("A", "x", 1000, None)))
        self.assertEqual(sig.recent_share(app("A", "x", 1000, 250)), 0.25)
        self.assertEqual(sig.recent_share(app("A", "x", 1000, 5000)), 1.0)

    def test_no_dollar_fields_in_output(self):
        out = sig.analyse([app("A", "x", 30_000)])
        self.assertNotIn("revenue", str(out).lower().replace("note", "").split("proxy only")[0])


if __name__ == "__main__":
    unittest.main()
