from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-home-care-referral-intake-caregiver-scheduling-evidence-checklist" / "index.html"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_home_care_asset_has_public_seo_and_schema_markers():
    html = source()
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/global-home-care-referral-intake-caregiver-scheduling-evidence-checklist/"' in html
    assert '<meta name="robots" content="index, follow"' in html
    assert len(re.findall(r'<script type="application/ld\+json">', html)) >= 4
    assert html.count("<h1>") == 1
    for marker in [
        "home care agency missed calls referral intake software",
        "home health referral tracking",
        "caregiver scheduling exception queue",
        "family enquiry follow-up",
        "start-of-care intake checklist",
        "Truth boundary",
    ]:
        assert marker in html


def test_home_care_asset_has_truth_boundaries_and_conversion_route():
    html = source()
    for boundary in [
        "No real home-care agency",
        "customer data",
        "testimonial",
        "revenue, ROI",
        "AI-accuracy claim",
        "no legal, medical, clinical, privacy, security, billing, reimbursement, labour, staffing or compliance advice",
    ]:
        assert boundary in html
    assert "/free-business-review/?package=home-care-referral-intake-caregiver-scheduling" in html
    assert "/resources/" in html
    assert "/llms.txt" in html


def test_home_care_asset_is_linked_from_discovery_surfaces():
    rel = "/resources/global-home-care-referral-intake-caregiver-scheduling-evidence-checklist/"
    assert rel in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in (ROOT / "llms.txt").read_text(encoding="utf-8")
