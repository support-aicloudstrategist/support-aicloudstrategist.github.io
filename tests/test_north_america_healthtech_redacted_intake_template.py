from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-healthtech-redacted-cloud-ai-intake-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "redacted-cloud-ai-intake-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}redacted-cloud-ai-intake-template.csv"


def test_north_america_healthtech_redacted_intake_template_page_and_csv():
    html = PAGE.read_text(encoding="utf-8")
    csv_text = CSV.read_text(encoding="utf-8")
    assert "Redacted cloud + AI intake template for healthtech trust reviews" in html
    assert "Download CSV template" in html
    assert CSV_URL in html
    assert "healthtech cloud cost optimization" in html
    assert "HIPAA security questionnaire evidence" in html
    assert "no PHI/ePHI" in html
    assert "not HIPAA compliance proof" in html
    assert "No customer outreach was sent" in html
    assert URL in html
    assert "intake_id,evidence_lane,region_scope" in csv_text
    assert "NAHT-001,cloud_ai_spend" in csv_text
    assert "NAHT-004,ai_workflow_boundary" in csv_text
    assert "credentials; tokens" in csv_text
    assert "PHI/ePHI" in csv_text
    assert "no savings/ROI/runway claim" in csv_text


def test_north_america_healthtech_redacted_intake_discovery_links():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    policy = (ROOT / "resources" / "north-america-healthtech-cloud-trust-finops-no-credentials-intake-policy" / "index.html").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert CSV_URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
    assert URL in sitemap
    assert f"/resources/{SLUG}/" in policy
    assert "redacted cloud + AI intake template" in policy
