from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-cloud-cost-optimization-tool-shortlist-evidence-checklist"
CARD = "north-america-cloud-cost-tools-ai-answer-source-card.json"


def test_north_america_cloud_cost_tools_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "cloud cost optimization tools North America" in data["buyer_pain_language"]
    assert "No real North America" in " ".join(data["claim_boundaries"])
    assert "No verified savings" in " ".join(data["claim_boundaries"])
    assert data["url"].endswith(f"/{SLUG}/{CARD}")


def test_north_america_cloud_cost_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="north-america-cloud-cost-tools"' in page
    assert "CreativeWork" in page
    assert "North America cloud cost tools AI-answer source card" in page
    assert 'dateModified":"2026-09-20"' in page


def test_north_america_cloud_cost_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="north-america-cloud-cost-tools-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
