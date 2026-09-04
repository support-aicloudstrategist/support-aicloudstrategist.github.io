import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-enterprise-ai-agent-access-review-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-agent-access-review-evidence-template.csv"
SVG = ROOT / "resources" / SLUG / "ai-agent-access-review-owner-board.svg"
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


def test_downloadable_access_review_csv_template_is_available_and_buyer_safe():
    html = PAGE.read_text(encoding="utf-8")
    csv_link = f"/resources/{SLUG}/ai-agent-access-review-evidence-template.csv"
    assert csv_link in html
    assert CSV.is_file()
    csv = CSV.read_text(encoding="utf-8")
    for header in [
        "agent_or_workflow_name",
        "agent_identity_or_service_account",
        "permission_type",
        "data_or_retrieval_source",
        "human_review_route",
        "revocation_trigger",
        "claim_boundary",
    ]:
        assert header in csv.splitlines()[0]
    assert "Synthetic row only" in csv
    for forbidden in ["real client", "customer proof", "guaranteed", "certified", "increased revenue"]:
        assert forbidden not in csv.lower()


def test_access_review_owner_board_svg_is_linked_and_claim_safe():
    html = PAGE.read_text(encoding="utf-8")
    svg_link = f"/resources/{SLUG}/ai-agent-access-review-owner-board.svg"
    assert svg_link in html
    assert f"https://aicloudstrategist.com{svg_link}" in html
    assert SVG.is_file()
    svg = SVG.read_text(encoding="utf-8")
    for phrase in [
        "AI agent access review owner board",
        "Business owner",
        "Tool permission",
        "Retrieval boundary",
        "Human review",
        "Monitoring evidence needed",
        "Revocation triggers",
        "No claim of risk reduction, compliance, savings, revenue, ranking or customer outcome",
    ]:
        assert phrase in svg
