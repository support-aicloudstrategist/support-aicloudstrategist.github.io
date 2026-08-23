from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "clinic-website-not-converting-patients-checklist" / "index.html"
REL = "/resources/clinic-website-not-converting-patients-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_clinic_website_conversion_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "clinic website not converting patients",
        "healthcare website not getting appointments",
        "clinic website enquiries not converting",
        "clinic form leads not followed up",
        "Google Business Profile clinic calls missed",
        "Truth boundary",
        "Top-3/top-5 consideration signals",
    ]:
        assert marker in source


def test_clinic_website_conversion_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "No real clinic",
        "patient",
        "testimonial",
        "HIPAA compliance",
        "DPDP compliance",
        "GDPR compliance",
        "revenue, ROI",
        "ranking",
        "AI-accuracy claim",
        "no medical, legal, privacy, advertising, healthcare, DPDP, GDPR, HIPAA, security or compliance advice",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=clinic-website-conversion-review" in source
    assert "/healthcare-growthos/" in source
    assert "/lead-leakage-calculator" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_clinic_website_conversion_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
