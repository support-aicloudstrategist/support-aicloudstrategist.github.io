from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "uk-care-home-family-enquiry-follow-up-evidence-checklist" / "index.html"
REL = "/resources/uk-care-home-family-enquiry-follow-up-evidence-checklist/"
URL = "https://aicloudstrategist.com/resources/uk-care-home-family-enquiry-follow-up-evidence-checklist/"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_uk_care_home_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "UK Care Home Family Enquiry Follow-Up Evidence Checklist",
        "care home missed calls family enquiry follow up",
        "care home CRM family enquiries UK",
        "care home tour booking follow up checklist",
        "AI receptionist for care homes UK",
        "CQC evidence family communication care home",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "family consent and channel evidence",
        "CQC-style evidence prompts",
        "Owner dashboard rows",
        "Truth boundary",
    ]:
        assert marker in source


def test_uk_care_home_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real UK care home case study",
        "not resident data",
        "not family data",
        "not care-plan data",
        "not medical advice",
        "not safeguarding advice",
        "not legal advice",
        "not privacy advice",
        "not CQC compliance advice",
        "not marketing-performance advice",
        "not admissions-growth evidence",
        "not response-time evidence",
        "not revenue evidence",
        "not occupancy evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real care home, care group, resident, family member, staff member, referral partner, local authority, NHS trust, call recording, care record, testimonial, logo, certification, accreditation, platform partnership or customer outcome is claimed",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=uk-care-home-family-enquiry-follow-up-evidence-checklist" in source
    assert "/resources/global-home-care-referral-intake-caregiver-scheduling-evidence-checklist/" in source
    assert "/case-studies/simulated-india-home-health-elder-care-referral-dpdp-diagnostic/" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/llms.txt" in source


def test_uk_care_home_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
