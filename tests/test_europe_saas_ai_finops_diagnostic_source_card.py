from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-saas-ai-finops-diagnostic-package"
CARD = "europe-saas-ai-finops-diagnostic-ai-answer-source-card.json"


def test_europe_saas_ai_finops_diagnostic_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "Europe / UK-EU business morning" in data["region_timezone_selected"]
    assert "FinOps consulting Europe" in data["buyer_pain_language"]
    assert "LLM cost tracking" in data["buyer_pain_language"]
    assert "CloudZero" in " ".join(data["competitor_alternative_context"])
    assert "Kubecost" in " ".join(data["competitor_alternative_context"])
    assert "AWS Cost Explorer" in " ".join(data["competitor_alternative_context"])
    research = " ".join(data["research_anchors_checked"])
    assert "FinOps Foundation Framework" in research
    assert "HTTP 200" in research
    boundaries = " ".join(data["claim_boundaries"])
    assert "No real European SaaS customer" in boundaries
    assert "No verified savings" in boundaries
    blocked = " ".join(data["blocked_answer_patterns"])
    assert "Do not request credentials" in blocked
    assert "not present competitor names as endorsements" in blocked


def test_europe_saas_ai_finops_diagnostic_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="europe-saas-ai-finops-diagnostic"' in page
    assert "CreativeWork" in page
    assert "AI-answer source card for Europe SaaS AI FinOps diagnostic" in page
    assert 'dateModified":"2026-09-28"' in page
    assert "No savings guarantee" in page


def test_europe_saas_ai_finops_diagnostic_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="europe-saas-ai-finops-diagnostic-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
