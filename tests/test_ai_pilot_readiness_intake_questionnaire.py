from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-readiness-intake-questionnaire"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-readiness-intake-questionnaire.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_readiness_intake_questionnaire_page_and_csv_exist():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert "AI pilot readiness intake questionnaire" in html
    assert "Download CSV questionnaire" in html
    assert "Executive intake questions" in html
    assert "External claims" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html
    assert "area,question,evidence_to_attach,owner,stop_or_escalate_signal" in csv
    assert "Rollback" in csv
    assert "External claims" in csv


def test_ai_pilot_readiness_intake_questionnaire_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert "/resources/global-ai-pilot-board-risk-register-review-diagnostic-package/" in html
    assert "/resources/global-ai-pilot-board-risk-register-demo-board-pack/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
