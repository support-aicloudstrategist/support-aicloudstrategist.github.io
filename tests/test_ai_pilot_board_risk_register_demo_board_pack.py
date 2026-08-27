from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-board-risk-register-demo-board-pack"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_ai_pilot_board_risk_register_demo_board_pack_exists_with_synthetic_boundary():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot board risk register demo board pack" in html
    assert "Synthetic risk-register rows" in html
    assert "Scale" in html
    assert "Remediate" in html
    assert "Pause" in html
    assert "not a real customer case study" in html
    assert "fictional examples only" in html
    assert "No outreach was sent" in html
    assert URL in html


def test_ai_pilot_board_risk_register_demo_board_pack_discovery_links():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert "/resources/global-ai-pilot-board-risk-register-review-diagnostic-package/" in html
    assert "/resources/global-ai-pilot-board-risk-register-template/" in html
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
