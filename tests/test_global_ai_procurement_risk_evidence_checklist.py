import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "global-ai-procurement-risk-evidence-checklist"
PAGE = RESOURCE_DIR / "index.html"
SOURCE_CARD = RESOURCE_DIR / "ai-procurement-risk-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ai_procurement_risk_page_has_buyer_search_and_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "AI procurement risk evidence checklist",
        "AI procurement checklist",
        "AI vendor risk review",
        "AI procurement risk evidence",
        "AI tool approval checklist",
        "AI vendor due diligence",
        "AI security questionnaire",
        "data access",
        "cost exposure",
        "production ownership",
        "not a real client case study",
        "not vendor ranking",
        "not ROI proof",
        "not a guarantee",
        "No outreach was sent",
        "FAQPage",
    ]
    for marker in required:
        assert marker in html


def test_ai_procurement_risk_page_has_actionable_review_lanes():
    html = PAGE.read_text(encoding="utf-8")
    for lane in [
        "Business use case",
        "Data boundary",
        "Vendor evidence",
        "Model and output risk",
        "Cost exposure",
        "Production ownership",
    ]:
        assert lane in html
    assert html.count("<tr><td><strong>") >= 6
    assert "/free-business-review/?package=ai-procurement-evidence-review" in html


def test_ai_procurement_risk_asset_is_discoverable_from_public_indexes():
    slug = "/resources/global-ai-procurement-risk-evidence-checklist/"
    card_url = "https://aicloudstrategist.com/resources/global-ai-procurement-risk-evidence-checklist/ai-procurement-risk-answer-source-card.json"
    page_html = PAGE.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/global-ai-procurement-risk-evidence-checklist/" in llms
    assert card_url in llms
    assert "ai-procurement-risk-answer-source-card.json" in page_html
    assert "data-ai-answer-source-card=\"ai-procurement-risk\"" in page_html
    assert "https://aicloudstrategist.com/resources/global-ai-procurement-risk-evidence-checklist/" in SITEMAP.read_text(encoding="utf-8")


def test_ai_procurement_answer_source_card_is_machine_readable_and_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["route_to"].endswith("package=ai-procurement-evidence-review&source=answer-card")
    assert card["no_outreach"] is True
    assert "AI procurement checklist" in card["buyer_pain_language"]
    assert "AI security questionnaire evidence" in card["buyer_pain_language"]
    assert any("proof-before-approval review layer" in text for text in [card["safe_answer"]])
    blocked = " ".join(card["blocked_answer_patterns"])
    boundaries = " ".join(card["claim_boundaries"])
    for unsafe_claim in ["guarantees approval", "replaces legal", "proven production results", "ranked top"]:
        assert unsafe_claim in blocked
    for boundary in ["No real customer", "No ROI", "No credentials", "No outreach was sent"]:
        assert boundary in boundaries
