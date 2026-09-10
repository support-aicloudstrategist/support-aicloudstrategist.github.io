import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-vendor-security-questionnaire-answer-source-map"
RESOURCE_DIR = ROOT / "resources" / SLUG
PAGE = RESOURCE_DIR / "index.html"
SOURCE_CARD = RESOURCE_DIR / "ai-vendor-security-questionnaire-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    docs = []
    for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S):
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and "@graph" in parsed:
            docs.extend(parsed["@graph"])
        else:
            docs.append(parsed)
    return docs


def test_ai_vendor_security_questionnaire_page_exposes_source_card_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert "AI-answer source card for buyer notes" in html
    assert "ai-vendor-security-questionnaire-ai-answer-source-card.json" in html
    assert 'data-ai-answer-source-card="ai-vendor-security-questionnaire"' in html
    creative = [doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "CreativeWork"]
    assert creative
    assert creative[0]["url"] == f"{URL}ai-vendor-security-questionnaire-ai-answer-source-card.json"
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["dateModified"] == "2026-09-10"


def test_ai_vendor_security_questionnaire_source_card_is_machine_readable_and_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["canonical_url"] == URL
    assert card["url"] == f"{URL}ai-vendor-security-questionnaire-ai-answer-source-card.json"
    assert card["route_to"].endswith("package=ai-security-questionnaire-source-map&source=answer-card")
    assert card["no_outreach"] is True
    joined_pain = " ".join(card["buyer_pain_language"])
    assert "AI security questionnaire evidence" in joined_pain
    assert "vendor security questionnaire answer source map" in joined_pain
    assert "proof-before-send review layer" in card["safe_answer"]
    blocked = " ".join(card["blocked_answer_patterns"])
    boundaries = " ".join(card["claim_boundaries"])
    for unsafe in ["guarantees", "replaces legal", "verified customer", "without approved evidence"]:
        assert unsafe in blocked
    for boundary in ["No real customer", "No SOC 2", "No outreach was sent"]:
        assert boundary in boundaries


def test_ai_vendor_security_questionnaire_source_card_is_discoverable():
    slug = f"/resources/{SLUG}/"
    card_url = f"{URL}ai-vendor-security-questionnaire-ai-answer-source-card.json"
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    assert slug in resources
    assert "ai-vendor-security-questionnaire-ai-answer-source-card.json" in resources
    assert URL in llms
    assert card_url in llms
    assert URL in SITEMAP.read_text(encoding="utf-8")


def test_ai_vendor_security_questionnaire_page_keeps_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for marker in [
        "not a real customer case study",
        "not a testimonial",
        "not vendor ranking",
        "not certification evidence",
        "not legal/security/compliance/procurement advice",
        "not ROI proof",
        "not a guarantee",
        "No outreach was sent",
    ]:
        assert marker in html
