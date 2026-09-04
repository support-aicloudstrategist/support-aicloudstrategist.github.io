import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
RESOURCE = "/resources/europe-healthtech-nis2-cloud-incident-supplier-evidence-checklist/"
RESOURCE_URL = f"https://aicloudstrategist.com{RESOURCE}"
CSV = f"{RESOURCE}europe-healthtech-nis2-cloud-incident-supplier-evidence-checklist.csv"
PACKAGE_URL = "/free-business-review/?package=europe-healthtech-nis2-incident-supplier-evidence&amp;source=pricing-fixed-scope"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_pricing_exposes_europe_healthtech_nis2_incident_supplier_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Twenty-eight concrete first offers" in section
    assert 'data-revenue-bridge="europe-healthtech-nis2-incident-supplier-evidence"' in section
    assert "Europe healthtech NIS2 incident supplier evidence diagnostic bridge" in section
    assert "cloud incident evidence-room, supplier-risk questionnaire, NIS2-readiness, GDPR/DPIA, security-questionnaire, cloud trust or FinOps spend" in section
    assert RESOURCE in section
    assert CSV in section
    assert PACKAGE_URL in section
    for boundary in [
        "no credentials",
        "patient data",
        "personal data",
        "health data",
        "production logs",
        "supplier portal access",
        "legal/privacy/security/audit/clinical advice",
        "NIS2/GDPR/ISO/SOC2/NHS compliance proof",
        "ranking, demand, lead, customer, revenue, savings or ROI claim",
    ]:
        assert boundary in section


def test_pricing_itemlist_schema_includes_europe_healthtech_nis2_service():
    html = PRICING.read_text(encoding="utf-8")
    item_list = next(
        doc for doc in _json_ld_documents(html)
        if doc.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    )

    assert item_list["numberOfItems"] == len(item_list["itemListElement"]) == 28
    item = next(entry for entry in item_list["itemListElement"] if entry.get("url") == RESOURCE_URL)
    assert item["position"] == 6
    assert item["item"]["name"] == "Europe healthtech NIS2 incident supplier evidence diagnostic"
    description = item["item"]["offers"]["priceSpecification"]["description"]
    for boundary in [
        "no credentials",
        "patient data",
        "personal data",
        "health data",
        "production logs",
        "supplier portal access",
        "legal/privacy/security/audit/clinical advice",
        "compliance proof",
        "savings, revenue, ROI or ranking claim",
    ]:
        assert boundary in description
