from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "cloud-ai-economics-decision-pack"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CARD = ROOT / "resources" / SLUG / "cloud-ai-economics-decision-pack-ai-answer-source-card.json"


def test_cloud_ai_economics_decision_pack_routes_answer_source_card():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert "Cloud &amp; AI Economics Decision Pack" in source
    assert "not a savings promise" in source
    assert "No billing files, credentials or work email are required" in source
    assert "cloud-ai-economics-decision-pack-ai-answer-source-card.json" in source


def test_cloud_ai_economics_answer_source_card_blocks_unverified_savings_claims():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["canonical_url"] == URL
    assert "contact.html?service=ai-finops-cloud-economics" in card["primary_route"]
    text = json.dumps(card).lower()
    for phrase in [
        "synthetic",
        "no credentials",
        "do not claim aics saved a real customer money",
        "do not present the synthetic usd values as benchmarks",
        "no savings guarantee",
    ]:
        assert phrase in text


def test_cloud_ai_economics_source_card_is_discoverable_to_answer_engines():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in llms
    assert "cloud-ai-economics-decision-pack-ai-answer-source-card.json" in llms
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
