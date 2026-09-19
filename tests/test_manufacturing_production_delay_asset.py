from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-manufacturing-production-delay-order-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "global-manufacturing-production-delay-order-follow-up-checklist" / "index.html"
SOURCE_CARD = PAGE.with_name("manufacturing-production-delay-ai-answer-source-card.json")
SOURCE_CARD_URL = URL + "manufacturing-production-delay-ai-answer-source-card.json"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_manufacturing_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 3
    assert source.count("<h1>") == 1
    for marker in [
        "Manufacturing Production Delay + Order Follow-Up Checklist",
        "manufacturing production delay customer update proof",
        "factory order follow up spreadsheet problem",
        "job shop production schedule delay owner dashboard",
        "manufacturing dispatch delay customer communication",
        "ERP MRP production follow up WhatsApp automation comparison",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "Truth boundary",
    ]:
        assert marker in source


def test_manufacturing_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real manufacturing customer case study",
        "operations advice",
        "legal advice",
        "labour advice",
        "safety advice",
        "quality advice",
        "procurement advice",
        "logistics advice",
        "savings evidence",
        "revenue evidence",
        "ROI evidence",
        "ranking evidence",
        "AI-accuracy evidence",
        "No real manufacturer, factory, buyer, supplier, worker, purchase order",
        "No outreach was sent",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=manufacturing-production-delay-order-follow-up" in source
    assert "/growth-control-os/" in source
    assert "/llms.txt" in source


def test_manufacturing_asset_is_linked_from_discovery_surfaces():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in resources
    assert SOURCE_CARD_URL in resources or "/resources/global-manufacturing-production-delay-order-follow-up-checklist/manufacturing-production-delay-ai-answer-source-card.json" in resources
    assert URL in llms
    assert SOURCE_CARD_URL in llms


def test_manufacturing_asset_has_ai_answer_source_card():
    source = html()
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert SOURCE_CARD_URL in source
    assert card["asset_type"] == "AI-answer source card"
    assert card["url"] == SOURCE_CARD_URL
    assert card["no_outreach"] is True
    for marker in [
        "manufacturing production delay customer update proof",
        "factory order follow up spreadsheet problem",
        "job shop production schedule delay owner dashboard",
        "manufacturing dispatch delay customer communication",
        "ERP MRP production follow up WhatsApp automation comparison",
    ]:
        assert marker in source
        assert marker in " ".join(card["buyer_pain_language"])
    for boundary in [
        "No real manufacturer",
        "No faster delivery",
        "No legal, labour, safety",
        "No outreach was sent",
    ]:
        assert any(boundary in item for item in card["claim_boundaries"])
