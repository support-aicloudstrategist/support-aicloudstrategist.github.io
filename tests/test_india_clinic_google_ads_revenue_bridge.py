import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
SLUG = "india-clinic-google-ads-not-converting-appointment-evidence-checklist"
RESOURCE = f"/resources/{SLUG}/"
RESOURCE_URL = f"https://aicloudstrategist.com{RESOURCE}"
CSV = f"{RESOURCE}india-clinic-google-ads-not-converting-appointment-evidence-checklist.csv"
PACKAGE_URL = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_pricing_exposes_india_clinic_ad_conversion_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Twenty-eight concrete first offers" in section
    assert f'data-revenue-bridge="{SLUG}"' in section
    assert "India clinic ad-to-appointment conversion diagnostic bridge" in section
    assert "Google/Meta ad spend, Practo upgrades, WhatsApp bots, CRM changes or AI receptionist spend" in section
    assert RESOURCE in section
    assert CSV in section
    assert PACKAGE_URL in section
    for boundary in [
        "no clinic client",
        "patient data",
        "health data",
        "ad-account access",
        "marketplace export",
        "DPDP compliance proof",
        "legal/privacy/medical/advertising advice",
        "appointment, revenue, savings, ROI or ad-performance claim",
    ]:
        assert boundary in section


def test_pricing_itemlist_schema_includes_india_clinic_ad_conversion_service():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(
        doc for doc in _json_ld_documents(html)
        if doc.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    )

    assert item_list["numberOfItems"] == len(item_list["itemListElement"])
    item = next(entry for entry in item_list["itemListElement"] if entry.get("url") == RESOURCE_URL)
    assert item["item"]["name"] == "India clinic ad-to-appointment conversion evidence review"
    assert "no patient data, health data, ad-account access, marketplace export, credentials" in item["item"]["offers"]["priceSpecification"]["description"]


def test_free_business_review_routes_india_clinic_ad_buyers():
    directory_html = FREE_REVIEW.read_text(encoding="utf-8")
    flat_html = FREE_REVIEW_FLAT.read_text(encoding="utf-8")
    assert directory_html == flat_html

    for html in (directory_html, flat_html):
        assert f'data-review-route="{SLUG}"' in html
        assert "India clinics buying ads" in html
        assert "Ad-to-appointment conversion fit check" in html
        assert "Google/Meta leads, missed calls, WhatsApp follow-up, front-desk handoff and DPDP-consent evidence" in html
        assert RESOURCE in html
        assert CSV in html
        assert "/pricing.html#fixed-scope-diagnostics" in html
