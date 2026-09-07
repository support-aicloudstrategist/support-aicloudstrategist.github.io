from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pricing_has_us_healthcare_patient_access_comparison_bridge():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    assert 'data-revenue-bridge="us-healthcare-patient-access-comparison"' in html
    assert "Scope before AI receptionist, patient engagement, RCM/prior-auth automation, GRC/trust-centre or FinOps platform spend" in html
    assert "/resources/us-healthcare-patient-access-vs-ai-receptionist-rcm-comparison/" in html
    assert "free-business-review/?package=us-healthcare-patient-access-comparison" in html
    assert "no real medical group" in html
    assert "revenue, savings, ROI or AI-accuracy claim" in html


def test_free_review_has_us_healthcare_patient_access_route_in_both_entrypoints():
    for rel in ["free-business-review/index.html", "free-business-review.html"]:
        html = (ROOT / rel).read_text(encoding="utf-8")
        assert 'data-review-route="us-healthcare-patient-access-comparison"' in html
        assert "Patient-access comparison fit check" in html
        assert "/resources/us-healthcare-patient-access-vs-ai-receptionist-rcm-comparison/us-healthcare-patient-access-comparison-matrix.csv" in html
        assert "/resources/us-healthcare-patient-access-vs-ai-receptionist-rcm-comparison/us-healthcare-patient-access-comparison-map.svg" in html
