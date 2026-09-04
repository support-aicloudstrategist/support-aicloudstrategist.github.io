import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
SLUG = "global-b2b-saas-customer-onboarding-implementation-delay-checklist"
RESOURCE = f"/resources/{SLUG}/"
RESOURCE_URL = f"https://aicloudstrategist.com{RESOURCE}"
SVG = f"{RESOURCE}saas-onboarding-delay-owner-dashboard.svg"
PACKAGE_URL = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_pricing_exposes_b2b_saas_onboarding_delay_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Twenty-six concrete first offers" in section
    assert 'data-revenue-bridge="global-b2b-saas-customer-onboarding-delay"' in section
    assert "B2B SaaS onboarding-delay owner dashboard diagnostic bridge" in section
    assert "customer-success platform, onboarding automation, project board, CRM workflow or AI follow-up spend" in section
    assert RESOURCE in section
    assert SVG in section
    assert PACKAGE_URL in section
    for boundary in [
        "no SaaS client",
        "CRM export",
        "customer-success export",
        "credential",
        "production access",
        "legal/privacy/security/implementation advice",
        "revenue, retention, churn, onboarding-speed, ROI or AI-accuracy claim",
    ]:
        assert boundary in section


def test_pricing_itemlist_schema_includes_saas_onboarding_delay_service():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(
        doc for doc in _json_ld_documents(html)
        if doc.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    )

    assert item_list["numberOfItems"] == len(item_list["itemListElement"])
    item = next(entry for entry in item_list["itemListElement"] if entry.get("url") == RESOURCE_URL)
    assert item["item"]["name"] == "B2B SaaS onboarding delay owner dashboard review"
    assert "no CRM export, customer-success export, customer data, credentials or production access" in item["item"]["offers"]["priceSpecification"]["description"]


def test_free_business_review_routes_b2b_saas_onboarding_delay_buyers():
    directory_html = FREE_REVIEW.read_text(encoding="utf-8")
    flat_html = FREE_REVIEW_FLAT.read_text(encoding="utf-8")
    assert directory_html == flat_html

    for html in (directory_html, flat_html):
        assert 'data-review-route="global-b2b-saas-customer-onboarding-implementation-delay-checklist"' in html
        assert "B2B SaaS founders / customer success leaders" in html
        assert "Customer onboarding implementation delay fit check" in html
        assert "sales-to-CS handoff, blocker ownership, kickoff, data migration and renewal-risk visibility" in html
        assert RESOURCE in html
        assert SVG in html
        assert "/pricing.html#fixed-scope-diagnostics" in html
