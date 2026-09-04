import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-customer-onboarding-implementation-delay-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SVG = ROOT / "resources" / SLUG / "saas-onboarding-delay-owner-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_is_indexable_canonical_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "ImageObject" and "saas-onboarding-delay-owner-dashboard.svg" in doc.get("contentUrl", "") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_page_contains_saas_onboarding_buyer_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "B2B SaaS customer onboarding implementation delay checklist",
        "SaaS customer onboarding implementation delayed",
        "B2B SaaS implementation handoff sales to customer success delays",
        "SaaS onboarding kickoff customer success implementation checklist",
        "customer onboarding data migration blocker SaaS",
        "SaaS integration delay onboarding checklist",
        "customer success onboarding dashboard renewal risk",
        "Sales-to-CS handoff evidence",
        "Human-review route",
        "executive visibility dashboard",
        "Demo owner dashboard",
        "saas-onboarding-delay-owner-dashboard.svg",
    ]:
        assert phrase in html
    for boundary in [
        "not a real customer case study",
        "not a testimonial",
        "not customer proof",
        "no real SaaS client",
        "no real SaaS client, customer, user, prospect, lead, opportunity, CRM export, customer-success export",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not implementation advice",
        "not a compliance claim",
        "does not claim SOC 2 compliance, ISO compliance, GDPR compliance, EU AI Act compliance",
        "revenue result, ROI result, ranking result, ad-performance result or AI-accuracy result",
    ]:
        assert boundary in html


def test_asset_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "saas-onboarding-delay-owner-dashboard.svg" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "saas-onboarding-delay-owner-dashboard.svg" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_demo_owner_dashboard_is_buyer_safe_and_bounded():
    svg = SVG.read_text(encoding="utf-8")
    for marker in [
        "Demo SaaS onboarding delay owner dashboard",
        "Synthetic · no customer data",
        "Handoff",
        "Blocker",
        "Review gate",
        "Owner board",
        "not a real customer dashboard",
        "not retention/revenue/onboarding-speed proof",
    ]:
        assert marker in svg
