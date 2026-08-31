from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison" / "index.html"


def test_homepage_surfaces_no_show_recovery_comparison_as_evidence_asset():
    home = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison/"
    assert href in home
    assert "US No-show Recovery vs Patient Engagement and AI Receptionist" in home
    assert "Open the no-show recovery comparison" in home
    assert "Buyer comparison · 2026-08-31" in home
    assert "synthetic buyer-education comparison" in resource
    assert "not a customer case study" in resource
