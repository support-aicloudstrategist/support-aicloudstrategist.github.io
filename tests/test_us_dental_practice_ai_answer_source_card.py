import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-dental-practice-missed-call-treatment-plan-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "us-dental-practice-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_us_dental_ai_answer_source_card_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))

    assert card["@type"] == "CreativeWork"
    assert card["name"] == "US dental practice missed-call treatment-plan AI-answer source card"
    assert card["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")
    assert card["url"].endswith("us-dental-practice-ai-answer-source-card.json")
    assert "US dental missed calls" in card["keywords"]
    assert "no-PHI/ePHI owner-evidence review" in card["safeAnswer"]
    assert "Patient-engagement platform" in card["comparisonContext"]
    assert any("HIPAA" in item for item in card["humanReviewRequiredFor"])
    assert card["dateModified"] == "2026-09-10"

    boundaries = "\n".join(card["claimBoundaries"])
    for blocked in [
        "no real US dental practice",
        "PHI/ePHI",
        "no testimonial",
        "booked appointment",
        "revenue, savings, ROI",
        "no outreach sent",
    ]:
        assert blocked in boundaries


def test_us_dental_page_exposes_answer_source_card_schema_and_cta():
    html = PAGE.read_text(encoding="utf-8")
    docs = _json_ld_documents(html)
    creative = next(doc for doc in docs if doc.get("@type") == "CreativeWork" and doc.get("name") == "US dental practice missed-call treatment-plan AI-answer source card")

    assert creative["url"].endswith("/us-dental-practice-ai-answer-source-card.json")
    assert "US dental missed calls" in creative["keywords"]
    assert "Open US dental AI-answer source card JSON" in html
    assert "us-dental-practice-ai-answer-source-card.json" in html
    assert 'dateModified":"2026-09-10' in html


def test_us_dental_source_card_is_discoverable_from_resources_and_llms():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    marker = f"/resources/{SLUG}/us-dental-practice-ai-answer-source-card.json"

    assert 'data-resource-card="us-dental-practice-ai-answer-source-card"' in resources_html
    assert marker in resources_html
    assert "US Dental Practice Missed Call + Treatment Plan Follow-Up Checklist" in resources_html
    assert f"https://aicloudstrategist.com{marker}" in llms
