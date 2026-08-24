from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-law-firm-missed-call-client-intake-follow-up-checklist" / "index.html"
REL = "/resources/global-law-firm-missed-call-client-intake-follow-up-checklist/"
URL = "https://aicloudstrategist.com/resources/global-law-firm-missed-call-client-intake-follow-up-checklist/"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_law_firm_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "Law Firm Missed-Call + Client Intake Follow-Up Checklist",
        "law firm missed calls intake follow up checklist",
        "law firm client intake follow up CRM",
        "legal consultation no show follow up",
        "AI receptionist for law firm intake",
        "law firm answering service owner dashboard",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "Clio, Lawmatics, Lexicata/Clio Grow, CallRail, Smith.ai",
        "conflict-check gates",
        "Partner dashboard rows",
        "Truth boundary",
    ]:
        assert marker in source


def test_law_firm_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real law firm case study",
        "not attorney-client data",
        "not client data",
        "not legal advice",
        "not privacy advice",
        "not marketing-performance advice",
        "not compliance advice",
        "not client-growth evidence",
        "not faster-intake evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real law firm, lawyer, attorney, client, matter, case, consultation, call recording, intake form, referral source, testimonial, logo, certification, platform partnership or customer outcome is claimed",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-law-firm-missed-call-client-intake-follow-up-checklist" in source
    assert "/resources/us-law-firm-ai-intake-answering-service-faq/" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_law_firm_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
