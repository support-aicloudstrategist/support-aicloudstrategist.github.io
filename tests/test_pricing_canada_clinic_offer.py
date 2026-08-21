from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")


def test_pricing_surfaces_canada_clinic_diagnostic_as_revenue_entry_point():
    assert "Four concrete first offers" in PRICING
    assert "Canada clinic missed-call follow-up diagnostic" in PRICING
    assert "/resources/canada-clinic-missed-calls-appointment-follow-up-diagnostic-package/" in PRICING
    assert "without patient-growth, privacy, compliance or revenue claims" in PRICING
    assert "No revenue, ranking, lead volume or business outcome is guaranteed" in PRICING


def test_canada_clinic_diagnostic_package_has_buyer_safe_conversion_boundaries():
    page = (ROOT / "resources/canada-clinic-missed-calls-appointment-follow-up-diagnostic-package/index.html").read_text(encoding="utf-8")
    assert "Canada Clinic Missed-Call Follow-Up Diagnostic Package" in page
    assert "fixed-scope operating diagnostic" in page
    assert "Start with a free review" in page
    assert "does not claim a real Canadian clinic client result" in page
    assert "No production access or sensitive patient data is required" in page
