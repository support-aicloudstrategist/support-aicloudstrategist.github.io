import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_FILES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
SLUG = "home-care-referral-intake-diagnostic-package"
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


def _fixed_scope_section(html: str) -> str:
    start = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1]
    return start.split('<section class="section"><div class="container faq">', 1)[0]


def test_home_care_diagnostic_visible_on_both_pricing_routes() -> None:
    for path in PRICING_FILES:
        section = _fixed_scope_section(path.read_text(encoding="utf-8"))
        assert 'data-revenue-bridge="home-care-referral-intake-diagnostic-package"' in section
        assert "Home-care referral intake diagnostic bridge" in section
        assert "Scope before home-care CRM, care-management platform, answering service" in section
        assert "no-patient-data owner view" in section
        assert "owner-dashboard demo" in section
        assert REL in section
        assert FIT in section
        for boundary in [
            "no real home-care agency",
            "patient/resident data",
            "family data",
            "caregiver files",
            "referral records",
            "call recording",
            "credential",
            "production access",
            "legal/privacy/compliance/clinical/staffing/billing advice",
            "admission, census",
            "revenue, savings, ROI",
            "AI-accuracy claim",
        ]:
            assert boundary in section


def test_home_care_diagnostic_pricing_structured_data_is_sellable_claim_safe() -> None:
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    itemlist = _fixed_scope_itemlist(html)
    assert itemlist["numberOfItems"] == len(itemlist["itemListElement"])
    assert itemlist["name"] == f'{itemlist["numberOfItems"]} fixed-scope AICS diagnostic offers'
    offer = next(item for item in itemlist["itemListElement"] if item["url"] == URL)
    assert offer["item"]["name"] == "Home-care referral intake diagnostic package"
    assert offer["item"]["areaServed"] == ["US", "UK", "CA", "AU", "Global"]
    description = offer["item"]["offers"]["priceSpecification"]["description"]
    assert "Scope before home-care CRM" in description
    assert "patient/resident data" in description
    assert "caregiver files" in description
    assert "legal/privacy/compliance/clinical/staffing/billing advice" in description
    assert "revenue, savings, ROI or AI-accuracy claim" in description
