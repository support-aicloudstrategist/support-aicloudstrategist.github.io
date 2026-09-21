import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing" / "index.html"
PRICING_ALIAS = ROOT / "pricing.html"
SLUG = "saudi-healthtech-board-forwarding-memo"
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


def test_saudi_healthtech_board_forwarding_has_pricing_bridge_and_fit_check():
    html = _html()
    assert 'data-revenue-bridge="saudi-healthtech-board-forwarding-memo"' in html
    assert "Saudi healthtech board-forwarding owner-evidence diagnostic bridge" in html
    assert f"/resources/{SLUG}/" in html
    assert FIT_CHECK in html
    assert "EHR/HIS, RCM/NPHIES-adjacent integration, AI receptionist, WhatsApp automation" in html
    assert "no patient data, health data, personal data, claim files, payer records" in html
    assert "compliance proof, regulator approval, ranking, demand, lead, appointment" in html
    assert "savings, revenue, ROI or AI-accuracy claim" in html


def test_saudi_healthtech_board_forwarding_is_in_fixed_scope_json_ld():
    data = _fixed_scope_itemlist(_html())
    assert data["numberOfItems"] == len(data["itemListElement"]) == 46
    assert data["name"] == "46 fixed-scope AICS diagnostic offers"
    item = data["itemListElement"][-1]
    assert item["position"] == 46
    assert item["url"] == f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert item["item"]["name"] == "Saudi healthtech board-forwarding owner-evidence diagnostic"
    assert item["item"]["areaServed"] == ["SA", "GCC", "Global"]
    description = item["item"]["offers"]["priceSpecification"]["description"]
    assert "Scope before Saudi healthtech EHR/HIS" in description
    assert "no patient data, health data, personal data" in description
    assert "Saudi client proof" in description
    assert "savings, revenue, ROI" in description


def test_pricing_alias_stays_in_sync_for_saudi_board_forwarding_bridge():
    assert _html(PRICING_ALIAS) == _html(PRICING)
