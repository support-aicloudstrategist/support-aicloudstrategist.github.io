from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ai-pilot-production-go-no-go-decision-record-template" / "index.html"
CSV = ROOT / "resources" / "global-ai-pilot-production-go-no-go-decision-record-template" / "ai-pilot-go-no-go-decision-record.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ai_pilot_go_no_go_decision_record_has_search_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "AI pilot production go/no-go decision record template",
        "AI pilot go no go decision record template",
        "AI pilot production go no go template",
        "AI pilot decision record template",
        "AI pilot launch approval checklist",
        "AI pilot leadership decision pack",
        "not a real client case study",
        "not a guarantee",
        "No outreach was sent",
        "FAQPage",
        "ai-pilot-go-no-go-decision-record.csv",
    ]
    for marker in required:
        assert marker in html


def test_ai_pilot_go_no_go_csv_template_is_downloadable_and_complete():
    csv = CSV.read_text(encoding="utf-8")
    required = [
        "decision_lane,evidence_to_attach,named_owner,go_condition",
        "Business value",
        "Quality and regression",
        "Data and security boundary",
        "Cost and scale economics",
        "Operations handoff",
        "Safe external claims",
        "Final decision",
        "Do not claim ROI",
    ]
    for marker in required:
        assert marker in csv


def test_ai_pilot_go_no_go_decision_record_cross_links_prior_assets():
    html = PAGE.read_text(encoding="utf-8")
    for slug in [
        "/resources/global-ai-pilot-proof-of-value-scorecard/",
        "/resources/global-ai-pilot-production-readiness-evidence-room-template/",
        "/resources/global-ai-pilot-tools-vs-assurance-led-review-comparison/",
        "/resources/global-enterprise-ai-model-evaluation-regression-evidence-checklist/",
        "/services/ai-mlops/",
    ]:
        assert slug in html


def test_ai_pilot_go_no_go_decision_record_is_discoverable_from_public_indexes():
    slug = "/resources/global-ai-pilot-production-go-no-go-decision-record-template/"
    canonical = "https://aicloudstrategist.com/resources/global-ai-pilot-production-go-no-go-decision-record-template/"
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert canonical in LLMS.read_text(encoding="utf-8")
    assert canonical in SITEMAP.read_text(encoding="utf-8")
