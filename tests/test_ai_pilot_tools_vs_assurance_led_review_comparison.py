from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ai-pilot-tools-vs-assurance-led-review-comparison" / "index.html"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ai_pilot_tools_vs_assurance_page_has_search_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "AI pilot tools vs assurance-led review",
        "AI pilot tools vs assurance led review",
        "AI pilot production readiness review",
        "AI prototyping platform comparison",
        "MLOps dashboard vs readiness evidence",
        "AI pilot go no go review",
        "Neutral comparison",
        "Choose assurance-led review when",
        "not a vendor ranking",
        "not a real client case study",
        "not a guarantee",
        "No outreach was sent",
        "FAQPage",
    ]
    for marker in required:
        assert marker in html


def test_ai_pilot_tools_vs_assurance_page_cross_links_evidence_assets():
    html = PAGE.read_text(encoding="utf-8")
    assert "/resources/global-ai-pilot-production-readiness-evidence-room-template/" in html
    assert "/resources/global-ai-pilot-proof-of-value-scorecard/" in html
    assert "/services/ai-mlops/" in html


def test_ai_pilot_tools_vs_assurance_page_is_discoverable_from_public_indexes():
    slug = "/resources/global-ai-pilot-tools-vs-assurance-led-review-comparison/"
    canonical = "https://aicloudstrategist.com/resources/global-ai-pilot-tools-vs-assurance-led-review-comparison/"
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert canonical in LLMS.read_text(encoding="utf-8")
    assert canonical in SITEMAP.read_text(encoding="utf-8")
