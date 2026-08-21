from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/europe-saas-ai-evidence-room-template/index.html"
RESOURCES = ROOT / "resources/index.html"
LLMS = ROOT / "llms.txt"
SITEMAP_SCRIPT = ROOT / "scripts/build_sitemap.py"


def test_europe_saas_ai_evidence_room_template_is_buyer_safe_and_linked():
    source = PAGE.read_text(encoding="utf-8")
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/europe-saas-ai-evidence-room-template/"' in source
    assert "AI use case" in source
    assert "Data boundary" in source
    assert "Human review" in source
    assert "Cloud and AI cost ownership" in source
    assert "Adviser question" in source
    assert "not legal, privacy, DPO, audit or certification advice" in source
    assert "does not claim real client outcomes" in source
    assert source.count("data-aics-navigation-mount") == 1
    assert source.count("data-aics-global-footer") == 1

    url = "https://aicloudstrategist.com/resources/europe-saas-ai-evidence-room-template/"
    assert url in LLMS.read_text(encoding="utf-8")
    assert "/resources/europe-saas-ai-evidence-room-template/" in RESOURCES.read_text(encoding="utf-8")
    assert "/resources/europe-saas-ai-evidence-room-template/" in SITEMAP_SCRIPT.read_text(encoding="utf-8")
