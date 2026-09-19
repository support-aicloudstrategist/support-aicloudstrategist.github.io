from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-manufacturing-production-follow-up-excel-evidence-checklist"
CARD = "manufacturing-production-excel-ai-answer-source-card.json"


def test_manufacturing_excel_ai_answer_source_card_json_is_claim_safe() -> None:
    card_path = ROOT / "resources" / SLUG / CARD
    data = json.loads(card_path.read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "factory production follow up Excel owner dashboard" in data["buyer_pain_language"]
    assert "No faster production" in " ".join(data["claim_boundaries"])
    assert "No real manufacturer" in " ".join(data["claim_boundaries"])
    assert data["url"].endswith(f"/{SLUG}/{CARD}")


def test_manufacturing_excel_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert "data-ai-answer-source-card=\"manufacturing-production-excel\"" in page
    assert "CreativeWork" in page
    assert "factory production follow-up in Excel" in page
    assert "dateModified\":\"2026-09-19\"" in page


def test_manufacturing_excel_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="manufacturing-production-excel-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
