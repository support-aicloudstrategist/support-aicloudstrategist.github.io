from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/us-specialty-clinic-patient-access-cloud-trust-diagnostic-package/"
CSV = "/resources/us-specialty-clinic-patient-access-cloud-trust-diagnostic-package/us-specialty-clinic-diagnostic-scope-matrix.csv"
PACKAGE = "us-specialty-clinic-patient-access-cloud-trust-diagnostic-package"


def test_pricing_exposes_us_specialty_patient_access_cloud_trust_package_as_fixed_scope_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert "Twenty-one concrete first offers" in section
    assert '"numberOfItems":21' in html
    assert f'data-revenue-bridge="{PACKAGE}"' in section
    assert "US specialty clinic Patient Access + Cloud Trust diagnostic package" in section
    assert "Scope before RCM/prior-auth automation, patient-engagement, AI receptionist" in section
    assert RESOURCE in section
    assert CSV in section
    assert f"/free-business-review/?package={PACKAGE}&amp;source=pricing-fixed-scope" in section
    assert "no patient data, payer files, EHR/PMS export, cloud credentials" in section
    assert "ranking, demand, revenue, savings, ROI or outcome claim" in section


def test_free_review_routes_us_specialty_patient_access_cloud_trust_buyers_on_both_entrypoints():
    for path in (FREE_REVIEW, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert f'data-review-route="{PACKAGE}"' in workflow
        assert "US specialty clinics / patient access + cloud trust" in workflow
        assert "no-PHI/ePHI scope matrix before platform or MSP spend" in workflow
        assert RESOURCE in workflow
        assert CSV in workflow
        assert "/pricing.html#fixed-scope-diagnostics" in workflow


def test_free_review_flat_file_stays_identical_to_directory_version_after_us_specialty_route():
    assert FREE_REVIEW.read_text(encoding="utf-8") == FREE_REVIEW_FLAT.read_text(encoding="utf-8")
