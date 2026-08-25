import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-demo-security-questionnaire-follow-up-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
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
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_page_contains_saas_buyer_language_and_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "B2B SaaS demo-to-security-questionnaire follow-up evidence checklist",
        "SaaS security questionnaire taking too long",
        "vendor security questionnaire follow up process",
        "Sales demo follow up procurement blocker SaaS",
        "Trust center security questionnaire evidence room",
        "AI vendor questionnaire customer due diligence",
        "Deal desk legal security procurement handoff CRM",
        "source-to-owner evidence",
        "AI-safe draft status",
        "founder/CRO dashboard",
    ]:
        assert phrase in html
    for boundary in [
        "not a real customer case study",
        "not a testimonial",
        "not customer proof",
        "no real SaaS client",
        "no real SaaS client, customer, user, prospect, lead, opportunity, CRM export",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not a compliance claim",
        "does not claim SOC 2 compliance, ISO compliance, GDPR compliance, EU AI Act compliance",
        "revenue result, ROI result, ranking result, ad-performance result or AI-accuracy result",
    ]:
        assert boundary in html


def test_asset_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
