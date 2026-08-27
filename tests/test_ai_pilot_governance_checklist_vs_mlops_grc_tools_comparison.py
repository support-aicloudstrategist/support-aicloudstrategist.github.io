from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-governance-checklist-vs-mlops-grc-tools-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_governance_comparison_page_exists_and_has_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot governance checklist vs MLOps and GRC tools" in html
    assert "Buyer comparison matrix" in html
    assert "Checklist governance" in html
    assert "MLOps / evaluation tools" in html
    assert "GRC tools" in html
    assert "Assurance-led review" in html
    assert "not a vendor ranking" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_governance_comparison_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert "/resources/global-ai-pilot-board-risk-register-review-diagnostic-package/" in html
    assert "/resources/global-ai-pilot-readiness-intake-questionnaire/" in html
    assert "/resources/global-ai-pilot-external-claim-approval-log-template/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
