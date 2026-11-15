#!/usr/bin/env python3
"""Tests for check_names.py (no network). Run: python3 scripts/test_check_names.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_names as cn  # noqa: E402


def fake_fetch(routes):
    """routes: {substring_of_url: (status, json)}; no match -> network failure (None, None)."""
    def fetch(url, timeout=8):
        for key, val in routes.items():
            if key in url:
                return val
        return None, None
    return fetch


class DomainTests(unittest.TestCase):
    def test_registered_available_and_unknown(self):
        self.assertEqual(cn.check_domain("a.com", fake_fetch({"a.com": (200, {})})), "registered")
        self.assertEqual(cn.check_domain("a.com", fake_fetch({"a.com": (404, None)})), "likely-available")
        self.assertEqual(cn.check_domain("a.com", fake_fetch({})), "unknown")

    def test_server_errors_are_unknown_not_available(self):
        for code in (429, 500, 502, 403):
            self.assertEqual(cn.check_domain("a.com", fake_fetch({"a.com": (code, None)})), "unknown")


class SimilarityTests(unittest.TestCase):
    def test_identical_prefix_and_distinct(self):
        self.assertEqual(cn.similar("Strava", "strava"), 1.0)
        self.assertGreaterEqual(cn.similar("Stravo", "Strava"), 0.8)
        self.assertGreaterEqual(cn.similar("Runna", "Runnamo"), 0.85)  # prefix rule
        self.assertLess(cn.similar("Kilo", "Strava"), 0.5)

    def test_slug(self):
        self.assertEqual(cn.slug("Plain Run!"), "plainrun")


class AppStoreTests(unittest.TestCase):
    RESULTS = {"results": [
        {"trackName": "Strava: Run & Ride", "sellerName": "Strava Inc", "trackViewUrl": "https://apps.apple.com/x"},
        {"trackName": "Totally Different App", "sellerName": "Y", "trackViewUrl": "https://apps.apple.com/y"}]}

    def test_finds_collision_using_title_head(self):
        r = cn.check_app_store("Strava", fetch=fake_fetch({"itunes.apple.com": (200, self.RESULTS)}))
        self.assertEqual(r["status"], "checked")
        self.assertEqual(r["matches"][0]["app"], "Strava: Run & Ride")
        self.assertEqual(len(r["matches"]), 1)

    def test_failure_is_unknown_not_clean(self):
        r = cn.check_app_store("Kilo", fetch=fake_fetch({}))
        self.assertEqual(r["status"], "unknown")


class ScreenTests(unittest.TestCase):
    def test_competitor_lookalike_flagged(self):
        rows = cn.screen(["Stravo"], ["com"], ["Strava"], fetch=fake_fetch({"rdap": (404, None), "itunes": (200, {"results": []})}))
        self.assertEqual(rows[0]["verdict"], "too-close-to-competitor")

    def test_never_clear_when_lookups_fail(self):
        rows = cn.screen(["Kilo"], ["com", "app"], [], fetch=fake_fetch({}))
        self.assertEqual(rows[0]["verdict"], "incomplete-check")

    def test_offline_is_incomplete(self):
        rows = cn.screen(["Kilo"], ["com"], [], offline=True)
        self.assertEqual(rows[0]["verdict"], "incomplete-check")
        self.assertEqual(rows[0]["domains"]["kilo.com"], "unknown")

    def test_clear_only_when_everything_came_back_clean(self):
        f = fake_fetch({"rdap": (404, None), "itunes": (200, {"results": []})})
        self.assertEqual(cn.screen(["Kilo"], ["com"], [], fetch=f)[0]["verdict"], "clear-so-far")

    def test_exact_app_store_match_is_a_collision(self):
        f = fake_fetch({"rdap": (404, None), "itunes": (200, {"results": [{"trackName": "Kilo", "sellerName": "Z", "trackViewUrl": "u"}]})})
        self.assertEqual(cn.screen(["Kilo"], ["com"], [], fetch=f)[0]["verdict"], "app-store-collision")

    def test_all_domains_taken(self):
        f = fake_fetch({"rdap": (200, {}), "itunes": (200, {"results": []})})
        self.assertEqual(cn.screen(["Kilo"], ["com", "app"], [], fetch=f)[0]["verdict"], "all-domains-taken")

    def test_candidates_too_similar_to_each_other_are_noted(self):
        rows = cn.screen(["Kilo", "Kilos"], ["com"], [], offline=True)
        self.assertTrue(any(l["kind"] == "candidate" for l in rows[0]["lookalikes"]))

    def test_markdown_has_disclaimer(self):
        md = cn.to_markdown(cn.screen(["Kilo"], ["com"], [], offline=True), ["com"])
        self.assertIn("unknown", md)
        self.assertIn("Not checked here", md)


if __name__ == "__main__":
    unittest.main()
