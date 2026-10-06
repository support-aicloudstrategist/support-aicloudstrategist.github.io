import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
RESOURCE = "/resources/global-enterprise-ai-incident-response-evidence-runbook/"
RESOURCE_URL = f"https://aicloudstrategist.com{RESOURCE}"
CSV = f"{RESOURCE}ai-incident-evidence-log-template.csv"
PACKAGE_URL = "/free-business-review/?package=enterprise-ai-incident-response-evidence&amp;source=pricing-fixed-scope"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_pricing_exposes_enterprise_ai_incident_response_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Fifty-four structured fixed-scope diagnostic offers" in section
    assert 'data-revenue-bridge="enterprise-ai-incident-response-evidence-diagnostic"' in section
    assert "Enterprise AI incident response evidence diagnostic" in section
    assert "Scope before production AI incident-response tooling, managed AI operations, AI security review, rollback planning or executive trust reporting spend" in section
    assert RESOURCE in section
    assert CSV in section
    assert PACKAGE_URL in section
    for boundary in [
        "no credentials",
        "secrets",
        "customer data",
        "regulated data",
        "production logs",
        "model traces",
        "prompt repository access",
        "containment execution",
        "legal/cybersecurity/privacy/compliance/insurance advice",
        "compliance proof",
        "breach assessment",
        "uptime guarantee",
        "risk-reduction guarantee",
        "revenue, savings, ROI or ranking claim",
    ]:
        assert boundary in section


def test_pricing_itemlist_schema_includes_enterprise_ai_incident_response_service():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(
        doc for doc in _json_ld_documents(html)
        if doc.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    )

    assert item_list["numberOfItems"] == len(item_list["itemListElement"]) == 54
    item = next(entry for entry in item_list["itemListElement"] if entry.get("url") == RESOURCE_URL)
    assert item["position"] == 7
    assert item["item"]["name"] == "Enterprise AI incident response evidence diagnostic"
    description = item["item"]["offers"]["priceSpecification"]["description"]
    for boundary in [
        "no credentials",
        "secrets",
        "customer data",
        "regulated data",
        "production logs",
        "model traces",
        "prompt repository access",
        "containment execution",
        "legal/cybersecurity/privacy/compliance/insurance advice",
        "compliance proof",
        "breach assessment",
        "uptime guarantee",
        "risk-reduction guarantee",
    ]:
        assert boundary in description
