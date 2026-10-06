import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_FILES = [ROOT / "pricing" / "index.html", ROOT / "pricing.html"]
SLUG = "dpdp-compliance-checklist-small-business-india"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
REL = f"/resources/{SLUG}/"
FIT = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _fixed_scope_itemlist(html: str) -> dict:
    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing fixed-scope ItemList JSON-LD missing"
    return json.loads(match.group(1))


def test_dpdp_smb_pricing_bridge_visible_on_both_pricing_routes():
    for path in PRICING_FILES:
        html = path.read_text(encoding="utf-8")
        assert 'data-revenue-bridge="dpdp-smb-owner-evidence-diagnostic"' in html
        assert "India SMB DPDP owner-evidence diagnostic bridge" in html
        assert REL in html
        assert REL + "dpdp-smb-shortlist-scoring-matrix.csv" in html
        assert FIT in html
        assert "Scope before CRM, WhatsApp automation, chatbot, lead-capture, privacy-consultant, legal-review, agency or internal spreadsheet spend" in html
        assert "no real customer, prospect, patient, child, financial, payment, health, sensitive personal or production data" in html
        assert "DPDP compliance proof, regulator approval, audit opinion, ranking, demand, lead, customer, revenue, savings, ROI or automation-performance claim" in html


def test_dpdp_smb_pricing_bridge_in_fixed_scope_json_ld():
    html = (ROOT / "pricing" / "index.html").read_text(encoding="utf-8")
    data = _fixed_scope_itemlist(html)
    assert data["numberOfItems"] == len(data["itemListElement"]) == 55
    assert data["name"] == "55 fixed-scope AICS diagnostic offers"
    offer = next(item for item in data["itemListElement"] if item["url"] == URL)
    assert offer["position"] == 55
    service = offer["item"]
    assert service["name"] == "India SMB DPDP owner-evidence diagnostic bridge"
    assert service["areaServed"] == ["India"]
    description = service["offers"]["priceSpecification"]["description"]
    assert "CRM, WhatsApp automation, chatbot" in description
    assert "legal/privacy/security advice" in description
    assert "DPDP compliance proof" in description
    assert "revenue, savings, ROI" in description
