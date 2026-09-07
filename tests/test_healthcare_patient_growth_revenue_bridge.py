from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "healthcare-ai-patient-growth-platform"
CSV_PATH = f"/resources/{SLUG}/healthcare-ai-patient-growth-owner-evidence.csv"
SVG_PATH = f"/resources/{SLUG}/healthcare-ai-patient-growth-owner-map.svg"


def _pricing_html() -> str:
    return (ROOT / "pricing.html").read_text(encoding="utf-8")


def _free_review_html() -> str:
    return (ROOT / "free-business-review.html").read_text(encoding="utf-8")


def test_pricing_has_healthcare_patient_growth_revenue_bridge():
    html = _pricing_html()
    assert 'data-revenue-bridge="healthcare-ai-patient-growth-platform"' in html
    assert "Healthcare AI Patient GrowthOS diagnostic bridge" in html
    assert "Scope before AI receptionist, patient-access automation, CRM/PMS/EHR workflow, WhatsApp follow-up, chatbot or clinic growth platform spend" in html
    assert f"/resources/{SLUG}/" in html
    assert CSV_PATH in html
    assert SVG_PATH in html
    assert "/free-business-review/?package=healthcare-ai-patient-growth-platform&amp;source=pricing-fixed-scope" in html


def test_pricing_patient_growth_bridge_keeps_no_patient_data_boundaries_near_cta():
    html = _pricing_html()
    start = html.index('data-revenue-bridge="healthcare-ai-patient-growth-platform"')
    end = html.index("</aside>", start)
    block = html[start:end]
    required_boundaries = [
        "no-patient-data",
        "no real healthcare client, clinic, patient, PHI/ePHI, health record, personal data",
        "vendor export, credential, production access",
        "GDPR/UK GDPR/DPIA/NIS2/ISO/SOC2/HIPAA compliance proof",
        "legal/privacy/security/medical advice",
        "revenue, savings, ROI or automation-performance claim",
    ]
    for boundary in required_boundaries:
        assert boundary in block


def test_pricing_itemlist_includes_patient_growth_service_with_matching_count():
    html = _pricing_html()
    match = re.search(r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList".*?})</script>', html)
    assert match, "pricing ItemList JSON-LD missing"
    itemlist = json.loads(match.group(1))
    assert itemlist["numberOfItems"] == len(itemlist["itemListElement"])
    urls = [item["url"] for item in itemlist["itemListElement"]]
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in urls
    item = itemlist["itemListElement"][urls.index(f"https://aicloudstrategist.com/resources/{SLUG}/")]["item"]
    assert item["name"] == "Healthcare AI Patient GrowthOS evidence review"
    description = item["offers"]["priceSpecification"]["description"]
    assert "no patient data" in description
    assert "revenue, savings, ROI" in description


def test_free_business_review_routes_patient_growth_buyers_to_bridge():
    html = _free_review_html()
    assert 'data-review-route="healthcare-ai-patient-growth-platform"' in html
    assert "Healthcare AI Patient GrowthOS fit check" in html
    assert f"/resources/{SLUG}/" in html
    assert CSV_PATH in html
    assert SVG_PATH in html
    assert "/pricing.html#fixed-scope-diagnostics" in html
    mirror = (ROOT / "free-business-review" / "index.html").read_text(encoding="utf-8")
    assert 'data-review-route="healthcare-ai-patient-growth-platform"' in mirror
