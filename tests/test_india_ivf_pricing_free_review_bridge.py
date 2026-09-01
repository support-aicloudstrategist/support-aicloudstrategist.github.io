from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-ivf-fertility-missed-patient-calls-vs-crm-ai-receptionist-comparison"
RESOURCE_PATH = f"/resources/{SLUG}/"
PROBLEM = "india-ivf-missed-patient-calls-owner-evidence"


def test_pricing_has_india_ivf_fixed_scope_bridge():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    assert 'data-revenue-bridge="india-ivf-missed-patient-calls-owner-evidence"' in html
    assert "India IVF missed patient calls owner-evidence diagnostic bridge" in html
    assert RESOURCE_PATH in html
    assert f"/free-business-review/?problem={PROBLEM}&amp;source=pricing-fixed-scope" in html
    for phrase in [
        "clinic CRM",
        "WhatsApp automation",
        "AI receptionist",
        "no patient data",
        "no patient data, PHI, appointments, pregnancy outcome, DPDP compliance proof, ranking, lead, revenue, savings or ROI claim",
    ]:
        assert phrase in html


def test_free_business_review_routes_india_ivf_buyers_to_proof_asset():
    for relative in ["free-business-review/index.html", "free-business-review.html"]:
        html = (ROOT / relative).read_text(encoding="utf-8")
        assert 'data-review-route="india-ivf-missed-patient-calls-owner-evidence"' in html
        assert "India IVF / fertility clinics" in html
        assert "Missed patient calls + counsellor handoff review" in html
        assert RESOURCE_PATH in html
        assert "See the IVF comparison and owner dashboard" in html
