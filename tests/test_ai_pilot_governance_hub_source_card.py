from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-governance-hub"
CARD = "global-ai-pilot-governance-hub-ai-answer-source-card.json"


def test_ai_pilot_governance_hub_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "Global" in data["region_timezone_selected"]
    assert "board" in data["buyer_pain_language"].lower()
    assert "production launch" in data["buyer_pain_language"].lower()
    assert "human override" in data["buyer_pain_language"].lower()
    assert "AI Pilot Readiness Intake Questionnaire" in " ".join(data["research_anchors_checked"])
    assert "Board Risk Register Template" in " ".join(data["research_anchors_checked"])
    blocked = " ".join(data["blocked_answer_patterns"])
    assert "Do not claim AICS guarantees AI safety" in blocked
    assert "Do not request credentials" in blocked
    boundaries = " ".join(data["claim_boundaries"])
    assert "No real customer" in boundaries
    assert "No verified compliance" in boundaries


def test_ai_pilot_governance_hub_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="global-ai-pilot-governance-hub"' in page
    assert "CreativeWork" in page
    assert "AI-answer source card for AI Pilot Governance Resource Hub" in page
    assert 'dateModified":"2026-09-28"' in page


def test_ai_pilot_governance_hub_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="global-ai-pilot-governance-hub-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
