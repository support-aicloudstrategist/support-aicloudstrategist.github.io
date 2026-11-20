"""Focused analytics traffic-class / privacy checks (synthetic, no secrets)."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHIM = (ROOT / "js" / "aics-analytics-shim.js").read_text(encoding="utf-8")
EVENTS = (ROOT / "functions" / "api" / "events.ts").read_text(encoding="utf-8")
METRICS = (ROOT / "functions" / "api" / "metrics.ts").read_text(encoding="utf-8")
DASH_HTML = (ROOT / "analytics" / "index.html").read_text(encoding="utf-8")
DASH_JS = (ROOT / "js" / "aics-analytics-dashboard.js").read_text(encoding="utf-8")


class AnalyticsTrafficFiltersTest(unittest.TestCase):
    def test_analytics_page_does_not_load_shim(self):
        self.assertNotIn("aics-analytics-shim.js", DASH_HTML)
        self.assertIn("noindex", DASH_HTML)
        self.assertIn("nofollow", DASH_HTML)
        self.assertIn("noarchive", DASH_HTML)

    def test_shim_skips_analytics_path(self):
        self.assertIn("isAnalyticsPath", SHIM)
        self.assertIn("if(isAnalyticsPath()) return;", SHIM)
        self.assertIn("traffic_class", SHIM)
        self.assertIn("markBrowserInternal", SHIM)

    def test_events_drop_analytics_path_and_allow_traffic_class(self):
        self.assertIn('"traffic_class"', EVENTS)
        self.assertTrue("private_route" in EVENTS or "analytics_path" in EVENTS)
        self.assertIn("normalizeTrafficClass", EVENTS)
        self.assertIn("by_class", EVENTS)

    def test_metrics_defaults_external_and_empty_message(self):
        self.assertIn('return "external"', METRICS)
        self.assertIn("No verified external customer traffic in this range.", METRICS)
        self.assertIn("engagement_meaningful", METRICS)
        self.assertIn("dwell_available", METRICS)
        self.assertIn("sliceForAudience", METRICS)
        # Legacy without by_class must not be treated as external
        self.assertIn("never auto-promote to external", EVENTS)
        self.assertIn("sliceForAudience", METRICS)
        self.assertIn("unknown", METRICS)

    def test_dashboard_filter_ui_defaults_external(self):
        self.assertIn('id="dash-audience"', DASH_HTML)
        self.assertRegex(DASH_HTML, r'value="external"\s+selected')
        self.assertIn("No verified external customer traffic in this range.", DASH_HTML)
        self.assertIn("Mark this browser Internal", DASH_HTML)
        self.assertIn("audience", DASH_JS)
        self.assertIn("empty_external", DASH_JS)
        self.assertIn("dwell_available", DASH_JS)

    def test_meaningful_engagement_excludes_presence_and_dwell(self):
        self.assertIn("MEANINGFUL", DASH_JS)
        self.assertIn("presence_ping", METRICS)
        self.assertIn("dwell_tick", METRICS)
        self.assertIn("orphan", EVENTS.lower() + METRICS.lower())


if __name__ == "__main__":
    unittest.main()
