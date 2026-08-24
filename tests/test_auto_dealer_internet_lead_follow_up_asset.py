from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-auto-dealer-internet-lead-follow-up-checklist" / "index.html"
REL = "/resources/global-auto-dealer-internet-lead-follow-up-checklist/"
URL = "https://aicloudstrategist.com/resources/global-auto-dealer-internet-lead-follow-up-checklist/"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_auto_dealer_asset_has_public_seo_and_schema_markers():
    source = read(PAGE)
    assert "<title>Auto Dealer Internet Lead Follow-Up Evidence Checklist | AICloudStrategist</title>" in source
    assert f'<link rel="canonical" href="{URL}"/>' in source
    assert '<meta name="robots" content="index, follow"/>' in source
    assert '"@type":"WebPage"' in source
    assert '"@type":"FAQPage"' in source
    for phrase in [
        "auto dealer internet lead follow up checklist",
        "car dealership missed calls CRM follow up",
        "dealer BDC owner dashboard",
        "AI receptionist for car dealership",
        "test drive lead response SLA",
    ]:
        assert phrase in source


def test_auto_dealer_asset_has_truth_boundaries_and_conversion_route():
    source = read(PAGE)
    for phrase in [
        "not a real auto dealer case study",
        "not dealership data",
        "not finance data",
        "not credit data",
        "not OEM data",
        "not lender data",
        "not legal advice",
        "not financing advice",
        "not lead-conversion evidence",
        "not appointment-show evidence",
        "not revenue evidence",
        "not gross-profit evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real dealership, dealer group, OEM, lender, DMS, CRM, marketplace, salesperson, BDC rep, service adviser, customer, lead, call recording, testimonial, logo, certification, platform partnership or customer outcome is claimed",
    ]:
        assert phrase in source
    assert "/free-business-review/?package=global-auto-dealer-internet-lead-follow-up-checklist" in source
    assert "/resources/global-insurance-agency-quote-claims-follow-up-checklist/" in source
    assert "/resources/global-real-estate-property-viewing-follow-up-checklist/" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/llms.txt" in source


def test_auto_dealer_asset_is_linked_from_discovery_surfaces():
    assert REL in read(ROOT / "resources" / "index.html")
    assert URL in read(ROOT / "llms.txt")
    assert URL in read(ROOT / "sitemap.xml")
    assert REL in read(ROOT / "scripts" / "build_sitemap.py")
