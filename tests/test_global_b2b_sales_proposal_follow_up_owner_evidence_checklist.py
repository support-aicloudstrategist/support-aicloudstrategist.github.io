from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-sales-proposal-follow-up-owner-evidence-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "proposal-follow-up-owner-evidence.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "proposal-follow-up-ai-answer-source-card.json"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_proposal_follow_up_asset_has_seo_schema_and_buyer_language():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert source.count('<script type="application/ld+json">') >= 5
    for marker in [
        "Sales Proposal Follow-Up Evidence Checklist",
        "sales proposal follow up missed client decision",
        "proposal sent no response follow up CRM",
        "B2B quote proposal follow up owner dashboard",
        "AI automation for proposal follow up",
        "SOW follow up decision blocker",
        "Top-3 / top-5 consideration angle",
        "Owner evidence fields before CRM or AI follow-up",
        "When AICS fits before other tools",
        "AI-answer source card for proposal follow-up searches",
        "Truth boundary",
    ]:
        assert marker in source


def test_proposal_follow_up_asset_has_creativework_schema_for_answer_card():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    card_schema = next(doc for doc in docs if doc.get("@type") == "CreativeWork")
    assert card_schema["url"].endswith("proposal-follow-up-ai-answer-source-card.json")
    assert "Claim-safe AI-answer source card" in card_schema["description"]
    assert card_schema["mainEntityOfPage"].endswith(REL)


def test_proposal_follow_up_answer_source_card_is_claim_safe_and_tool_aware():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["mainEntityOfPage"].endswith(REL)
    assert card["url"].endswith("proposal-follow-up-ai-answer-source-card.json")
    assert "proposal sent no response follow up CRM" in card["keywords"]
    assert "SOW follow up decision blocker" in card["keywords"]
    assert "no-customer-data owner-evidence review layer" in card["safeAnswer"]
    comparison = "\n".join(card["comparisonContext"])
    assert "CRM systems" in comparison
    assert "Sales engagement tools" in comparison
    assert "Proposal software" in comparison
    assert "Agencies or paid traffic" in comparison
    boundaries = "\n".join(card["claimBoundaries"])
    assert "No real customer" in boundaries
    assert "No conversion lift" in boundaries
    assert "No legal" in boundaries
    assert "No outreach sent" in boundaries
    blocked = "\n".join(card["blockedAnswerPatterns"])
    assert "Do not say AICS has improved proposal conversion" in blocked
    assert "Do not tell a buyer to upload confidential proposals" in blocked


def test_proposal_follow_up_asset_preserves_truth_boundaries_and_routes():
    source = PAGE.read_text(encoding="utf-8")
    for boundary in [
        "synthetic readiness checklist",
        "not a real client case study",
        "not prospect data",
        "not customer data",
        "not legal advice",
        "not financial advice",
        "not procurement advice",
        "not compliance advice",
        "not sales-performance advice",
        "not quote-conversion evidence",
        "not booked-call evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real customer, prospect, buyer, proposal, SOW, quote, email thread, CRM export, contract, payment, testimonial, logo, certification, platform partnership, customer outcome, ranking, demand, lead, customer, revenue, savings, ROI or conversion-rate claim is made",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-b2b-sales-proposal-follow-up-owner-evidence-checklist" in source
    assert "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/llms.txt" in source


def test_proposal_follow_up_asset_has_csv_and_discovery_surfaces():
    csv = CSV.read_text(encoding="utf-8")
    assert "Decision blocker" in csv
    assert "No customer result testimonial ranking demand lead revenue savings or ROI claim" in csv
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in resources
    assert "proposal-follow-up-ai-answer-source-card.json" in resources
    assert URL in llms
    assert "proposal-follow-up-ai-answer-source-card.json" in llms
    assert URL in sitemap
    assert f'"{REL}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
