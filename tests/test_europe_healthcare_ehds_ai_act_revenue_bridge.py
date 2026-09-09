from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthcare-ehds-ai-act-cloud-trust-source-map"
FIT_CHECK = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_pricing_exposes_europe_healthcare_ehds_ai_act_bridge():
    html = read("pricing.html")
    assert 'data-revenue-bridge="europe-healthcare-ehds-ai-act-cloud-trust-source-map"' in html
    assert "Europe healthcare EHDS + EU AI Act cloud-trust diagnostic bridge" in html
    assert "/resources/europe-healthcare-ehds-ai-act-cloud-trust-source-map/" in html
    assert "europe-healthcare-ehds-ai-act-answer-bank.csv" in html
    assert "europe-healthcare-ehds-ai-act-ai-answer-source-card.json" in html
    assert FIT_CHECK in html


def test_pricing_bridge_keeps_claim_boundaries_near_fit_check():
    html = read("pricing.html")
    start = html.index('data-revenue-bridge="europe-healthcare-ehds-ai-act-cloud-trust-source-map"')
    section = html[start: html.index('data-revenue-bridge="saas-security-questionnaire-evidence-pack"')]
    for blocked in [
        "no real healthcare buyer",
        "PHI/ePHI",
        "EHDS/GDPR/UK GDPR/EU AI Act/NIS2/ISO/SOC2/DSPT/DTAC compliance proof",
        "ranking",
        "revenue",
        "ROI",
        "AI-accuracy claim",
    ]:
        assert blocked in section
    assert "no-patient-data source map" in section
    assert "cloud/AI FinOps" in section


def test_pricing_index_mirror_matches_flat_pricing_route():
    assert read("pricing/index.html") == read("pricing.html")


def test_free_review_routes_surface_europe_healthcare_fit_check():
    for relative in ["free-business-review/index.html", "free-business-review.html"]:
        html = read(relative)
        assert 'data-review-route="europe-healthcare-ehds-ai-act-cloud-trust-source-map"' in html
        assert "EHDS + EU AI Act cloud-trust fit check" in html
        assert "europe-healthcare-ehds-ai-act-cloud-trust-source-map.csv" in html
        assert "europe-healthcare-ehds-ai-act-answer-bank.csv" in html
        assert "/pricing.html#fixed-scope-diagnostics" in html
