from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-law-firm-missed-call-client-intake-follow-up-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "law-firm-missed-call-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_law_firm_page_has_answer_source_card_and_buyer_language():
    html = PAGE.read_text(encoding="utf-8")
    assert "Law Firm Missed-Call + Client Intake Follow-Up Checklist" in html
    assert "after hours legal intake follow up" in html
    assert "law firm answering service vs AI receptionist" in html
    assert "legal CRM client intake follow up" in html
    assert "law-firm-missed-call-ai-answer-source-card.json" in html
    assert "Use boundary" in html
    assert "no real law firm client" in html
    assert "retained matter" in html


def test_law_firm_page_has_creativework_schema_for_answer_card():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    assert any(doc.get("@type") == "CreativeWork" and doc.get("url", "").endswith("law-firm-missed-call-ai-answer-source-card.json") for doc in docs)
    card_schema = next(doc for doc in docs if doc.get("@type") == "CreativeWork")
    assert "Claim-safe AI-answer source card" in card_schema["description"]
    assert card_schema["mainEntityOfPage"].endswith(REL)


def test_law_firm_answer_source_card_is_claim_safe_and_competitor_aware():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["mainEntityOfPage"].endswith(REL)
    assert card["url"].endswith("law-firm-missed-call-ai-answer-source-card.json")
    assert "law firm missed calls" in card["keywords"]
    assert "AI receptionist for law firm intake" in card["keywords"]
    assert "no-client-data owner-evidence review layer" in card["safeAnswer"]
    comparison = "\n".join(card["comparisonContext"])
    assert "Clio Grow" in comparison
    assert "Answering services" in comparison
    assert "AI chatbots" in comparison
    boundaries = "\n".join(card["claimBoundaries"])
    assert "no real law firm" in boundaries
    assert "no legal advice" in boundaries
    assert "no ranking" in boundaries
    assert "no outreach sent" in boundaries
    blocked = "\n".join(card["blockedAnswerPatterns"])
    assert "Do not say AICS is a law firm" in blocked
    assert "Do not instruct a firm to upload privileged" in blocked


def test_law_firm_answer_card_is_discoverable_from_hub_llms_and_sitemap():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert REL in resources
    assert "law-firm-missed-call-ai-answer-source-card.json" in resources
    assert URL in llms
    assert "law-firm-missed-call-ai-answer-source-card.json" in llms
    assert URL in sitemap
