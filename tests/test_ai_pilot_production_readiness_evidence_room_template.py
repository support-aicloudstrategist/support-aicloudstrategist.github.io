from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ai-pilot-production-readiness-evidence-room-template" / "index.html"
CSV = ROOT / "resources" / "global-ai-pilot-production-readiness-evidence-room-template" / "evidence-room-index.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ai_pilot_evidence_room_page_has_search_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "AI pilot production readiness evidence room template",
        "AI pilot production readiness evidence room",
        "AI pilot evidence room template",
        "AI pilot go no go evidence",
        "AI production readiness checklist",
        "AI pilot risk evidence",
        "AI pilot owner handoff",
        "not a real client case study",
        "not ROI proof",
        "not a guarantee",
        "No outreach was sent",
        "evidence-room-index.csv",
        "FAQPage",
    ]
    for marker in required:
        assert marker in html


def test_ai_pilot_evidence_room_csv_template_is_downloadable_and_complete():
    csv = CSV.read_text(encoding="utf-8")
    assert csv.startswith("folder,evidence_check,document_or_link,status,owner,reviewer,claim_boundary_note")
    for folder in [
        "01-business-problem-baseline",
        "02-pilot-result-and-limits",
        "03-quality-evaluation",
        "04-data-security-boundary",
        "05-economics-and-scale-cost",
        "06-operations-handoff",
        "07-decision-record",
    ]:
        assert folder in csv
    assert csv.count("\n") >= 21


def test_ai_pilot_evidence_room_is_discoverable_from_public_indexes():
    slug = "/resources/global-ai-pilot-production-readiness-evidence-room-template/"
    canonical = "https://aicloudstrategist.com/resources/global-ai-pilot-production-readiness-evidence-room-template/"
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert canonical in LLMS.read_text(encoding="utf-8")
    assert canonical in SITEMAP.read_text(encoding="utf-8")
