from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/us-medical-group-ai-scribe-documentation-human-review-checklist/index.html"
CSV = ROOT / "resources/us-medical-group-ai-scribe-documentation-human-review-checklist/us-medical-group-ai-scribe-documentation-human-review-checklist.csv"
SVG = ROOT / "resources/us-medical-group-ai-scribe-documentation-human-review-checklist/ai-scribe-review-owner-map.svg"
RESOURCES = ROOT / "resources/index.html"
LLMS = ROOT / "llms.txt"
SITEMAP_SCRIPT = ROOT / "scripts/build_sitemap.py"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ai_scribe_page_has_core_buyer_language_and_structured_data():
    html = text(PAGE)
    assert "US Medical Group AI Scribe Human Review Checklist" in html
    assert "ambient clinical documentation" in html
    assert "physician documentation burden" in html
    assert "AI scribe HIPAA vendor risk" in html
    assert "clinical note quality review" in html
    assert "patient consent ambient listening" in html
    assert "AI scribe cost ownership" in html
    assert '"@type":"Article"' in html
    assert '"@type":"Dataset"' in html
    assert '"@type":"ImageObject"' in html
    assert '"@type":"FAQPage"' in html


def test_ai_scribe_artifacts_are_synthetic_no_phi_and_linked():
    html = text(PAGE)
    csv = text(CSV)
    svg = text(SVG)
    assert "synthetic buyer-education checklist and demo owner map only" in html
    assert "not PHI/ePHI" in html
    assert "No customer outreach was sent" in html
    assert "us-medical-group-ai-scribe-documentation-human-review-checklist.csv" in html
    assert "ai-scribe-review-owner-map.svg" in html
    assert "no_phi_evidence_to_prepare" in csv
    assert "unsafe_claim_blocked" in csv
    assert "No charting-time reduction or physician-burnout improvement claim" in csv
    assert "Synthetic/no-PHI illustration" in svg


def test_ai_scribe_resource_discovery_routes():
    route = "/resources/us-medical-group-ai-scribe-documentation-human-review-checklist/"
    assert route in text(RESOURCES)
    assert route in text(LLMS)
    assert route in text(SITEMAP_SCRIPT)
    assert "AI scribe documentation human-review checklist" in text(LLMS)


def test_ai_scribe_claim_boundaries_are_explicit():
    html = text(PAGE).lower()
    blocked = [
        "not documentation-time reduction evidence",
        "not burnout reduction evidence",
        "not note-accuracy evidence",
        "not savings evidence",
        "not roi evidence",
        "not ranking evidence",
        "not demand evidence",
        "not lead evidence",
        "not revenue evidence",
    ]
    for phrase in blocked:
        assert phrase in html
    assert "does this prove aics ranks top 3 or top 5" in html
