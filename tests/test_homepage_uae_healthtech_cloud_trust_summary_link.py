from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
SUMMARY = ROOT / "resources" / "uae-healthtech-cloud-trust-executive-summary" / "index.html"


def test_homepage_surfaces_uae_healthtech_cloud_trust_summary():
    html = HOME.read_text(encoding="utf-8")
    assert 'data-homepage-resource="uae-healthtech-cloud-trust-executive-summary"' in html
    assert "/resources/uae-healthtech-cloud-trust-executive-summary/" in html
    assert "UAE Healthtech Cloud Trust + Patient GrowthOS Executive Summary" in html
    assert "no-patient-data route for UAE clinics, telehealth and healthtech teams" in html
    assert "patient-data boundaries, cloud/AI spend, questionnaire evidence and owner handoff" in html
    assert "Open the UAE healthtech cloud trust summary" in html


def test_uae_healthtech_cloud_trust_summary_exists_and_is_buyer_safe():
    assert SUMMARY.exists()
    summary_html = SUMMARY.read_text(encoding="utf-8")
    for phrase in [
        "UAE Healthtech Cloud Trust Executive Summary",
        "patient-data risk",
        "not legal/privacy/security/clinical/medical/diagnostic/billing/procurement/audit advice",
        "not ranking evidence",
        "not demand evidence",
    ]:
        assert phrase in summary_html
