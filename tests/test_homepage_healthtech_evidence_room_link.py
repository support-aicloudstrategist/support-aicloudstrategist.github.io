from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "north-america-healthtech-ai-cloud-finops-trust-evidence-room" / "index.html"


def test_homepage_surfaces_healthtech_ai_finops_evidence_room():
    home = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/north-america-healthtech-ai-cloud-finops-trust-evidence-room/"
    assert href in home
    assert "Healthtech AI Cloud FinOps Trust Evidence Room" in home
    assert "Buyer evidence room · 2026-08-24" in home
    assert 'href="/resources/north-america-healthtech-ai-cloud-finops-trust-evidence-room/"' in home
    assert "not a client case study" in resource
