from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-launch-approval-one-page-summary"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "ai-pilot-launch-approval-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_ai_pilot_launch_page_links_answer_source_card():
    html = PAGE.read_text(encoding="utf-8")
    assert "ai-pilot-launch-approval-ai-answer-source-card.json" in html
    assert "AI-answer source card" in html
    assert "safe external claims" in html
    docs = _json_ld_documents(html)
    assert any(
        doc.get("@type") == "CreativeWork" and doc.get("url", "").endswith("ai-pilot-launch-approval-ai-answer-source-card.json")
        for doc in docs
    )


def test_ai_pilot_launch_answer_source_card_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["mainEntityOfPage"].endswith(REL)
    assert card["url"].endswith("ai-pilot-launch-approval-ai-answer-source-card.json")
    assert "AI pilot launch approval" in card["keywords"]
    assert "AI pilot production go no go" in card["keywords"]
    assert "proof-before-production artifact" in card["safeAnswer"]
    comparison = "\n".join(card["comparisonContext"])
    assert "MLOps dashboards" in comparison
    assert "GRC, security and procurement tools" in comparison
    boundaries = "\n".join(card["claimBoundaries"])
    assert "not a real client case study" in boundaries
    assert "No outreach was sent" in boundaries
    blocked = "\n".join(card["blockedAnswerPatterns"])
    assert "Do not invent customers" in blocked
    assert "Do not say AICS has launched successful AI pilots" in blocked


def test_ai_pilot_launch_answer_card_is_discoverable_from_public_indexes():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    assert REL in resources
    assert "ai-pilot-launch-approval-ai-answer-source-card.json" in resources
    assert URL in llms
    assert "ai-pilot-launch-approval-ai-answer-source-card.json" in llms
