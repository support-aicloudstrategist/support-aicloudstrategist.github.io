from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ai-pilot-proof-of-value-scorecard" / "index.html"
CSV = ROOT / "resources" / "global-ai-pilot-proof-of-value-scorecard" / "scorecard-template.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ai_pilot_scorecard_page_has_buyer_search_and_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "AI pilot proof-of-value scorecard",
        "AI pilot proof of value",
        "AI pilot go no go checklist",
        "AI pilot production readiness",
        "AI pilot ROI evidence",
        "AI pilot risk review",
        "not a real client case study",
        "not ROI proof",
        "not a guarantee",
        "No outreach was sent",
        "scorecard-template.csv",
        "FAQPage",
    ]
    for marker in required:
        assert marker in html


def test_ai_pilot_scorecard_csv_template_is_downloadable_and_complete():
    csv = CSV.read_text(encoding="utf-8")
    assert csv.startswith("lane,check,green_evidence,score_status,owner,notes")
    for lane in [
        "Business value",
        "Quality and failure modes",
        "Data and security boundary",
        "Economics",
        "Operations",
        "Decision record",
    ]:
        assert lane in csv
    assert csv.count("\n") >= 18


def test_ai_pilot_scorecard_is_discoverable_from_public_indexes():
    slug = "/resources/global-ai-pilot-proof-of-value-scorecard/"
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/global-ai-pilot-proof-of-value-scorecard/" in LLMS.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/global-ai-pilot-proof-of-value-scorecard/" in SITEMAP.read_text(encoding="utf-8")
