from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-clinic-after-hours-missed-call-follow-up-checklist" / "index.html"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_clinic_after_hours_asset_has_public_seo_and_schema_markers():
    html = source()
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/global-clinic-after-hours-missed-call-follow-up-checklist/"' in html
    assert '<meta name="robots" content="index, follow"' in html
    assert len(re.findall(r'<script type="application/ld\+json">', html)) >= 4
    assert html.count("<h1>") == 1
    for marker in [
        "clinic after hours missed calls patient appointment follow up",
        "medical clinic missed calls after hours appointment scheduling",
        "private clinic missed patient calls AI receptionist",
        "patient appointment callback evidence",
        "clinic reception handoff owner dashboard",
        "Truth boundary",
    ]:
        assert marker in html


def test_clinic_after_hours_asset_has_truth_boundaries_and_conversion_route():
    html = source()
    for boundary in [
        "No real clinic",
        "patient, PHI",
        "customer data",
        "testimonial",
        "revenue, ROI",
        "AI-accuracy claim",
        "no medical, clinical, legal, privacy, security, insurance or compliance advice",
    ]:
        assert boundary in html
    assert "/free-business-review/?package=clinic-after-hours-missed-call-evidence" in html
    assert "/resources/" in html
    assert "/llms.txt" in html


def test_clinic_after_hours_asset_is_linked_from_discovery_surfaces():
    rel = "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/"
    assert rel in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert rel in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
