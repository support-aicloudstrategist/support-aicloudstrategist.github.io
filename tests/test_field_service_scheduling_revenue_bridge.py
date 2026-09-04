import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
SLUG = "global-field-service-technician-scheduling-owner-evidence-checklist"
RESOURCE = f"/resources/{SLUG}/"
RESOURCE_URL = f"https://aicloudstrategist.com{RESOURCE}"
CSV = f"/resources/{SLUG}/field-service-technician-scheduling-owner-evidence.csv"
PACKAGE_URL = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_pricing_exposes_field_service_scheduling_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Thirty-one concrete first offers" in section
    assert 'data-revenue-bridge="field-service-technician-scheduling-owner-evidence"' in section
    assert "Field service technician scheduling evidence diagnostic bridge" in section
    assert "field-service management software, CRM cleanup, call answering, WhatsApp automation or AI scheduling spend" in section
    assert RESOURCE in section
    assert PACKAGE_URL in section
    for boundary in [
        "no field-service customer",
        "technician",
        "phone number",
        "CRM/FSM export",
        "GPS record",
        "booked job, utilisation, SLA, savings, revenue, ROI or automation-performance claim",
    ]:
        assert boundary in section


def test_pricing_itemlist_schema_includes_field_service_scheduling_review():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(
        doc for doc in _json_ld_documents(html)
        if doc.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    )

    assert item_list["numberOfItems"] == len(item_list["itemListElement"])
    item = next(entry for entry in item_list["itemListElement"] if entry.get("url") == RESOURCE_URL)
    assert item["item"]["name"] == "Field service technician scheduling evidence review"
    description = item["item"]["offers"]["priceSpecification"]["description"]
    assert "no customer data" in description
    assert "CRM/FSM exports" in description
    assert "booked-job, utilisation, SLA, savings, revenue, ROI or automation-performance claim" in description


def test_free_business_review_routes_field_service_buyers_to_public_asset():
    directory_html = FREE_REVIEW.read_text(encoding="utf-8")
    flat_html = FREE_REVIEW_FLAT.read_text(encoding="utf-8")
    assert directory_html == flat_html

    for html in (directory_html, flat_html):
        assert f'data-review-route="{SLUG}"' in html
        assert "Field-service / home-service operations" in html
        assert "Technician scheduling evidence fit check" in html
        assert "missed appointments, dispatch handoff, parts blockers, customer updates and quote follow-up" in html
        assert RESOURCE in html
        assert CSV in html
        assert "/pricing.html#fixed-scope-diagnostics" in html
