import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "singapore-private-clinic-pdpa-patient-follow-up-evidence-checklist" / "index.html"
URL = "https://aicloudstrategist.com/resources/singapore-private-clinic-pdpa-patient-follow-up-evidence-checklist/"
REL = "/resources/singapore-private-clinic-pdpa-patient-follow-up-evidence-checklist/"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_singapore_clinic_asset_has_public_seo_and_schema_markers():
    html = source()
    assert f'<link rel="canonical" href="{URL}"' in html
    assert '<meta name="robots" content="index, follow"' in html
    assert len(re.findall(r'<script type="application/ld\+json">', html)) >= 4
    assert html.count("<h1>") == 1
    for marker in [
        "Singapore clinic missed calls",
        "private clinic appointment reminder Singapore",
        "patient engagement software Singapore",
        "WhatsApp appointment follow-up for clinics",
        "PDPA patient communication checklist",
        "AI receptionist for clinics Singapore",
    ]:
        assert marker in html


def test_singapore_clinic_asset_has_truth_boundaries_and_conversion_route():
    html = source()
    for boundary in [
        "No real Singapore clinic",
        "personal data",
        "client result",
        "testimonial",
        "revenue, ROI, ranking",
        "AI-accuracy claim",
        "not medical, clinical, legal, privacy, security, PDPA",
    ]:
        assert boundary in html
    assert "/free-business-review/?package=singapore-private-clinic-pdpa-patient-follow-up" in html
    assert "/healthcare-growthos/" in html
    assert "/llms.txt" in html


def test_singapore_clinic_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
