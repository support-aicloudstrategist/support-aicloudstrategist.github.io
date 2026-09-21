import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing" / "index.html"
PRICING_ALIAS = ROOT / "pricing.html"
SLUG = "uk-private-clinic-patient-growthos-trust-comparison"
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


def test_uk_private_clinic_patient_growthos_has_pricing_bridge_and_fit_check():
    html = _html()
    assert 'data-revenue-bridge="uk-private-clinic-patient-growthos-trust-comparison"' in html
    assert "UK private clinic Patient GrowthOS trust diagnostic bridge" in html
    assert f"/resources/{SLUG}/" in html
    assert FIT_CHECK in html
    assert "clinic CRM, practice-management, review-marketplace, AI receptionist, ads" in html
    assert "no real clinic, patient data, special-category health data, call recording, EHR/PMS export" in html
    assert "booked consultation, patient growth, revenue, savings, ROI or AI-accuracy claim" in html


def test_uk_private_clinic_patient_growthos_is_in_fixed_scope_json_ld():
    data = _fixed_scope_itemlist(_html())
    assert data["numberOfItems"] == len(data["itemListElement"]) == 45
    assert data["name"] == "45 fixed-scope AICS diagnostic offers"
    item = data["itemListElement"][-1]
    assert item["position"] == 45
    assert item["url"] == f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert item["item"]["name"] == "UK private clinic Patient GrowthOS trust diagnostic"
    description = item["item"]["offers"]["priceSpecification"]["description"]
    assert "clinic CRM" in description
    assert "CQC/UK GDPR compliance proof" in description
    assert "booked consultation, patient growth, revenue, savings, ROI" in description


def test_pricing_alias_stays_in_sync_for_uk_private_clinic_bridge():
    assert _html(PRICING_ALIAS) == _html(PRICING)
