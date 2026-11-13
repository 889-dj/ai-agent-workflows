#!/usr/bin/env python3
"""Tests for score.py. Run: python3 scripts/test_score.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score  # noqa: E402


def cand(**kw):
    base = {
        "name": "x", "pmf_tier": "T2", "money_evidence": "estimated", "trend": "rising_both",
        "build_days": 10, "budget_days": 14, "hazard": False,
        "scores": {"pain": 12, "money": 18, "demand": 15, "marketability": 12, "feasibility": 6},
    }
    base.update(kw)
    return base


class ScoreTests(unittest.TestCase):
    def rows(self, *cs):
        return score.build_rows(list(cs))

    def test_clean_candidate_survives(self):
        live, dead = self.rows(cand())
        self.assertEqual((len(live), len(dead)), (1, 0))
        self.assertEqual(live[0]["total"], 63)

    def test_t0_t1_killed(self):
        for t in ("T0", "T1"):
            live, dead = self.rows(cand(pmf_tier=t, scores={"pain": 0, "money": 18, "demand": 15, "marketability": 12, "feasibility": 6}))
            self.assertEqual(len(dead), 1, t)

    def test_ungraded_killed(self):
        _, dead = self.rows(cand(pmf_tier=None))
        self.assertEqual(len(dead), 1)

    def test_money_none_kills_but_unknown_and_missing_do_not(self):
        _, dead = self.rows(cand(money_evidence="none"))
        self.assertEqual(len(dead), 1)
        live, _ = self.rows(cand(money_evidence="unknown"))
        self.assertEqual(len(live), 1)
        c = cand()
        del c["money_evidence"]
        live, _ = self.rows(c)
        self.assertEqual(len(live), 1)
        self.assertTrue(live[0]["warnings"])

    def test_t3_overrides_money_none(self):
        live, dead = self.rows(cand(pmf_tier="T3", money_evidence="none",
                                    scores={"pain": 25, "money": 5, "demand": 15, "marketability": 12, "feasibility": 6}))
        self.assertEqual((len(live), len(dead)), (1, 0))
        self.assertIn("waived", live[0]["warnings"][0])

    def test_flat_trend_kills_unknown_does_not(self):
        _, dead = self.rows(cand(trend="flat", scores={"pain": 12, "money": 18, "demand": 8, "marketability": 12, "feasibility": 6}))
        self.assertEqual(len(dead), 1)
        live, _ = self.rows(cand(trend="unknown"))
        self.assertEqual(len(live), 1)

    def test_budget_gate(self):
        _, dead = self.rows(cand(build_days=22, budget_days=14))
        self.assertEqual(len(dead), 1)
        live, _ = self.rows(cand(build_days=21, budget_days=14))
        self.assertEqual(len(live), 1)

    def test_hazard_string_false_is_not_a_hazard(self):
        live, _ = self.rows(cand(hazard="false"))
        self.assertEqual(len(live), 1)
        _, dead = self.rows(cand(hazard="true"))
        self.assertEqual(len(dead), 1)
        with self.assertRaises(SystemExit):
            self.rows(cand(hazard="maybe"))

    def test_pain_ceiling_by_tier(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(pmf_tier="T2", scores={"pain": 25, "money": 18, "demand": 15, "marketability": 12, "feasibility": 6}))

    def test_demand_ceiling_by_trend(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(trend="spiky", scores={"pain": 12, "money": 18, "demand": 18, "marketability": 12, "feasibility": 6}))

    def test_marketability_cap_without_first_video(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(first_video=False, scores={"pain": 12, "money": 18, "demand": 15, "marketability": 14, "feasibility": 6}))

    def test_giant_category_penalty_applied_once(self):
        live, _ = self.rows(cand(giant_category=True))
        self.assertEqual(live[0]["total"], 58)

    def test_bad_enum_and_duplicates_rejected(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(trend="sideways"))
        with self.assertRaises(SystemExit):
            self.rows(cand(money_evidence="lots"))
        with self.assertRaises(SystemExit):
            self.rows(cand(), cand())

    def test_incomplete_ranks_below_complete(self):
        full = cand(name="full", scores={"pain": 12, "money": 10, "demand": 5, "marketability": 4, "feasibility": 3})
        part = cand(name="part", scores={"pain": 18, "money": 25, "demand": 20, "marketability": None, "feasibility": 10})
        live, _ = self.rows(part, full)
        self.assertEqual([r["name"] for r in live], ["full", "part"])
        self.assertEqual(live[1]["verdict"], "INCOMPLETE")

    def test_wedge_is_passed_through_and_missing_wedge_warns(self):
        live, _ = self.rows(cand(wedge="clean run tracker, no upsells"))
        self.assertEqual(live[0]["wedge"], "clean run tracker, no upsells")
        self.assertFalse(any("wedge" in w for w in live[0]["warnings"]))
        live, _ = self.rows(cand())
        self.assertTrue(any("wedge" in w for w in live[0]["warnings"]))

    def test_t3_wins_within_five_points(self):
        t2 = cand(name="t2", scores={"pain": 18, "money": 18, "demand": 15, "marketability": 12, "feasibility": 10})
        t3 = cand(name="t3", pmf_tier="T3", scores={"pain": 25, "money": 18, "demand": 14, "marketability": 8, "feasibility": 6})
        live, _ = self.rows(t2, t3)
        self.assertEqual(live[0]["name"], "t3")


if __name__ == "__main__":
    unittest.main()
