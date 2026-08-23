from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "saudi-private-clinic-whatsapp-appointment-follow-up-checklist" / "index.html"
REL = "/resources/saudi-private-clinic-whatsapp-appointment-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_saudi_private_clinic_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "Saudi Private Clinic WhatsApp Appointment Follow-Up Checklist",
        "Saudi clinic missed calls",
        "WhatsApp patient follow-up",
        "clinic no-show reminders",
        "PDPL adviser questions",
        "Patient GrowthOS owner dashboard",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "Truth boundary",
    ]:
        assert marker in source


def test_saudi_private_clinic_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real Saudi clinic case study",
        "not patient data",
        "not Saudi PDPL compliance proof",
        "not healthcare compliance proof",
        "not medical advice",
        "not legal advice",
        "not privacy advice",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real clinic, patient, client, logo, certification or customer outcome is claimed",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=saudi-private-clinic-whatsapp-appointment-follow-up-checklist" in source
    assert "/healthcare-growthos/" in source
    assert "/lead-leakage-calculator" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_saudi_private_clinic_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
