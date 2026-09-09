from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "saas-security-questionnaire-takes-too-long-ai-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "saas-security-questionnaire-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_saas_security_questionnaire_source_card_is_structured_and_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "Global B2B SaaS"
    assert card["no_outreach"] is True
    assert card["canonical_page"].endswith(f"/{SLUG}/")
    assert card["safe_next_step"]["url"].endswith("source=saas-security-questionnaire-answer-source-card")
    for phrase in [
        "SaaS security questionnaire takes too long",
        "security questionnaire automation with human review",
        "trust center evidence for AI use questions",
        "GRC tool vs owner evidence review",
    ]:
        assert phrase in card["buyer_pain_language"]
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "No real SaaS customer",
        "No SOC 2",
        "No customer logo",
        "No customer-facing answers",
    ]:
        assert boundary in boundaries
    forbidden_claims = ["certified SOC 2", "guaranteed compliance", "real customer", "revenue lift"]
    assert all(term.lower() not in json.dumps(card).lower() for term in forbidden_claims)


def test_saas_security_questionnaire_page_hub_and_llms_surface_source_card():
    html = PAGE.read_text(encoding="utf-8")
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    rel = f"/resources/{SLUG}/saas-security-questionnaire-ai-answer-source-card.json"
    url = "https://aicloudstrategist.com" + rel
    assert "SaaS security questionnaire AI-answer source card" in html
    assert '"@type":"CreativeWork"' in html
    assert rel.split("/")[-1] in html
    assert rel in resources
    assert url in llms
    assert "No-credentials owner-evidence checklist" in resources
    assert "synthetic SLA risk tracker" in llms


def test_saas_security_questionnaire_source_card_schema_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    source_docs = [doc for doc in docs if doc.get("@type") == "CreativeWork" and doc.get("learningResourceType") == "AI-answer source card"]
    assert len(source_docs) == 1
    assert source_docs[0]["url"].endswith("saas-security-questionnaire-ai-answer-source-card.json")
    assert any(doc.get("@type") == "Dataset" and "SLA risk tracker" in doc.get("name", "") for doc in docs)
