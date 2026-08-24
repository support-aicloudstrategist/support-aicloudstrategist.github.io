from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-insurance-agency-quote-claims-follow-up-checklist" / "index.html"
REL = "/resources/global-insurance-agency-quote-claims-follow-up-checklist/"
URL = "https://aicloudstrategist.com/resources/global-insurance-agency-quote-claims-follow-up-checklist/"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_insurance_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "Insurance Agency Quote + Claims Follow-Up Evidence Checklist",
        "insurance agency missed calls lead follow up CRM",
        "insurance agency quote follow up checklist",
        "insurance broker claims follow up owner dashboard",
        "AI receptionist for insurance agency",
        "agency management system follow up evidence",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "AgencyBloc, EZLynx, Applied Systems, Vertafore, HawkSoft, QQCatalyst",
        "Claims and service handoff",
        "Agency owner dashboard rows",
        "Truth boundary",
    ]:
        assert marker in source


def test_insurance_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real insurance agency case study",
        "not policyholder data",
        "not prospect data",
        "not claims data",
        "not carrier data",
        "not legal advice",
        "not insurance advice",
        "not coverage advice",
        "not financial advice",
        "not privacy advice",
        "not compliance advice",
        "not marketing-performance advice",
        "not quote-conversion evidence",
        "not retention evidence",
        "not claims-speed evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real insurance agency, broker, producer, account manager, CSR, carrier, policyholder, claimant, quote, policy, claim file, call recording, customer data, testimonial, logo, certification, regulator approval, carrier appointment, platform partnership or customer outcome is claimed",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-insurance-agency-quote-claims-follow-up-checklist" in source
    assert "/resources/global-accounting-firm-tax-season-client-intake-follow-up-checklist/" in source
    assert "/resources/global-law-firm-missed-call-client-intake-follow-up-checklist/" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/llms.txt" in source


def test_insurance_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
