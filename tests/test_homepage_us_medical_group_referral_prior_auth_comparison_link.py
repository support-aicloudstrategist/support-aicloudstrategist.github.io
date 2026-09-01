from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "us-medical-group-referral-prior-auth-vs-patient-engagement-rcm-ai-receptionist-comparison" / "index.html"


def test_homepage_surfaces_medical_group_referral_prior_auth_comparison():
    homepage = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/us-medical-group-referral-prior-auth-vs-patient-engagement-rcm-ai-receptionist-comparison/"

    assert href in homepage
    assert "US Medical Group Referral + Prior Auth vs Patient Engagement, RCM and AI Receptionist Tools" in homepage
    assert "Open the medical group referral + prior auth comparison" in homepage
    assert "tool-neutral, no-PHI comparison" in homepage
    assert "link rel=\"canonical\" href=\"https://aicloudstrategist.com/resources/us-medical-group-referral-prior-auth-vs-patient-engagement-rcm-ai-receptionist-comparison/\"" in resource
