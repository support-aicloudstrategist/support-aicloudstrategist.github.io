from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-external-claim-approval-log-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-external-claim-approval-log-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_external_claim_approval_log_page_and_csv_exist():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert "AI pilot external claim approval log template" in html
    assert "Download CSV template" in html
    assert "Approval log fields" in html
    assert "ROI, safety, accuracy, compliance" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html
    assert "claim_id,claim_text,claim_category,intended_channel,evidence_source" in csv
    assert "Production-ready claim without rollback" in csv
    assert "Compliant/certified language without formal adviser approval" in csv


def test_ai_pilot_external_claim_approval_log_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert "/resources/global-ai-pilot-readiness-intake-questionnaire/" in html
    assert "/resources/global-ai-pilot-board-risk-register-review-diagnostic-package/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
