from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "global-clinic-after-hours-missed-call-follow-up-checklist" / "index.html"


def test_homepage_surfaces_clinic_after_hours_missed_call_checklist():
    home = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/"
    assert href in home
    assert "Clinic After-Hours Missed-Call Follow-Up Checklist" in home
    assert "Buyer leakage checklist · 2026-08-25" in home
    assert 'href="/resources/global-clinic-after-hours-missed-call-follow-up-checklist/"' in home
    assert "does not claim AICS clients, testimonials, certifications, partnerships, guaranteed appointment growth, patient outcomes, revenue lift" in resource