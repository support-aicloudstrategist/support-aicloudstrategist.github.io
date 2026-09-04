import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
RESOURCE = "/resources/global-enterprise-ai-agent-access-review-evidence-checklist/"
RESOURCE_URL = f"https://aicloudstrategist.com{RESOURCE}"
CSV = f"{RESOURCE}ai-agent-access-review-evidence-template.csv"
PACKAGE_URL = "/free-business-review/?package=enterprise-ai-agent-access-review-evidence&amp;source=pricing-fixed-scope"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_pricing_exposes_ai_agent_access_review_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Twenty-eight concrete first offers" in section
    assert 'data-revenue-bridge="enterprise-ai-agent-access-review-evidence-diagnostic"' in section
    assert "AI agent access review evidence diagnostic" in section
    assert "Scope before expanding AI agent tool access, retrieval sources, service accounts, workflow permissions or production autonomy" in section
    assert RESOURCE in section
    assert CSV in section
    assert PACKAGE_URL in section
    for boundary in [
        "no credentials",
        "secrets",
        "customer data",
        "regulated data",
        "production access",
        "production logs",
        "permission changes",
        "security/legal/privacy/compliance advice",
        "risk-reduction guarantee",
        "revenue, savings, ROI or ranking claim",
    ]:
        assert boundary in section


def test_pricing_itemlist_schema_includes_ai_agent_access_review_service():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(
        doc for doc in _json_ld_documents(html)
        if doc.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    )

    assert item_list["numberOfItems"] == len(item_list["itemListElement"]) == 28
    item = next(entry for entry in item_list["itemListElement"] if entry.get("url") == RESOURCE_URL)
    assert item["position"] == 3
    assert item["item"]["name"] == "AI agent access review evidence diagnostic"
    description = item["item"]["offers"]["priceSpecification"]["description"]
    for boundary in [
        "no credentials",
        "secrets",
        "customer data",
        "regulated data",
        "production access",
        "production logs",
        "permission changes",
        "security/legal/privacy/compliance advice",
        "risk-reduction guarantee",
    ]:
        assert boundary in description
