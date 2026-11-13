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
        self.assertTrue(any("waived" in w for w in live[0]["warnings"]))

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

    def test_confidence_range_and_flip_warning(self):
        conf = {"pain": "high", "money": "low", "demand": "low", "marketability": "medium", "feasibility": "low"}
        live, _ = self.rows(cand(money_evidence="listed", trend="spiky", confidence=conf,
                                 scores={"pain": 18, "money": 10, "demand": 7, "marketability": 18, "feasibility": 6}))
        cf = live[0]["confidence"]
        self.assertEqual(cf["overall"], "low")
        self.assertTrue(cf["verdict_could_flip"])
        self.assertTrue(any("sensitive" in w for w in live[0]["warnings"]))

    def test_all_high_confidence_is_tight(self):
        conf = {a: "high" for a in ("pain", "money", "demand", "marketability", "feasibility")}
        live, _ = self.rows(cand(money_evidence="verified", confidence=conf))
        self.assertEqual(live[0]["confidence"]["range"][0], live[0]["confidence"]["range"][1])
        self.assertEqual(live[0]["confidence"]["overall"], "high")

    def test_cannot_claim_high_money_confidence_on_proxies(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(money_evidence="listed", confidence={"money": "high"}))

    def test_cannot_claim_high_demand_confidence_on_spiky_trend(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(trend="spiky", scores={"pain": 12, "money": 18, "demand": 7, "marketability": 12, "feasibility": 6},
                           confidence={"demand": "high"}))

    def test_bad_confidence_values_rejected(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(confidence={"money": "certain"}))
        with self.assertRaises(SystemExit):
            self.rows(cand(confidence={"vibes": "low"}))

    def test_missing_confidence_warns(self):
        live, _ = self.rows(cand())
        self.assertTrue(any("confidence not recorded" in w for w in live[0]["warnings"]))

    def test_fatal_blocker_kills(self):
        _, dead = self.rows(cand(blockers=[{"area": "API", "severity": "fatal", "note": "only data source closed", "source": "x"}]))
        self.assertEqual(len(dead), 1)
        self.assertTrue(any("Fatal blocker" in g for g in dead[0]["gates_failed"]))

    def test_major_blocker_caps_feasibility(self):
        b = [{"area": "API", "severity": "major", "note": "paid API", "source": "https://x"}]
        live, _ = self.rows(cand(blockers=b))  # feasibility 6 is allowed
        self.assertEqual(len(live), 1)
        with self.assertRaises(SystemExit):
            self.rows(cand(blockers=b, scores={"pain": 12, "money": 18, "demand": 15, "marketability": 12, "feasibility": 8}))

    def test_minor_blocker_does_not_cap(self):
        b = [{"area": "legal", "severity": "minor", "note": "avoid medical claims"}]
        live, _ = self.rows(cand(blockers=b, scores={"pain": 12, "money": 18, "demand": 15, "marketability": 12, "feasibility": 10}))
        self.assertEqual(len(live), 1)

    def test_empty_blockers_list_means_checklist_done(self):
        live, _ = self.rows(cand(blockers=[]))
        self.assertFalse(any("blocker checklist" in w for w in live[0]["warnings"]))
        live, _ = self.rows(cand())
        self.assertTrue(any("blocker checklist" in w for w in live[0]["warnings"]))

    def test_blocker_validation(self):
        with self.assertRaises(SystemExit):
            self.rows(cand(blockers=[{"severity": "huge", "note": "x"}]))
        with self.assertRaises(SystemExit):
            self.rows(cand(blockers=[{"severity": "major"}]))
        with self.assertRaises(SystemExit):
            self.rows(cand(blockers="none"))

    def test_major_blocker_without_source_warns(self):
        live, _ = self.rows(cand(blockers=[{"severity": "major", "note": "paid API"}]))
        self.assertTrue(any("no source" in w for w in live[0]["warnings"]))

    def test_unchecked_areas_reported(self):
        live, _ = self.rows(cand(blockers=[], unchecked_areas=["Regional availability"]))
        self.assertTrue(any("not checked" in w for w in live[0]["warnings"]))

    def test_t3_wins_within_five_points(self):
        t2 = cand(name="t2", scores={"pain": 18, "money": 18, "demand": 15, "marketability": 12, "feasibility": 10})
        t3 = cand(name="t3", pmf_tier="T3", scores={"pain": 25, "money": 18, "demand": 14, "marketability": 8, "feasibility": 6})
        live, _ = self.rows(t2, t3)
        self.assertEqual(live[0]["name"], "t3")


if __name__ == "__main__":
    unittest.main()
