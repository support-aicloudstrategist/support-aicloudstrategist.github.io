from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-model-evaluation-regression-drift-faq"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_model_evaluation_regression_drift_faq_page_exists_with_truth_boundary():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI Pilot Model Evaluation Regression and Drift FAQ" in html
    assert "what to check when answers regress after launch" in html
    assert "model accuracy drops" in html
    assert "retrieval quality drift" in html
    assert "Regression evidence map" in html
    assert "External claim status" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_model_evaluation_regression_drift_faq_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert "/resources/global-enterprise-ai-model-evaluation-regression-evidence-checklist/" in html
    assert "/resources/global-ai-pilot-rollback-readiness-checklist/" in html
    assert "/resources/global-ai-pilot-remediation-decision-log-template/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
