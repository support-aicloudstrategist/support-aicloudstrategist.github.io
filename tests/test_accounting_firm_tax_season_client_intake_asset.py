from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-accounting-firm-tax-season-client-intake-follow-up-checklist" / "index.html"
REL = "/resources/global-accounting-firm-tax-season-client-intake-follow-up-checklist/"
URL = "https://aicloudstrategist.com/resources/global-accounting-firm-tax-season-client-intake-follow-up-checklist/"

def html() -> str:
    return PAGE.read_text(encoding="utf-8")

def test_accounting_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "Accounting Firm Tax Season Client Intake Follow-Up Checklist",
        "accounting firm missed calls",
        "tax season client intake follow up",
        "CPA firm client onboarding workflow",
        "document collection chasing",
        "client portal invite queue",
        "accounting practice owner dashboard",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "TaxDome, Karbon, Canopy, Thomson Reuters",
        "Truth boundary",
    ]:
        assert marker in source

def test_accounting_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real accounting firm case study",
        "not a real CPA firm case study",
        "not taxpayer data",
        "not client data",
        "not tax advice",
        "not accounting advice",
        "not legal advice",
        "not privacy advice",
        "not client-growth evidence",
        "not faster-filing evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real accounting firm, CPA firm, bookkeeper, taxpayer, client, customer, logo, certification or customer outcome is claimed",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-accounting-firm-tax-season-client-intake-follow-up-checklist" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/resources/" in source
    assert "/llms.txt" in source

def test_accounting_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
