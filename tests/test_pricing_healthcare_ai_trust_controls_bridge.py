from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "healthcare-ai-trust-controls"


def _pricing_html() -> str:
    return (ROOT / "pricing.html").read_text(encoding="utf-8")


def test_pricing_has_healthcare_ai_trust_controls_revenue_bridge():
    html = _pricing_html()
    assert 'data-revenue-bridge="healthcare-ai-trust-controls"' in html
    assert "Healthcare AI trust controls first-review diagnostic bridge" in html
    assert "Scope before AI receptionist, patient engagement, chatbot, CRM/PMS/EHR workflow or cloud automation spend" in html
    assert f"/resources/{SLUG}/" in html
    assert f"/resources/{SLUG}/healthcare-ai-trust-controls-owner-evidence.csv" in html
    assert "/free-business-review/?package=healthcare-ai-trust-controls&amp;source=pricing-fixed-scope" in html


def test_pricing_healthcare_ai_trust_controls_bridge_keeps_claim_boundaries_near_cta():
    html = _pricing_html()
    start = html.index('data-revenue-bridge="healthcare-ai-trust-controls"')
    end = html.index("</aside>", start)
    block = html[start:end]
    required_boundaries = [
        "no-patient-data",
        "no real clinic, patient, PHI/ePHI, health record, personal data",
        "credential, production access",
        "DPDP/GDPR/UK GDPR/HIPAA compliance proof",
        "legal/privacy/security/medical advice",
        "ranking, demand, lead, appointment, patient, revenue, savings, ROI or automation-performance claim",
    ]
    for boundary in required_boundaries:
        assert boundary in block


def test_pricing_itemlist_count_contract_is_not_changed_by_visual_bridge():
    html = _pricing_html()
    match = re.search(r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList".*?})</script>', html)
    assert match, "pricing ItemList JSON-LD missing"
    itemlist = json.loads(match.group(1))
    assert itemlist["numberOfItems"] == len(itemlist["itemListElement"])
    assert itemlist["numberOfItems"] == 34
