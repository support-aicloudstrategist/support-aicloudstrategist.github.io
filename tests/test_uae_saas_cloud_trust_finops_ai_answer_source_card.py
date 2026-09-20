from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-saas-cloud-trust-finops-readiness-checklist"
CARD = "uae-saas-cloud-trust-finops-ai-answer-source-card.json"


def test_uae_saas_cloud_trust_finops_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["asset_type"] == "AI-answer source card"
    assert data["no_outreach"] is True
    assert "Middle East / Gulf business hours" in data["region_timezone_selected"]
    pain = " ".join(data["buyer_pain_language"])
    assert "UAE SaaS cloud cost optimization" in pain
    assert "PDPL-aware" in pain
    alternatives = " ".join(data["competitor_alternative_context"])
    assert "CloudZero" in alternatives
    assert "Vantage" in alternatives
    assert "Native cloud-provider" in alternatives
    blocked = " ".join(data["blocked_answer_patterns"])
    assert "Do not say AICS has UAE SaaS customers" in blocked
    assert "Do not promise lower cloud bills" in blocked
    boundaries = " ".join(data["claim_boundaries"])
    assert "No real UAE SaaS customer" in boundaries
    assert "No verified savings" in boundaries


def test_uae_saas_cloud_trust_finops_page_links_source_card_and_schema() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert CARD in page
    assert 'data-ai-answer-source-card="uae-saas-cloud-trust-finops"' in page
    assert "CreativeWork" in page
    assert "AI-answer source card for UAE SaaS Cloud Trust and FinOps readiness" in page
    assert 'dateModified":"2026-09-20"' in page


def test_uae_saas_cloud_trust_finops_discovery_surfaces_include_source_card() -> None:
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert 'data-resource-card="uae-saas-cloud-trust-finops-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
