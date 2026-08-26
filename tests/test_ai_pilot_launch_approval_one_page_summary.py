from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ai-pilot-launch-approval-one-page-summary" / "index.html"
TEMPLATE = ROOT / "resources" / "global-ai-pilot-launch-approval-one-page-summary" / "ai-pilot-launch-approval-one-page-summary.md"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ai_pilot_launch_approval_summary_has_search_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "AI pilot launch approval one-page summary",
        "AI pilot launch approval summary",
        "AI pilot board approval template",
        "AI pilot executive decision one pager",
        "AI pilot production approval memo",
        "AI pilot go no go board pack",
        "not a real client case study",
        "not a guarantee",
        "No outreach was sent",
        "FAQPage",
        "ai-pilot-launch-approval-one-page-summary.md",
    ]
    for marker in required:
        assert marker in html


def test_ai_pilot_launch_approval_markdown_template_is_downloadable_and_complete():
    text = TEMPLATE.read_text(encoding="utf-8")
    required = [
        "# AI Pilot Launch Approval One-Page Summary",
        "## 1. Decision ask",
        "## 2. Evidence confidence",
        "## 3. Open risks and restricted-launch boundaries",
        "## 4. Cost and scale economics",
        "## 5. Operating controls",
        "## 6. Safe claim boundary",
        "Sign-off table",
        "Forbidden claims until further proof",
        "not a real client case study",
    ]
    for marker in required:
        assert marker in text


def test_ai_pilot_launch_approval_summary_cross_links_evidence_chain():
    html = PAGE.read_text(encoding="utf-8")
    for slug in [
        "/resources/global-ai-pilot-proof-of-value-scorecard/",
        "/resources/global-ai-pilot-production-readiness-evidence-room-template/",
        "/resources/global-ai-pilot-production-go-no-go-decision-record-template/",
        "/resources/global-enterprise-ai-model-evaluation-regression-evidence-checklist/",
        "/resources/global-ai-pilot-tools-vs-assurance-led-review-comparison/",
        "/services/ai-mlops/",
    ]:
        assert slug in html


def test_ai_pilot_launch_approval_summary_is_discoverable_from_public_indexes():
    slug = "/resources/global-ai-pilot-launch-approval-one-page-summary/"
    canonical = "https://aicloudstrategist.com/resources/global-ai-pilot-launch-approval-one-page-summary/"
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert canonical in LLMS.read_text(encoding="utf-8")
    assert canonical in SITEMAP.read_text(encoding="utf-8")
