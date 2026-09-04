import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
SLUG = "uk-care-home-family-enquiry-follow-up-evidence-checklist"
RESOURCE = f"/resources/{SLUG}/"
RESOURCE_URL = f"https://aicloudstrategist.com{RESOURCE}"
PACKAGE_URL = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_pricing_exposes_uk_care_home_family_enquiry_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Twenty-five concrete first offers" in section
    assert 'data-revenue-bridge="uk-care-home-family-enquiry-follow-up"' in section
    assert "UK care-home family enquiry follow-up diagnostic bridge" in section
    assert "care-home CRM, care planning system, call answering service, local SEO agency or AI receptionist spend" in section
    assert RESOURCE in section
    assert PACKAGE_URL in section
    for boundary in [
        "no care home client",
        "resident data",
        "family data",
        "call recording",
        "care-plan data",
        "legal/privacy/safeguarding/medical/care-quality advice",
        "occupancy, admissions, revenue, ROI or AI-accuracy claim",
    ]:
        assert boundary in section


def test_pricing_itemlist_schema_includes_uk_care_home_service():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(
        doc for doc in _json_ld_documents(html)
        if doc.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    )

    assert item_list["numberOfItems"] == len(item_list["itemListElement"])
    item = next(entry for entry in item_list["itemListElement"] if entry.get("url") == RESOURCE_URL)
    assert item["item"]["name"] == "UK care-home family enquiry follow-up evidence review"
    assert "no resident data, family data, call recordings, care-plan data, credentials or production access" in item["item"]["offers"]["priceSpecification"]["description"]


def test_free_business_review_routes_uk_care_home_buyers():
    directory_html = FREE_REVIEW.read_text(encoding="utf-8")
    flat_html = FREE_REVIEW_FLAT.read_text(encoding="utf-8")
    assert directory_html == flat_html

    for html in (directory_html, flat_html):
        assert 'data-review-route="uk-care-home-family-enquiry-follow-up-evidence-checklist"' in html
        assert "UK care homes / care groups" in html
        assert "Family enquiry follow-up fit check" in html
        assert "missed calls, tour requests, referral emails, funding questions and manager review" in html
        assert RESOURCE in html
        assert "/pricing.html#fixed-scope-diagnostics" in html
