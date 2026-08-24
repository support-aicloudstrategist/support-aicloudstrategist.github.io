from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "us-outpatient-imaging-referral-prior-auth-leakage-checklist" / "index.html"


def test_homepage_surfaces_outpatient_imaging_referral_leakage_checklist():
    home = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/us-outpatient-imaging-referral-prior-auth-leakage-checklist/"
    assert href in home
    assert "Outpatient Imaging Referral + Prior Auth Leakage Checklist" in home
    assert "Buyer leakage checklist · 2026-08-24" in home
    assert 'href="/resources/us-outpatient-imaging-referral-prior-auth-leakage-checklist/"' in home
    assert "It does not claim a real customer, patient data, PHI, testimonial, ranking, revenue, prior-authorization speed improvement, denial reduction or booked-study result." in resource
