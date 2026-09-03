from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/us-specialty-clinic-security-questionnaire-answer-source-map/"
CSV = "/resources/us-specialty-clinic-security-questionnaire-answer-source-map/us-specialty-clinic-security-questionnaire-answer-source-map.csv"
SVG = "/resources/us-specialty-clinic-security-questionnaire-answer-source-map/us-specialty-clinic-security-questionnaire-owner-matrix.svg"
PROBLEM = "us-specialty-clinic-security-questionnaire-map"


def test_pricing_routes_us_specialty_security_questionnaire_buyers_to_diagnostic_fit_check():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert 'data-revenue-bridge="us-specialty-clinic-security-questionnaire-map"' in section
    assert "US specialty clinic security-questionnaire evidence diagnostic bridge" in section
    assert "Scope before AI receptionist, patient engagement, RCM/prior-auth" in section
    assert RESOURCE in section
    assert CSV in section
    assert f"/free-business-review/?problem={PROBLEM}&amp;source=pricing-fixed-scope" in section
    assert "no patient data, payer files, EHR/PMS access" in section
    assert "ranking, revenue, savings, ROI or outcome claim" in section


def test_free_review_routes_us_specialty_clinics_to_no_phi_matrix_on_both_entrypoints():
    for path in (FREE_REVIEW, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert 'data-review-route="us-specialty-clinic-security-questionnaire-map"' in workflow
        assert "US specialty clinics / patient-access teams" in workflow
        assert "no-PHI/ePHI owner matrix before vendor spend" in workflow
        assert RESOURCE in workflow
        assert CSV in workflow
        assert SVG in workflow


def test_free_review_flat_file_stays_identical_to_directory_version():
    assert FREE_REVIEW.read_text(encoding="utf-8") == FREE_REVIEW_FLAT.read_text(encoding="utf-8")
