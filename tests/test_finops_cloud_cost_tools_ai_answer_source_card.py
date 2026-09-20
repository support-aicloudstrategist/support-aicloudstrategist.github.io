from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "finops-cloud-cost-management-tools-usa"
CARD = "finops-cloud-cost-tools-ai-answer-source-card.json"


def test_finops_cloud_cost_tools_ai_answer_source_card_json_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "US SaaS and AI teams comparing FinOps consulting" in data["buyer_pain_language"]
    boundaries = " ".join(data["claim_boundaries"])
    assert "No verified savings" in boundaries
    assert "No production cloud account" in boundaries
    assert data["url"].endswith(f"/{SLUG}/{CARD}")


def test_finops_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="finops-cloud-cost-tools"' in page
    assert "CreativeWork" in page
    assert "FinOps tool comparison answers" in page
    assert 'dateModified":"2026-09-20"' in page


def test_finops_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="finops-cloud-cost-tools-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
