from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review.html"
FREE_REVIEW_INDEX = ROOT / "free-business-review" / "index.html"
RESOURCE_SLUG = "india-healthcare-dpdp-cloud-trust-evidence-source-map"


def test_pricing_has_india_healthcare_dpdp_cloud_trust_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    assert "Thirty-three concrete first offers" in html
    assert 'data-revenue-bridge="india-healthcare-dpdp-cloud-trust-evidence-source-map"' in html
    assert "India healthcare DPDP + cloud trust source-map diagnostic bridge" in html
    assert "Scope before DPDP software, EMR/EHR changes, WhatsApp patient workflows, AI reception, cloud migration, GRC tool or MSP spend" in html
    assert f"/resources/{RESOURCE_SLUG}/" in html
    assert f"/resources/{RESOURCE_SLUG}/india-healthcare-dpdp-cloud-trust-evidence-source-map.csv" in html
    assert "/free-business-review/?package=india-healthcare-dpdp-cloud-trust-source-map" in html
    assert "no hospital, clinic, lab, patient, health record, cloud account, production export, credential, DPDP compliance proof" in html


def test_free_business_review_has_matching_india_healthcare_route_and_flat_copy_is_synced():
    html = FREE_REVIEW.read_text(encoding="utf-8")
    index_html = FREE_REVIEW_INDEX.read_text(encoding="utf-8")
    assert html == index_html
    assert 'data-review-route="india-healthcare-dpdp-cloud-trust-evidence-source-map"' in html
    assert "India healthcare DPDP + cloud trust fit check: patient-data source map, WhatsApp/AI boundaries, cloud owner evidence and adviser-ready questions" in html
    assert f"/resources/{RESOURCE_SLUG}/india-healthcare-dpdp-cloud-trust-owner-map.svg" in html
    assert "/pricing.html#fixed-scope-diagnostics" in html
