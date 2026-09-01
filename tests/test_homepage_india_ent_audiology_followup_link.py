from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "india-ent-audiology-hearing-aid-trial-followup-checklist" / "index.html"


def test_homepage_surfaces_india_ent_audiology_followup_checklist():
    homepage = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/india-ent-audiology-hearing-aid-trial-followup-checklist/"

    assert href in homepage
    assert "India ENT / Audiology Missed Calls + Hearing Aid Trial Follow-up Checklist" in homepage
    assert "Open the ENT / audiology follow-up checklist" in homepage
    assert "synthetic, no-patient-data checklist" in homepage
    assert "link rel=\"canonical\" href=\"https://aicloudstrategist.com/resources/india-ent-audiology-hearing-aid-trial-followup-checklist/\"" in resource
