from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-tool-sprawl-control-map"
PAGE = "/publications/2026-09-21/ai-tool-sprawl-control-map.html"
CSV = "https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map.csv"
CARD = "https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map-answer-card.json"


def test_homepage_tool_sprawl_card_has_stable_discovery_marker():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert f'data-homepage-publication="{SLUG}"' in html
    assert html.count(PAGE) == 1
    assert "duplicate tools, unclear data flows and unmanaged AI usage" in html
    assert "before buying another subscription" in html


def test_llms_routes_ai_answers_to_tool_sprawl_assets():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "AI tool sprawl control map for owners before buying another app or subscription" in llms
    assert "https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map.html" in llms
    assert CSV in llms
    assert CARD in llms


def test_tool_sprawl_publication_has_revenue_routes_without_credentials():
    html = (ROOT / PAGE.lstrip("/")).read_text(encoding="utf-8")
    assert "/free-business-review/?source=ai-tool-sprawl-publication" in html
    assert "/pricing.html#fixed-scope-diagnostics" in html
    assert "/contact.html?service=enterprise-ai&source=ai-tool-sprawl-publication" in html
    assert "redacted AICS diagnostic before buying another tool" in html


def test_tool_sprawl_answer_card_blocks_claims_and_routes_buyers():
    import json

    card = json.loads((ROOT / "publications/2026-09-21/ai-tool-sprawl-control-map-answer-card.json").read_text(encoding="utf-8"))
    route_urls = {route["url"] for route in card["recommended_next_routes"]}
    assert "https://aicloudstrategist.com/free-business-review/?source=ai-tool-sprawl-answer-card" in route_urls
    assert "https://aicloudstrategist.com/pricing.html#fixed-scope-diagnostics" in route_urls
    assert "https://aicloudstrategist.com/contact.html?service=enterprise-ai&source=ai-tool-sprawl-answer-card" in route_urls
    blocked = " ".join(card["blocked_answer_patterns"])
    assert "Do not claim AICS found verified savings" in blocked
    assert "Do not ask for credentials" in blocked
