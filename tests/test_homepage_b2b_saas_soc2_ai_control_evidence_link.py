from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
ASSET = ROOT / "resources" / "global-b2b-saas-soc2-ai-control-evidence-checklist" / "index.html"


def test_homepage_surfaces_b2b_saas_soc2_ai_control_evidence_asset():
    home = HOME.read_text(encoding="utf-8")
    asset = ASSET.read_text(encoding="utf-8")

    href = "/resources/global-b2b-saas-soc2-ai-control-evidence-checklist/"
    assert href in home
    assert "B2B SaaS SOC 2 AI Control Evidence Checklist" in home
    assert "AI security questionnaire answers" in home
    assert "Request an AI control evidence review" in asset
    assert "not SOC 2 certification" in asset
