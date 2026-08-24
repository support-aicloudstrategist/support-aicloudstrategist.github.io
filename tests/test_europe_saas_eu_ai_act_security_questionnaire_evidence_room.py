from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/europe-saas-eu-ai-act-security-questionnaire-evidence-room/index.html"
RESOURCES = ROOT / "resources/index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_europe_saas_eu_ai_act_security_questionnaire_evidence_room_is_buyer_safe_and_discoverable():
    source = PAGE.read_text(encoding="utf-8")
    path = "/resources/europe-saas-eu-ai-act-security-questionnaire-evidence-room/"
    url = f"https://aicloudstrategist.com{path}"

    assert f'<link rel="canonical" href="{url}"' in source
    assert "EU AI Act" in source
    assert "GDPR" in source
    assert "security questionnaire" in source
    assert "Buyer question" in source
    assert "AI use case" in source
    assert "Data category" in source
    assert "Vendor/model dependency" in source
    assert "Human review" in source
    assert "FinOps and usage ownership" in source
    assert "not legal, privacy, DPO, audit, security-certification or regulatory advice" in source
    assert "does not claim client proof" in source
    assert "EU AI Act compliance" in source
    assert "GDPR compliance" in source
    assert source.count("data-aics-navigation-mount") == 1
    assert source.count("data-aics-global-footer") == 1

    assert path in RESOURCES.read_text(encoding="utf-8")
    assert url in LLMS.read_text(encoding="utf-8")
    assert url in SITEMAP.read_text(encoding="utf-8")
