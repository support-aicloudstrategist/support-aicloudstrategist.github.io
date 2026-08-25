from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-freight-forwarding-shipment-exception-follow-up-checklist" / "index.html"
REL = "/resources/global-freight-forwarding-shipment-exception-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_freight_forwarding_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "Freight Forwarding Shipment Exception Follow-Up Checklist",
        "freight forwarding shipment follow up software",
        "logistics company quote follow up freight enquiry CRM",
        "3PL warehouse shipment exception customer communication software",
        "shipment exception customer update proof",
        "freight forwarding owner dashboard",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "CargoWise, GoFreight, Magaya, Descartes",
        "Truth boundary",
    ]:
        assert marker in source


def test_freight_forwarding_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real logistics customer case study",
        "not operational advice",
        "not customs advice",
        "not legal advice",
        "not trade-compliance advice",
        "not production data",
        "not shipment data",
        "not customer data",
        "not delivery improvement evidence",
        "not clearance improvement evidence",
        "not savings evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real forwarder, 3PL, warehouse, shipper, consignee, carrier, broker, shipment",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-freight-forwarding-shipment-exception-follow-up-checklist" in source
    assert "/growth-control-os/" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_freight_forwarding_asset_has_demo_dashboard_visual():
    source = html()
    svg = PAGE.with_name("demo-dashboard.svg")
    visual = svg.read_text(encoding="utf-8")
    assert "demo-dashboard.svg" in source
    assert "Synthetic freight forwarding exception follow-up dashboard" in source
    for marker in [
        "Synthetic Freight Forwarding Exception Follow-Up Dashboard",
        "Open quote follow-ups",
        "Document blockers",
        "Shipment exceptions",
        "Customer update gaps",
        "Automation boundary",
        "no real shipper, shipment, customer, quote, invoice, customs entry or production export",
        "no delivery, clearance, savings, revenue, ROI, ranking, compliance or AI-accuracy claim",
    ]:
        assert marker in visual


def test_freight_forwarding_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
