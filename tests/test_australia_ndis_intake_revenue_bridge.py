from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review.html"
FREE_REVIEW_INDEX = ROOT / "free-business-review" / "index.html"
RESOURCE_SLUG = "australia-ndis-intake-vs-answering-service-crm-comparison"


def test_pricing_has_australia_ndis_intake_diagnostic_bridge():
    html = PRICING.read_text(encoding="utf-8")
    assert "Thirty-seven concrete first offers" in html
    assert "Thirty-seven fixed-scope AICS diagnostic offers" in html
    assert '"numberOfItems":37' in html
    assert "https://aicloudstrategist.com/resources/australia-ndis-intake-vs-answering-service-crm-comparison/" in html
    assert "Australia NDIS intake owner-evidence diagnostic" in html
    assert 'data-revenue-bridge="australia-ndis-intake-comparison"' in html
    assert "Australia NDIS intake owner-evidence diagnostic bridge" in html
    assert "Scope before NDIS answering service, CRM, rostering software, referral marketing, AI receptionist or workflow automation spend" in html
    assert f"/resources/{RESOURCE_SLUG}/" in html
    assert f"/resources/{RESOURCE_SLUG}/australia-ndis-intake-comparison-matrix.csv" in html
    assert f"/resources/{RESOURCE_SLUG}/australia-ndis-intake-comparison-map.svg" in html
    assert "/free-business-review/?package=australia-ndis-intake-comparison" in html
    assert "no real NDIS provider, participant, nominee, carer, personal/health data" in html


def test_free_business_review_has_matching_australia_ndis_route_and_flat_copy_is_synced():
    html = FREE_REVIEW.read_text(encoding="utf-8")
    index_html = FREE_REVIEW_INDEX.read_text(encoding="utf-8")
    assert html == index_html
    assert 'data-review-route="australia-ndis-intake-comparison"' in html
    assert "Australia NDIS intake fit check: missed participant calls, support-coordinator referrals, consent prompts, capacity handoff and owner dashboards" in html
    assert f"/resources/{RESOURCE_SLUG}/australia-ndis-intake-comparison-matrix.csv" in html
    assert f"/resources/{RESOURCE_SLUG}/australia-ndis-intake-comparison-map.svg" in html
    assert "/pricing.html#fixed-scope-diagnostics" in html
