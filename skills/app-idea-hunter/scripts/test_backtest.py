#!/usr/bin/env python3
"""Tests for backtest.py. Run: python3 scripts/test_backtest.py"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import backtest as bt  # noqa: E402


def case(name, total_parts, result):
    pain, money, demand, mkt, feas = total_parts
    return {"name": name, "as_of": "2026-01-01",
            "scores": {"pain": pain, "money": money, "demand": demand, "marketability": mkt, "feasibility": feas},
            "outcome": {"result": result, "evidence": "", "resolved_on": ""}}


class BacktestTests(unittest.TestCase):
    def test_rank_handles_ties(self):
        self.assertEqual(bt.rank([10, 20, 20, 30]), [1.0, 2.5, 2.5, 4.0])

    def test_spearman_perfect_and_inverse(self):
        self.assertAlmostEqual(bt.spearman([1, 2, 3, 4], [1, 2, 3, 4]), 1.0)
        self.assertAlmostEqual(bt.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)

    def test_spearman_needs_variation_and_size(self):
        self.assertIsNone(bt.spearman([1, 1, 1, 1], [1, 2, 3, 4]))
        self.assertIsNone(bt.spearman([1, 2], [1, 2]))

    def test_report_with_nothing_resolved(self):
        out = bt.report({"cases": [case("a", (20, 20, 15, 15, 8), "pending")]})
        self.assertEqual(out["resolved"], 0)
        self.assertIn("message", out)

    def test_small_sample_is_flagged_as_anecdote(self):
        cases = [case("a", (25, 20, 15, 15, 8), "success"), case("b", (5, 5, 5, 5, 3), "failure"),
                 case("c", (15, 10, 10, 10, 5), "partial")]
        out = bt.report({"cases": cases})
        self.assertFalse(out["enough_data"])
        self.assertTrue(any("anecdote" in n for n in out["notes"]))

    def test_good_scores_predict_good_outcomes(self):
        cases = []
        for i in range(5):
            cases.append(case(f"hi{i}", (25, 22, 16, 16, 8), "success"))
            cases.append(case(f"lo{i}", (5, 5, 4, 4, 2), "failure"))
        out = bt.report({"cases": cases})
        self.assertTrue(out["enough_data"])
        self.assertGreater(out["total_vs_outcome_spearman"], 0.9)
        self.assertEqual(out["predicted_positive"], {"n": 5, "worked_out": 5})
        self.assertEqual(out["predicted_negative"], {"n": 5, "failed_as_predicted": 5})

    def test_add_is_idempotent_and_writes_pending(self):
        with tempfile.TemporaryDirectory() as d:
            sp, lp = os.path.join(d, "s.json"), os.path.join(d, "sub", "log.json")
            json.dump({"candidates": [{"name": "X", "pmf_tier": "T2", "wedge": "w",
                                       "scores": {"pain": 12, "money": 10, "demand": 8, "marketability": 10, "feasibility": 6}}]},
                      open(sp, "w"))
            self.assertEqual(bt.add(sp, lp, "2026-02-01"), 1)
            self.assertEqual(bt.add(sp, lp, "2026-02-01"), 0)
            log = json.load(open(lp))
            self.assertEqual(log["cases"][0]["outcome"]["result"], "pending")
            self.assertEqual(log["cases"][0]["total"], 46)
            self.assertEqual(log["cases"][0]["predicted_band"], "KILL")


if __name__ == "__main__":
    unittest.main()
