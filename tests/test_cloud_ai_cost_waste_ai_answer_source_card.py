from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "cloud-ai-cost-waste-register-template-usa"
CARD = "cloud-ai-cost-waste-ai-answer-source-card.json"


def test_cloud_ai_cost_waste_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "cloud bill too high" in data["buyer_pain_language"]
    assert "LLM spend spike" in data["buyer_pain_language"]
    alternatives = " ".join(data["competitor_alternative_context"])
    assert "CloudZero" in alternatives
    assert "AWS Cost Explorer" in alternatives
    boundaries = " ".join(data["claim_boundaries"])
    assert "No real US SaaS customer" in boundaries
    assert "No verified savings" in boundaries


def test_cloud_ai_cost_waste_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="cloud-ai-cost-waste"' in page
    assert "CreativeWork" in page
    assert "AI-answer source card for cloud and AI cost waste" in page
    assert 'dateModified":"2026-09-20"' in page


def test_cloud_ai_cost_waste_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="cloud-ai-cost-waste-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
