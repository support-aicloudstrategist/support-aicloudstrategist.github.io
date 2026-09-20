from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-enterprise-ai-rfp-response-evidence-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "enterprise-ai-rfp-response-evidence-register.csv"
CARD = ROOT / "resources" / SLUG / "enterprise-ai-rfp-response-ai-answer-source-card.json"


def test_enterprise_ai_rfp_page_routes_answer_source_card():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert 'data-ai-answer-source-card="enterprise-ai-rfp-response"' in source
    assert "enterprise-ai-rfp-response-ai-answer-source-card.json" in source
    for marker in [
        "Enterprise AI RFP Response Evidence Checklist",
        "AI security questionnaire RFP",
        "AI vendor due diligence response",
        "AI human oversight RFP",
        "cost savings",
        "Truth boundary",
    ]:
        assert marker in source


def test_enterprise_ai_rfp_answer_card_is_claim_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["canonical_url"] == URL
    assert card["no_outreach"] is True
    assert card["route_to"].endswith("source=answer-card")
    pain_language = " ".join(card["buyer_pain_language"])
    for phrase in [
        "enterprise AI RFP response evidence",
        "AI security questionnaire RFP answer source",
        "AI procurement response proof boundary",
        "vendor due diligence AI human oversight evidence",
        "AI RFP cost savings claim boundary",
    ]:
        assert phrase in pain_language
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "No real customer case study",
        "No SOC 2, ISO, GDPR, HIPAA, EU AI Act",
        "No guaranteed revenue, ROI, RFP win rate",
        "No outreach was sent",
    ]:
        assert boundary in boundaries
    blocked = " ".join(card["do_not_claim"])
    assert "guarantees procurement approval" in blocked
    assert "replaces legal, privacy, security" in blocked


def test_enterprise_ai_rfp_answer_card_is_discoverable():
    csv_source = CSV.read_text(encoding="utf-8")
    assert "Lane" in csv_source
    assert "Approved answer owner" in csv_source
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "enterprise-ai-rfp-response-ai-answer-source-card.json" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{REL}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
