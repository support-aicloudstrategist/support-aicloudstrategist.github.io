from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-healthtech-ai-cloud-owner-dashboard-demo"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "north-america-healthtech-ai-cloud-owner-dashboard-demo.csv"
SVG = ROOT / "resources" / SLUG / "north-america-healthtech-ai-cloud-owner-dashboard-demo.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}north-america-healthtech-ai-cloud-owner-dashboard-demo.csv"
SVG_URL = f"{URL}north-america-healthtech-ai-cloud-owner-dashboard-demo.svg"


def test_north_america_healthtech_ai_cloud_owner_dashboard_demo_assets():
    html = PAGE.read_text(encoding="utf-8")
    csv_text = CSV.read_text(encoding="utf-8")
    svg_text = SVG.read_text(encoding="utf-8")
    assert "Healthtech AI + cloud owner dashboard demo" in html
    assert "healthtech cloud cost owner dashboard" in html
    assert "AI spend governance dashboard" in html
    assert "HIPAA questionnaire evidence ageing" in html
    assert "AI medical receptionist human review dashboard" in html
    assert "not HIPAA compliance proof" in html
    assert "No customer outreach was sent" in html
    assert CSV_URL in html
    assert SVG_URL in html
    assert "dashboard_id,queue_lane,evidence_signal" in csv_text
    assert "NAHT-DASH-001,cloud_ai_spend" in csv_text
    assert "NAHT-DASH-003,ai_medical_receptionist_human_review" in csv_text
    assert "no PHI/ePHI" in svg_text
    assert "No HIPAA proof" in svg_text


def test_north_america_healthtech_ai_cloud_owner_dashboard_discovery_links():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    policy = (ROOT / "resources" / "north-america-healthtech-cloud-trust-finops-no-credentials-intake-policy" / "index.html").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert CSV_URL in llms
    assert SVG_URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
    assert URL in sitemap
    assert f"/resources/{SLUG}/" in policy
    assert "synthetic owner dashboard" in policy
