from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-no-credentials-intake-policy"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_europe_healthtech_no_credentials_policy_exists_with_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "No-credentials intake policy for Cloud Trust + FinOps evidence-room reviews" in html
    assert "no cloud-console credentials" in html
    assert "no secrets" in html
    assert "not customer data" in html
    assert "not patient data" in html
    assert "not health data" in html
    assert "not GDPR/UK GDPR/EU AI Act/NHS DSPT compliance proof" in html
    assert "not SOC 2/ISO 27001/HITRUST certification proof" in html
    assert "No customer outreach was sent" in html
    assert URL in html


def test_europe_healthtech_no_credentials_policy_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    evidence_room = (ROOT / "resources" / "europe-healthtech-cloud-trust-finops-evidence-room" / "index.html").read_text(encoding="utf-8")
    assert "/resources/europe-healthtech-cloud-trust-finops-evidence-room/" in html
    assert "/resources/europe-saas-ai-security-questionnaire-evidence-gap-matrix/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
    assert URL in sitemap
    assert f"/resources/{SLUG}/" in evidence_room
    assert "no-credentials intake policy" in evidence_room
