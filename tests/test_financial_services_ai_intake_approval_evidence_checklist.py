import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-financial-services-ai-intake-approval-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
REL = f"/resources/{SLUG}/"


def json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_has_indexable_canonical_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert "noindex" not in html.lower()
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "WebPage" and doc.get("url") == URL for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_page_covers_financial_services_buyer_intent_and_safe_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required_phrases = [
        "financial services AI intake automation checklist",
        "client document chasing workflow",
        "AI approval evidence for financial services",
        "risk review queue dashboard",
        "cloud AI spend owner visibility for finance teams",
        "prohibited-advice boundaries",
        "named human approval",
        "not a real financial services case study",
        "not revenue evidence",
        "not cost-savings evidence",
        "not AI-accuracy evidence",
    ]
    for phrase in required_phrases:
        assert phrase in html


def test_resource_links_into_existing_revenue_cluster():
    html = PAGE.read_text(encoding="utf-8")
    required_links = [
        "/industries/financial-services/",
        "/resources/global-insurance-agency-quote-claims-follow-up-checklist/",
        "/resources/global-accounting-firm-tax-season-client-intake-follow-up-checklist/",
        "/resources/ai-answer-validation-prompts/",
        "/resources/cloud-ai-economics-decision-pack/",
        "/free-business-review/?package=global-financial-services-ai-intake-approval-evidence-checklist",
    ]
    for link in required_links:
        assert link in html


def test_discoverability_surfaces_include_resource():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert REL in (ROOT / "industries" / "financial-services" / "index.html").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
