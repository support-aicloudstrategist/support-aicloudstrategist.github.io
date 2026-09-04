from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-nis2-cloud-incident-supplier-evidence-checklist"
RESOURCE = ROOT / "resources" / SLUG / "index.html"
DASHBOARD = ROOT / "resources" / SLUG / "europe-healthtech-nis2-incident-owner-dashboard.svg"
LLMS = ROOT / "llms.txt"


def test_europe_healthtech_nis2_page_links_synthetic_owner_dashboard():
    html = RESOURCE.read_text(encoding="utf-8")
    dashboard_href = f"/resources/{SLUG}/europe-healthtech-nis2-incident-owner-dashboard.svg"

    assert dashboard_href in html
    assert "View synthetic owner dashboard" in html
    assert "incident row, data boundary, supplier owner, FinOps impact" in html
    assert "without importing patient, personal, health, production or customer data" in html


def test_europe_healthtech_nis2_dashboard_is_valid_synthetic_svg():
    svg = DASHBOARD.read_text(encoding="utf-8")
    ET.fromstring(svg)

    for required in [
        "Synthetic Europe healthtech NIS2 incident owner dashboard",
        "No PHI / PII import",
        "DPO + counsel",
        "No compliance proof",
        "not legal, compliance, security, clinical, incident-reporting, ROI, savings or customer evidence",
    ]:
        assert required in svg


def test_llms_exposes_europe_healthtech_nis2_dashboard_asset():
    llms = LLMS.read_text(encoding="utf-8")
    assert f"https://aicloudstrategist.com/resources/{SLUG}/europe-healthtech-nis2-incident-owner-dashboard.svg" in llms
