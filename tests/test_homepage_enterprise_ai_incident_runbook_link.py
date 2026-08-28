from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RUNBOOK = ROOT / "resources" / "global-enterprise-ai-incident-response-evidence-runbook" / "index.html"


def test_homepage_surfaces_enterprise_ai_incident_response_runbook():
    homepage = HOME.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")

    href = "/resources/global-enterprise-ai-incident-response-evidence-runbook/"

    assert href in homepage
    assert "Enterprise AI Incident Response Evidence Runbook" in homepage
    assert "Open the AI incident response runbook" in homepage
    assert "buyer-safe operating artifact" in homepage
    assert "link rel=\"canonical\" href=\"https://aicloudstrategist.com/resources/global-enterprise-ai-incident-response-evidence-runbook/\"" in runbook
