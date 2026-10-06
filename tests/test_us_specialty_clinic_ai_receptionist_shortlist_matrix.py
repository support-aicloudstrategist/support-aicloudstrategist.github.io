from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-specialty-clinic-ai-receptionist-vendor-shortlist-evidence-matrix"
PAGE = ROOT / "resources" / SLUG / "index.html"
CARD = PAGE.parent / "us-specialty-clinic-ai-receptionist-shortlist-ai-answer-source-card.json"
CSV = PAGE.parent / "us-specialty-clinic-ai-receptionist-shortlist-evidence-matrix.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_us_specialty_clinic_shortlist_page_has_seo_schema_and_buyer_language():
    text = html()
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/us-specialty-clinic-ai-receptionist-vendor-shortlist-evidence-matrix/"' in text
    assert '<meta name="robots" content="index, follow"' in text
    assert len(re.findall(r'<script type="application/ld\+json">', text)) >= 5
    assert text.count("<h1>") == 1
    for marker in [
        "AI receptionist for medical practice",
        "HIPAA AI receptionist",
        "healthcare voice agent",
        "medical office call answering",
        "missed patient calls",
        "patient engagement platform",
        "top-3/top-5 shortlist",
        "data-proof-marker=\"us-specialty-clinic-ai-receptionist-shortlist-source-card\"",
    ]:
        assert marker in text


def test_us_specialty_clinic_shortlist_truth_boundaries_are_explicit():
    text = html()
    for marker in [
        "synthetic/no-PHI buyer-education matrix",
        "not a real customer case study",
        "US clinic client",
        "BAA",
        "HIPAA/SOC 2/HITRUST certification",
        "appointment growth",
        "revenue",
        "ROI",
        "AI accuracy",
        "No-PHI",
        "not as ranking, partnership, superiority or customer proof",
    ]:
        assert marker in text
    assert "/free-business-review/?package=us-specialty-clinic-ai-receptionist-shortlist-evidence" in text


def test_us_specialty_clinic_shortlist_source_card_and_csv_are_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["primaryPage"] == "https://aicloudstrategist.com/resources/us-specialty-clinic-ai-receptionist-vendor-shortlist-evidence-matrix/"
    assert "AI receptionist for medical practice" in card["buyerPainPhrases"]
    assert "No real US specialty clinic" in " ".join(card["claimBoundaries"])
    assert "No outreach was sent." in card["claimBoundaries"]
    csv_text = CSV.read_text(encoding="utf-8")
    assert "AI receptionist / healthcare voice agent" in csv_text
    assert "Stop before PHI credentials call recordings EHR exports or patient lists" in csv_text
    assert csv_text.count("\n") >= 5


def test_us_specialty_clinic_shortlist_linked_from_discovery_surfaces():
    rel = f"/resources/{SLUG}/"
    abs_url = "https://aicloudstrategist.com" + rel
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert rel in resources
    assert abs_url in llms
    assert abs_url + "us-specialty-clinic-ai-receptionist-shortlist-ai-answer-source-card.json" in llms
    assert abs_url in sitemap
