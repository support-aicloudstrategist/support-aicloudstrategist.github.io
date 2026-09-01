from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/us-outpatient-specialty-referral-prior-auth-growthos-evidence-checklist/"


def test_free_review_routes_outpatient_specialty_buyers_to_growthos_checklist():
    for path in (FREE_REVIEW, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert 'data-review-route="us-outpatient-referral-prior-auth-growthos"' in workflow
        assert "US medical groups / outpatient specialty" in workflow
        assert "Referral + prior-auth owner-handoff review" in workflow
        assert "See the outpatient GrowthOS checklist" in workflow
        assert RESOURCE in workflow
        assert "See the no-PHI handoff FAQ" in workflow
        assert "Compare buyer routes" in workflow


def test_free_review_canonical_and_flat_page_stay_identical():
    assert FREE_REVIEW.read_text(encoding="utf-8") == FREE_REVIEW_FLAT.read_text(encoding="utf-8")
