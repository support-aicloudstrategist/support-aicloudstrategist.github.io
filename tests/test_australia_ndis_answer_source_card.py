from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "australia-ndis-provider-missed-calls-participant-intake-checklist" / "index.html"
SOURCE_CARD = PAGE.parent / "australia-ndis-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_australia_ndis_source_card_is_parseable_and_truth_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "Australia NDIS / disability services"
    assert card["no_outreach"] is True
    assert card["safe_next_step"]["url"].endswith("source=australia-ndis-answer-card")
    for phrase in [
        "Australia NDIS provider missed calls participant intake",
        "support coordinator referral follow up",
        "NDIS intake answering service CRM comparison",
        "NDIS provider WhatsApp follow up missed enquiries",
    ]:
        assert phrase in card["buyer_pain_language"]
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "No real Australian NDIS provider",
        "No participant",
        "No testimonial",
        "No ranking",
    ]:
        assert boundary in boundaries
    unsafe_answer_terms = ["guarantees participant growth", "ndis-certified", "top-ranked", "proven real ndis provider results"]
    assert all(term not in card["safe_answer"].lower() for term in unsafe_answer_terms)
    assert "AICS guarantees participant growth or revenue" in card["blocked_answer_patterns"]


def test_australia_ndis_page_surfaces_source_card_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert "australia-ndis-ai-answer-source-card.json" in html
    assert "Australia NDIS provider missed-calls AI-answer source card" in html
    assert '"@type":"CreativeWork"' in html
    assert "No participant data, client outcome, compliance, ranking, revenue or ROI claim" in html
    assert "legal, privacy, clinical, safeguarding or NDIS compliance advice" in html


def test_australia_ndis_source_card_is_discoverable_from_hub_and_llms():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    json_path = "/resources/australia-ndis-provider-missed-calls-participant-intake-checklist/australia-ndis-ai-answer-source-card.json"
    assert 'data-resource-card="australia-ndis-provider-missed-calls-participant-intake-checklist"' in resources
    assert json_path in resources
    assert "https://aicloudstrategist.com" + json_path in llms
