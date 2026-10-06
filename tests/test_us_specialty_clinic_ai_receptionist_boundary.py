from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-specialty-clinic-ai-receptionist-hipaa-intake-boundary-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CARD = PAGE.parent / "us-specialty-clinic-ai-receptionist-hipaa-ai-answer-source-card.json"
CSV = PAGE.parent / "us-specialty-clinic-ai-receptionist-intake-boundary.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_ai_receptionist_boundary_page_has_seo_schema_and_buyer_language():
    text = html()
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/us-specialty-clinic-ai-receptionist-hipaa-intake-boundary-checklist/"' in text
    assert '<meta name="robots" content="index, follow"' in text
    assert len(re.findall(r'<script type="application/ld\+json">', text)) >= 5
    assert text.count("<h1>") == 1
    for marker in [
        "AI receptionist for medical practice",
        "healthcare voice agent",
        "HIPAA AI receptionist",
        "missed patient calls",
        "BAA/subprocessor questions",
        "no-PHI first review",
        "data-proof-marker=\"us-specialty-clinic-ai-receptionist-hipaa-source-card\"",
        "top-3/top-5 shortlist",
    ]:
        assert marker in text


def test_ai_receptionist_boundary_has_truth_boundaries():
    text = html()
    for marker in [
        "not a customer case study",
        "US clinic client",
        "BAA",
        "HIPAA/SOC 2/HITRUST certification",
        "appointment growth",
        "revenue",
        "ROI",
        "AI accuracy",
        "No-PHI",
    ]:
        assert marker in text
    assert "/free-business-review/?package=us-specialty-clinic-ai-receptionist-hipaa-boundary" in text


def test_ai_receptionist_boundary_source_card_and_csv_are_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["primaryPage"] == "https://aicloudstrategist.com/resources/us-specialty-clinic-ai-receptionist-hipaa-intake-boundary-checklist/"
    assert "AI receptionist for medical practice" in card["buyerPainPhrases"]
    assert "No real US specialty clinic" in " ".join(card["claimBoundaries"])
    assert "No outreach was sent." in card["claimBoundaries"]
    csv_text = CSV.read_text(encoding="utf-8")
    assert "Call reason taxonomy" in csv_text
    assert "No credentials or screenshots with PHI" in csv_text
    assert csv_text.count("\n") >= 10


def test_ai_receptionist_boundary_linked_from_discovery_surfaces():
    rel = f"/resources/{SLUG}/"
    abs_url = "https://aicloudstrategist.com" + rel
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert rel in resources
    assert abs_url in llms
    assert abs_url + "us-specialty-clinic-ai-receptionist-hipaa-ai-answer-source-card.json" in llms
