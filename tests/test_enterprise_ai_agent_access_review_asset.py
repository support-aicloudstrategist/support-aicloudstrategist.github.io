import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-enterprise-ai-agent-access-review-evidence-checklist"
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


def test_page_contains_enterprise_ai_access_control_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Enterprise AI agent access review evidence checklist",
        "Enterprise AI agent access review checklist",
        "AI agent tool permission evidence",
        "AI agent data access governance checklist",
        "LLM retrieval source access review",
        "agent identity and service account review",
        "AI access revocation evidence checklist",
        "Human-review route",
        "Monitoring and revocation trigger",
        "executive-ready decision packet",
    ]:
        assert phrase in html
    for boundary in [
        "not a real customer case study",
        "not a testimonial",
        "not customer proof",
        "no real enterprise client",
        "no real enterprise client, customer, user, prospect, lead, opportunity, production incident",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not implementation advice",
        "not a compliance claim",
        "does not claim SOC 2 compliance, ISO compliance, GDPR compliance, EU AI Act compliance, HIPAA compliance",
        "revenue result, ROI result, ranking result, ad-performance result or AI-performance result",
    ]:
        assert boundary in html


def test_asset_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
