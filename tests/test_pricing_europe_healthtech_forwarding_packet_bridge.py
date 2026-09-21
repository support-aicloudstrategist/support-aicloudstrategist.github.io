import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing" / "index.html"
PRICING_ALIAS = ROOT / "pricing.html"
SLUG = "europe-healthtech-cloud-trust-finops-forwarding-packet"
FIT_CHECK = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _html(path=PRICING):
    return path.read_text(encoding="utf-8")


def _fixed_scope_itemlist(html):
    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing fixed-scope ItemList JSON-LD missing"
    return json.loads(match.group(1))


def test_europe_healthtech_forwarding_packet_has_pricing_bridge_and_fit_check():
    html = _html()
    assert 'data-revenue-bridge="europe-healthtech-cloud-trust-finops-forwarding-packet"' in html
    assert "Europe healthtech cloud trust + AI FinOps forwarding-packet diagnostic bridge" in html
    assert f"/resources/{SLUG}/" in html
    assert FIT_CHECK in html
    assert "no patient data, health data, personal data, cloud bill, GRC export, credential, production access" in html
    assert "compliance proof, ranking, demand, lead, customer, revenue, savings, ROI or AI-accuracy claim" in html


def test_europe_healthtech_forwarding_packet_is_in_fixed_scope_json_ld():
    data = _fixed_scope_itemlist(_html())
    assert data["numberOfItems"] == len(data["itemListElement"]) == 46
    assert data["name"] == "46 fixed-scope AICS diagnostic offers"
    item = next(
        item for item in data["itemListElement"]
        if item["url"] == f"https://aicloudstrategist.com/resources/{SLUG}/"
    )
    assert item["position"] == 44
    assert item["item"]["name"] == "Europe healthtech cloud trust and AI FinOps forwarding-packet diagnostic"
    description = item["item"]["offers"]["priceSpecification"]["description"]
    assert "GDPR/DPIA" in description
    assert "no patient data, health data, personal data" in description
    assert "revenue, savings, ROI" in description


def test_pricing_alias_stays_in_sync_for_the_bridge():
    assert _html(PRICING_ALIAS) == _html(PRICING)
