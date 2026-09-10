import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
SLUG = "saudi-healthtech-cloud-trust-nphies-owner-evidence-checklist"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
REL = f"/resources/{SLUG}/"
FIT = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _pricing_html() -> str:
    return PRICING.read_text(encoding="utf-8")


def _fixed_scope_itemlist(html: str) -> dict:
    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing fixed-scope ItemList JSON-LD missing"
    return json.loads(match.group(1))


def test_pricing_surfaces_saudi_healthtech_nphies_as_sellable_first_step():
    html = _pricing_html()
    assert 'data-revenue-bridge="saudi-healthtech-nphies-cloud-trust"' in html
    assert "Saudi healthtech Cloud Trust + NPHIES evidence diagnostic bridge" in html
    assert "Scope before patient-access platform, AI receptionist, WhatsApp follow-up, cloud, FinOps or vendor-questionnaire spend" in html
    assert "no-patient-data owner view of NPHIES-adjacent workflow evidence" in html
    assert REL in html
    assert FIT in html
    for blocked_claim in [
        "no patient data",
        "NPHIES production evidence",
        "Saudi client proof",
        "regulator approval",
        "revenue, ROI or AI-accuracy claim",
    ]:
        assert blocked_claim in html


def test_pricing_structured_data_includes_saudi_healthtech_nphies_offer():
    html = _pricing_html()
    itemlist = _fixed_scope_itemlist(html)
    assert itemlist["numberOfItems"] == len(itemlist["itemListElement"]) == 42
    assert itemlist["name"] == "42 fixed-scope AICS diagnostic offers"
    offer = next(item for item in itemlist["itemListElement"] if item["url"] == URL)
    assert offer["position"] == 42
    assert offer["item"]["name"] == "Saudi healthtech Cloud Trust + NPHIES evidence diagnostic"
    assert offer["item"]["areaServed"] == ["SA", "GCC", "Global"]
    description = offer["item"]["offers"]["priceSpecification"]["description"]
    assert "Scope before Saudi healthtech patient-access platform" in description
    assert "no patient data" in description
    assert "NPHIES production evidence" in description
    assert "Saudi client proof" in description
    assert "revenue, ROI or AI-accuracy claim" in description
