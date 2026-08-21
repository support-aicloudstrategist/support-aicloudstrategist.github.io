from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")


def test_pricing_surfaces_canada_clinic_diagnostic_as_revenue_entry_point():
    assert "Four concrete first offers" in PRICING
    assert "Canada clinic missed-call follow-up diagnostic" in PRICING
    assert "/free-business-review/?package=canada-clinic-missed-calls-appointment-follow-up" in PRICING
    assert "without patient-growth, privacy, compliance or revenue claims" in PRICING
    assert "No revenue, ranking, lead volume or business outcome is guaranteed" in PRICING
