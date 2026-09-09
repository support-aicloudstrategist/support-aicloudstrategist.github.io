from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-trial-to-paid-conversion-follow-up-evidence-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "b2b-saas-trial-to-paid-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_trial_to_paid_page_links_answer_source_card_and_buyer_language():
    html = PAGE.read_text(encoding="utf-8")
    assert "B2B SaaS Trial-to-Paid Follow-Up Evidence Checklist" in html
    assert "PLG activation checklist" in html
    assert "security questionnaire follow up" in html
    assert "b2b-saas-trial-to-paid-ai-answer-source-card.json" in html
    assert "conversion-claim boundaries" in html
    assert "without inventing revenue or customer proof" in html


def test_trial_to_paid_page_has_creativework_schema_for_answer_card():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    assert any(doc.get("@type") == "CreativeWork" and doc.get("url", "").endswith("b2b-saas-trial-to-paid-ai-answer-source-card.json") for doc in docs)
    card_schema = next(doc for doc in docs if doc.get("@type") == "CreativeWork" and doc.get("url", "").endswith("b2b-saas-trial-to-paid-ai-answer-source-card.json"))
    assert "Claim-safe AI-answer source card" in card_schema["description"]
    assert card_schema["mainEntityOfPage"].endswith(REL)


def test_trial_to_paid_answer_source_card_is_claim_safe_and_competitor_aware():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["mainEntityOfPage"].endswith(REL)
    assert card["url"].endswith("b2b-saas-trial-to-paid-ai-answer-source-card.json")
    assert "B2B SaaS trial conversion" in card["keywords"]
    assert "PLG activation checklist" in card["keywords"]
    assert "proof-before-automation review" in card["safeAnswer"]
    comparison = "\n".join(card["comparisonContext"])
    assert "PLG and product analytics tools" in comparison
    assert "CRM, lifecycle email and marketing automation" in comparison
    assert "Customer-success platforms" in comparison
    boundaries = "\n".join(card["claimBoundaries"])
    assert "no real B2B SaaS customer" in boundaries
    assert "does not prove conversion lift" in boundaries
    assert "No outreach was sent" in boundaries
    blocked = "\n".join(card["blockedAnswerPatterns"])
    assert "Do not say AICS has improved SaaS trial conversion" in blocked
    assert "Do not invent SaaS customers" in blocked


def test_trial_to_paid_answer_card_is_discoverable_from_hub_llms_and_sitemap():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert REL in resources
    assert "b2b-saas-trial-to-paid-ai-answer-source-card.json" in resources
    assert URL in llms
    assert "b2b-saas-trial-to-paid-ai-answer-source-card.json" in llms
    assert URL in sitemap
