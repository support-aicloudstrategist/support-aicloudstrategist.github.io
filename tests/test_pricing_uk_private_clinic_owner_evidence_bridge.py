import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "/resources/uk-private-clinic-owner-evidence-decision-memo/"
PUBLIC_URL = f"https://aicloudstrategist.com{RESOURCE}"


def _fixed_scope_itemlist(html: str) -> dict:
    itemlist_json = next(
        match.group(1)
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html)
        if "pricing#fixed-scope-diagnostics" in match.group(1)
    )
    return json.loads(itemlist_json)


def test_uk_private_clinic_owner_evidence_pricing_bridge_is_visible_and_claim_safe():
    for pricing_page in PRICING_PAGES:
        html = pricing_page.read_text(encoding="utf-8")
        assert 'data-revenue-bridge="uk-private-clinic-owner-evidence-decision-memo"' in html
        assert "UK private clinic owner-evidence diagnostic bridge" in html
        assert "Scope before AI receptionist, practice-management software, patient engagement" in html
        assert "no-patient-data owner memo" in html
        assert "AI handover stop rules and GDPR evidence questions" in html
        assert RESOURCE in html
        assert "/free-business-review/?package=uk-private-clinic-owner-evidence-decision-memo&amp;source=pricing-fixed-scope" in html
        assert "no real clinic, patient data, personal data, health data" in html
        assert "no real clinic, patient data, personal data, health data, call recording" in html
        assert "legal/privacy/security/clinical/CQC/DTAC/DSPT/GDPR advice" in html
        assert "appointment growth, revenue, savings, ROI or AI-accuracy claim" in html


def test_uk_private_clinic_owner_evidence_pricing_bridge_is_in_schema():
    for pricing_page in PRICING_PAGES:
        html = pricing_page.read_text(encoding="utf-8")
        itemlist = _fixed_scope_itemlist(html)
        matching = [item for item in itemlist["itemListElement"] if item["url"] == PUBLIC_URL]
        assert len(matching) == 1
        bridge = matching[0]
        assert bridge["position"] == 53
        assert bridge["item"]["name"] == "UK private clinic owner-evidence diagnostic bridge"
        assert bridge["item"]["areaServed"] == ["GB", "Europe"]
        offer = bridge["item"]["offers"]
        assert offer["url"] == PUBLIC_URL
        description = offer["priceSpecification"]["description"]
        assert "Scope before UK private-clinic AI receptionist" in description
        assert "no real clinic, patient data, personal data, health data" in description
        assert "legal/privacy/security/clinical/CQC/DTAC/DSPT/GDPR advice" in description
        assert "ranking, demand, lead, booked appointment, patient growth, revenue, savings, ROI" in description
