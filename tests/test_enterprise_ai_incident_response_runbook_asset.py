from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "resources" / "global-enterprise-ai-incident-response-evidence-runbook" / "index.html"
RESOURCES_INDEX = ROOT / "resources" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"


def test_enterprise_ai_incident_response_runbook_is_publicly_discoverable():
    page = RESOURCE.read_text(encoding="utf-8")
    resources = RESOURCES_INDEX.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    url = "https://aicloudstrategist.com/resources/global-enterprise-ai-incident-response-evidence-runbook/"
    href = "/resources/global-enterprise-ai-incident-response-evidence-runbook/"

    assert "Enterprise AI incident response evidence runbook" in page
    assert "enterprise AI incident response runbook" in page
    assert "AI agent incident response checklist" in page
    assert "LLM application rollback evidence" in page
    assert "No real customer, incident, breach" in page
    assert "not legal, cybersecurity, insurance, clinical, financial or regulatory advice" in page
    assert f'link rel="canonical" href="{url}"' in page
    assert href in resources
    assert url in sitemap
    assert url in llms
