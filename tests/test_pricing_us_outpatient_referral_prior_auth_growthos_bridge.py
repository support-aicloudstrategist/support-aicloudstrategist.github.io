from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")


def test_us_outpatient_referral_prior_auth_growthos_revenue_bridge_visible():
    assert 'data-revenue-bridge="us-outpatient-referral-prior-auth-growthos"' in PRICING
    for phrase in [
        "US outpatient referral + prior-auth GrowthOS diagnostic bridge",
        "Scope before platform spend",
        "US outpatient specialty groups",
        "prior authorization blockers",
        "abandoned calls",
        "patient engagement, RCM, AI receptionist or call-center expansion",
        "no patient data, PHI, HIPAA attestation",
        "no patient data, PHI, HIPAA attestation, prior-authorization approval",
    ]:
        assert phrase in PRICING


def test_us_outpatient_referral_prior_auth_growthos_bridge_routes_to_assets_and_fit_check():
    for href in [
        "/resources/us-outpatient-specialty-referral-prior-auth-growthos-evidence-checklist/",
        "/resources/us-outpatient-specialty-referral-prior-auth-growthos-evidence-checklist/us-outpatient-referral-prior-auth-growthos-evidence-register.csv",
        "/free-business-review/?package=us-outpatient-referral-prior-auth-growthos&amp;source=pricing-fixed-scope",
    ]:
        assert href in PRICING


def test_existing_fixed_scope_count_contract_unchanged():
    assert "Twenty concrete first offers buyers can understand before a custom build." in PRICING
    assert '"numberOfItems":20' in PRICING
