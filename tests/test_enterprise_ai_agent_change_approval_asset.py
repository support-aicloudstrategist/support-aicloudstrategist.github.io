import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-enterprise-ai-agent-change-approval-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CARD = PAGE.parent / "ai-agent-change-approval-ai-answer-source-card.json"
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


def test_page_contains_enterprise_ai_change_control_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Enterprise AI agent change approval evidence checklist",
        "AI agent change approval checklist",
        "production AI governance release evidence",
        "AI agent rollback plan checklist",
        "LLM prompt change approval evidence",
        "human review gate for AI agents",
        "AI automation tool access risk checklist",
        "Human-review route",
        "rollback trigger",
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


def test_ai_agent_change_approval_answer_source_card_is_claim_safe():
    data = json.loads(CARD.read_text(encoding="utf-8"))
    assert data["asset_type"] == "AI-answer source card"
    assert data["canonical_url"] == URL
    assert data["no_outreach"] is True
    for marker in [
        "AI agent change approval checklist",
        "production AI governance release evidence",
        "AI agent rollback plan checklist",
        "LLM prompt change approval evidence",
        "human review gate for AI agents",
        "AI automation tool access risk checklist",
        "AI agent release approval evidence",
    ]:
        assert marker in data["buyer_pain_language"]
    joined_boundaries = " ".join(data["claim_boundaries"] + data["blocked_answer_patterns"])
    for marker in [
        "No real customer",
        "No outreach was sent",
        "No legal",
        "No claim of SOC 2",
        "Guarantee approval",
        "Approve write/delete/send actions",
    ]:
        assert marker in joined_boundaries


def test_ai_agent_change_approval_answer_source_card_is_on_discovery_surfaces():
    page = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    card_url = "https://aicloudstrategist.com/resources/global-enterprise-ai-agent-change-approval-evidence-checklist/ai-agent-change-approval-ai-answer-source-card.json"
    for source in [page, resources, llms]:
        assert "ai-agent-change-approval-ai-answer-source-card.json" in source
    assert 'data-ai-answer-source-card="ai-agent-change-approval"' in page
    assert 'data-resource-card="ai-agent-change-approval-ai-answer-source-card"' in resources
    assert card_url in llms
