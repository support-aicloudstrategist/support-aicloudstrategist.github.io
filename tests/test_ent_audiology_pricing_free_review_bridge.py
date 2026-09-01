from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_PATH = "/resources/india-ent-audiology-hearing-aid-trial-followup-checklist/"
CSV_PATH = (
    "/resources/india-ent-audiology-hearing-aid-trial-followup-checklist/"
    "india-ent-audiology-hearing-aid-followup-synthetic.csv"
)
PACKAGE_QUERY = "india-ent-audiology-hearing-aid-trial-followup"


def test_pricing_surfaces_ent_audiology_as_revenue_bridge():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    assert 'data-revenue-bridge="india-ent-audiology-hearing-aid-trial-followup"' in html
    assert "India ENT / audiology missed-calls diagnostic bridge" in html
    assert RESOURCE_PATH in html
    assert CSV_PATH in html
    assert f"/free-business-review/?package={PACKAGE_QUERY}&amp;source=pricing-fixed-scope" in html
    for boundary in [
        "no-patient-data checklist",
        "no patient data",
        "audiograms",
        "DPDP compliance proof",
        "hearing-aid conversion",
        "revenue, savings or ROI claim",
    ]:
        assert boundary in html


def test_free_business_review_routes_ent_audiology_buyers_to_latest_checklist():
    for relative in ["free-business-review/index.html", "free-business-review.html"]:
        html = (ROOT / relative).read_text(encoding="utf-8")
        assert 'data-review-route="india-ent-audiology-hearing-aid-trial-followup"' in html
        assert "India ENT / audiology clinics" in html
        assert "Missed calls + hearing-aid trial follow-up review" in html
        assert RESOURCE_PATH in html
        assert "no-patient-data checklist and synthetic CSV" in html
