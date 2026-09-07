from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "index.html"
CSV = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "healthcare-ai-patient-growth-owner-evidence.csv"


def test_healthcare_patient_growth_page_has_conversion_route_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        'href="/free-business-review/?package=healthcare-ai-patient-growth-platform&amp;source=resource-healthcare-ai-patient-growth-platform"',
        'href="/pricing.html#fixed-scope-diagnostics"',
        'href="/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-owner-evidence.csv"',
        "no real client",
        "no PHI",
        "no personal data",
        "no revenue",
        "no ROI",
        "not legal, privacy, security, medical, procurement or FinOps advice",
        "No outreach is sent",
        "Human review is required",
        "stop-rule matrix",
    ]
    for marker in required:
        assert marker in html


def test_healthcare_patient_growth_owner_evidence_csv_is_buyer_safe_template():
    csv = CSV.read_text(encoding="utf-8")
    assert csv.startswith("check_id,owner_question,evidence_to_collect,stop_rule,proof_boundary")
    assert "Synthetic template only; no real patient or clinic data" in csv
    assert "No outcome ROI booking or medical result claim" in csv
    assert "Stop if clinical triage symptoms diagnosis or emergency content appears" in csv
