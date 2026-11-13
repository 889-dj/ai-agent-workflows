#!/usr/bin/env python3
"""Tests for trend_check.py. Run: python3 scripts/test_trend_check.py"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trend_check as tc  # noqa: E402


def artifact_curve(scale=1.0, wobble=0):
    """Shape seen in two unrelated real terms: slow creep, step up, peak, fall."""
    s = [9 + 6 * i / 190 for i in range(190)]            # 9 -> 15 over ~3.6 years
    s += [15 + (100 - 15) * i / 45 for i in range(45)]    # step up to a peak
    s += [100 - (100 - 18) * i / 25 for i in range(25)]   # fall back
    return [max(0.0, v * scale + wobble * math.sin(i)) for i, v in enumerate(s)]


class TrendTests(unittest.TestCase):
    def test_short_series_unknown(self):
        self.assertEqual(tc.classify([5] * 10)[0], "unknown")

    def test_flat(self):
        self.assertEqual(tc.classify([20 + (i % 3) for i in range(200)])[0], "flat")

    def test_rising(self):
        self.assertEqual(tc.classify([10 + i * 0.4 for i in range(200)])[0], "rising")

    def test_declining(self):
        self.assertEqual(tc.classify([90 - i * 0.3 for i in range(200)])[0], "declining")

    def test_seasonal(self):
        s = [50 + 25 * math.sin(2 * math.pi * i / 52) for i in range(260)]
        self.assertEqual(tc.classify(s)[0], "seasonal")

    def test_artifact_shape_is_spiky(self):
        self.assertEqual(tc.classify(artifact_curve())[0], "spiky")

    def test_two_unrelated_terms_with_one_shape_flagged(self):
        out = tc.analyse({"running app": artifact_curve(1.0, 0.5), "subscription tracker": artifact_curve(0.8, 0.5)})
        self.assertEqual(len(out["shared_curves"]), 1)
        for t in out["terms"].values():
            self.assertTrue(t["shared_artifact_suspected"])
            self.assertEqual(t["score_as"], "spiky")

    def test_genuinely_different_terms_not_flagged(self):
        rising = [10 + i * 0.4 for i in range(260)]
        seasonal = [50 + 25 * math.sin(2 * math.pi * i / 52) for i in range(260)]
        out = tc.analyse({"a": rising, "b": seasonal})
        self.assertEqual(out["shared_curves"], [])

    def test_artifact_does_not_downgrade_a_flat_term(self):
        flat = [20 + (i % 3) for i in range(260)]
        out = tc.analyse({"a": flat, "b": [x * 2 for x in flat]})
        self.assertEqual(out["terms"]["a"]["score_as"], "flat")

    def test_extract_from_apify_rows(self):
        rows = [{"value": [i]} for i in range(30)]
        self.assertEqual(len(tc.extract_series(rows)["term"]), 30)

    def test_extract_from_dict_with_series(self):
        self.assertIn("x", tc.extract_series({"series": {"x": [1, 2, 3]}}))

    def test_pearson_constant_series_is_none(self):
        self.assertIsNone(tc.pearson([1] * 20, list(range(20))))


if __name__ == "__main__":
    unittest.main()
