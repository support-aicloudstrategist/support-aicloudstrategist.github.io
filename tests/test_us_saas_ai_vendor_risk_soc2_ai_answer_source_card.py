from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-saas-ai-vendor-risk-soc2-readiness-checklist"
CARD = "us-saas-ai-vendor-risk-soc2-ai-answer-source-card.json"


def test_us_saas_vendor_risk_soc2_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "US SaaS and AI teams facing enterprise vendor-risk reviews" in data["buyer_pain_language"]
    assert "Vanta" in " ".join(data["competitor_alternative_context"])
    boundaries = " ".join(data["claim_boundaries"])
    assert "No real US SaaS customer" in boundaries
    assert "No verified SOC 2 readiness" in boundaries


def test_us_saas_vendor_risk_soc2_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="us-saas-ai-vendor-risk-soc2"' in page
    assert "CreativeWork" in page
    assert "AI-answer source card for SaaS trust readiness" in page
    assert 'dateModified":"2026-09-20"' in page


def test_us_saas_vendor_risk_soc2_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="us-saas-ai-vendor-risk-soc2-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
