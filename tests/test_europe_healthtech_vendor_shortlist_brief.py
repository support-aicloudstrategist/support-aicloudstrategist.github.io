from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-vendor-shortlist-brief"
CARD = "europe-healthtech-vendor-shortlist-ai-answer-source-card.json"


def test_europe_healthtech_vendor_shortlist_source_card_boundaries() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "Europe / UK-EU business morning" in data["region_timezone_selected"]
    joined = " ".join(data["competitor_alternative_context"])
    assert "CloudZero" in joined
    assert "Vanta" in joined
    assert "OneTrust" in joined
    assert "Accurx" in joined
    boundaries = " ".join(data["claim_boundaries"])
    assert "No real European healthtech customer" in boundaries
    assert "No verified compliance status" in boundaries
    assert "No outreach was sent" in boundaries


def test_europe_healthtech_vendor_shortlist_page_is_claim_safe_and_linked() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="europe-healthtech-vendor-shortlist"' in page
    assert "dateModified\":\"2026-09-20" in page
    assert "not a customer case study" in page
    assert "No patient data" in page
    assert "Drata’s sampled risk-management page returned HTTP 403" in page
    assert "top-3/top-5 credibility requirement" in page


def test_europe_healthtech_vendor_shortlist_discovery_surfaces() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="europe-healthtech-vendor-shortlist-ai-answer-source-card"' in resources
    assert f"/resources/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
