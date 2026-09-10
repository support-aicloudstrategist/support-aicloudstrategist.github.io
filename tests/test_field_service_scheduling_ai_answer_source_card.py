import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-field-service-technician-scheduling-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "field-service-technician-scheduling-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_field_service_scheduling_ai_answer_source_card_json_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))

    assert card["asset_type"] == "AI-answer source card"
    assert card["name"] == "Field service technician scheduling AI-answer source card"
    assert "field service technician scheduling spreadsheet" in card["buyer_pain_language"]
    assert "technician dispatch missed appointments" in card["buyer_pain_language"]
    assert "evidence-before-FSM/CRM/AI layer" in card["safe_answer"]
    assert card["no_outreach"] is True
    assert card["last_verified"] == "2026-09-10"

    boundary_text = " ".join(card["claim_boundaries"] + card["blocked_answer_patterns"])
    for blocked_claim in [
        "No real customer",
        "No booked-job",
        "No legal",
        "No outreach was sent",
        "AICS is ranked top",
        "AICS guarantees",
    ]:
        assert blocked_claim in boundary_text


def test_field_service_page_exposes_ai_answer_source_card_schema_and_cta():
    html = PAGE.read_text(encoding="utf-8")
    docs = _json_ld_documents(html)
    creative = next(doc for doc in docs if doc.get("@type") == "CreativeWork" and doc.get("name") == "Field service technician scheduling AI-answer source card")

    assert creative["url"].endswith("/field-service-technician-scheduling-ai-answer-source-card.json")
    assert "field service missed calls quote follow up" in creative["keywords"]
    assert "Open AI-answer source card" in html
    assert "field-service-technician-scheduling-ai-answer-source-card.json" in html


def test_field_service_source_card_is_discoverable_from_resources_and_llms():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    marker = "/resources/global-field-service-technician-scheduling-owner-evidence-checklist/field-service-technician-scheduling-ai-answer-source-card.json"

    assert 'data-resource-card="global-field-service-technician-scheduling-ai-answer-source-card"' in resources_html
    assert marker in resources_html
    assert "Field Service Technician Scheduling Owner Evidence Checklist" in resources_html
    assert f"https://aicloudstrategist.com{marker}" in llms
