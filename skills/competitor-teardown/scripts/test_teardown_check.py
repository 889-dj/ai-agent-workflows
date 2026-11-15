#!/usr/bin/env python3
"""Tests for teardown_check.py. Run: python3 scripts/test_teardown_check.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import teardown_check as tc  # noqa: E402

TODAY = "2026-11-15"


def good(**kw):
    f = {"lens": "pricing", "claim": "Individual plan", "value": "$79.99/yr", "evidence": "reported",
         "url": "https://example.com/p", "date": "2026-11-13"}
    f.update(kw)
    return f


def data(*findings):
    return {"product": "X", "competitors": [{"name": "A", "findings": list(findings)}]}


class CheckTests(unittest.TestCase):
    def errs(self, *findings):
        return tc.check(data(*findings), today=TODAY)[0]

    def test_valid_finding_passes(self):
        self.assertEqual(self.errs(good()), [])

    def test_no_url_is_an_error(self):
        self.assertTrue(any("https URL" in e for e in self.errs(good(url=""))))
        self.assertTrue(any("https URL" in e for e in self.errs(good(url="http://insecure.example.com"))))

    def test_missing_or_future_date_is_an_error(self):
        self.assertTrue(any("date" in e for e in self.errs(good(date=""))))
        self.assertTrue(any("future" in e for e in self.errs(good(date="2027-01-01"))))

    def test_unknown_needs_a_lookup_and_no_value(self):
        self.assertTrue(any("lookup" in e for e in self.errs({"lens": "traction", "claim": "MRR", "evidence": "unknown"})))
        ok = {"lens": "traction", "claim": "MRR", "evidence": "unknown", "lookup": "Sensor Tower"}
        self.assertEqual(self.errs(ok), [])
        self.assertTrue(any("cannot carry a value" in e for e in self.errs(dict(ok, value="$1M"))))

    def test_estimated_needs_a_note(self):
        self.assertTrue(any("note" in e for e in self.errs(good(evidence="estimated"))))
        self.assertEqual(self.errs(good(evidence="estimated", note="from rank and category")), [])

    def test_bad_lens_and_evidence(self):
        self.assertTrue(any("lens" in e for e in self.errs(good(lens="vibes"))))
        self.assertTrue(any("evidence" in e for e in self.errs(good(evidence="trust me"))))

    def test_competitor_without_findings(self):
        errors, _, _ = tc.check({"competitors": [{"name": "A", "findings": []}]}, today=TODAY)
        self.assertTrue(any("no findings" in e for e in errors))

    def test_coverage_counts_lenses(self):
        _, _, cov = tc.check(data(good(), good(lens="reviews", value="3 themes")), today=TODAY)
        self.assertEqual(cov["A"]["pricing"], 1)
        self.assertEqual(cov["A"]["reviews"], 1)
        self.assertEqual(cov["A"]["paywall"], 0)

    def test_render_marks_uncovered_lenses_and_tags(self):
        d = data(good())
        md = tc.render(d, tc.check(d, today=TODAY)[2])
        self.assertIn("$79.99/yr [R]", md)
        self.assertIn("NOT COVERED", md)
        self.assertIn("https://example.com/p", md)

    def test_render_lists_unknowns_with_how_to_settle(self):
        d = data(good(), {"lens": "traction", "claim": "MRR", "evidence": "unknown", "lookup": "Sensor Tower"})
        md = tc.render(d, tc.check(d, today=TODAY)[2])
        self.assertIn("Still unknown", md)
        self.assertIn("Sensor Tower", md)


if __name__ == "__main__":
    unittest.main()
