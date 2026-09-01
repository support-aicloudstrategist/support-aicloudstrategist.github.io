import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-enterprise-ai-rfp-response-evidence-checklist"
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
    graph_docs = []
    for doc in docs:
        if "@graph" in doc:
            graph_docs.extend(doc["@graph"])
        else:
            graph_docs.append(doc)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in graph_docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_page_contains_buyer_intent_and_safe_ai_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Enterprise AI RFP response evidence checklist",
        "enterprise AI RFP response",
        "AI RFP evidence checklist",
        "AI procurement response evidence",
        "AI security questionnaire RFP",
        "AI vendor due diligence response",
        "AI human oversight RFP",
        "AI output is draft support, not an official representation",
        "Request RFP evidence review",
    ]:
        assert phrase in html
    for boundary in [
        "not a real customer case study",
        "not a testimonial",
        "not customer proof",
        "not an RFP win claim",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not procurement advice",
        "not a compliance claim",
        "does not claim SOC 2 compliance, ISO compliance, GDPR compliance, HIPAA compliance, EU AI Act compliance",
        "revenue result, ROI result, ranking result, ad-performance result, procurement win rate or AI-accuracy result",
        "No real SaaS client, customer, user, prospect, lead, opportunity, RFP or buyer result is represented",
    ]:
        assert boundary in html


def test_asset_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
