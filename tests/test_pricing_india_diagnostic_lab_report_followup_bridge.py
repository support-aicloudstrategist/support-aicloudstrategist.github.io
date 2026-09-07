from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-diagnostic-lab-report-delay-whatsapp-follow-up-checklist"
CSV_PATH = f"/resources/{SLUG}/diagnostic-lab-report-follow-up-owner-evidence.csv"


def _pricing_html() -> str:
    return (ROOT / "pricing.html").read_text(encoding="utf-8")


def test_pricing_has_india_diagnostic_lab_report_followup_revenue_bridge():
    html = _pricing_html()
    assert 'data-revenue-bridge="india-diagnostic-lab-report-delay-whatsapp-follow-up"' in html
    assert "India diagnostic lab report-delay follow-up diagnostic bridge" in html
    assert "Scope before LIS add-ons, CRM cleanup, WhatsApp automation, call-centre support or AI receptionist spend" in html
    assert f"/resources/{SLUG}/" in html
    assert CSV_PATH in html
    assert "/free-business-review/?package=india-diagnostic-lab-report-delay-whatsapp-follow-up&amp;source=pricing-fixed-scope" in html


def test_pricing_lab_bridge_keeps_proof_boundaries_near_cta():
    html = _pricing_html()
    start = html.index('data-revenue-bridge="india-diagnostic-lab-report-delay-whatsapp-follow-up"')
    end = html.index("</aside>", start)
    block = html[start:end]
    required_boundaries = [
        "no-patient-data",
        "no patient data",
        "no patient data, health records, lab reports, phone numbers, LIS/CRM export, credentials, production access",
        "DPDP compliance proof",
        "legal/privacy/medical advice",
        "revenue, savings, ROI or automation-performance claim",
    ]
    for boundary in required_boundaries:
        assert boundary in block


def test_pricing_itemlist_includes_lab_followup_service_with_matching_count():
    html = _pricing_html()
    match = re.search(r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList".*?})</script>', html)
    assert match, "pricing ItemList JSON-LD missing"
    itemlist = json.loads(match.group(1))
    assert itemlist["numberOfItems"] == len(itemlist["itemListElement"])
    urls = [item["url"] for item in itemlist["itemListElement"]]
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in urls
    lab_item = itemlist["itemListElement"][urls.index(f"https://aicloudstrategist.com/resources/{SLUG}/")]["item"]
    assert lab_item["name"] == "India diagnostic lab report-delay follow-up evidence review"
    assert "no patient data" in lab_item["offers"]["priceSpecification"]["description"]
