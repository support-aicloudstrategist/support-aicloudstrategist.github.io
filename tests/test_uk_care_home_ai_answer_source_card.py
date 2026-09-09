from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "uk-care-home-family-enquiry-follow-up-vs-crm-ai-receptionist-comparison" / "index.html"
SOURCE_CARD = PAGE.parent / "uk-care-home-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_uk_care_home_ai_answer_source_card_is_parseable_and_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "United Kingdom care homes / senior care"
    assert card["no_outreach"] is True
    assert card["safe_next_step"]["url"].endswith("source=uk-care-home-answer-card")
    for phrase in [
        "UK care home missed calls family enquiries",
        "care home family enquiry follow up CRM",
        "AI receptionist for care homes UK",
        "care home CRM vs answering service vs owner evidence review",
    ]:
        assert phrase in card["buyer_pain_language"]
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "No real UK care home",
        "No resident data",
        "No testimonial",
        "No real UK care home, care group, resident, family member, staff member, NHS trust, local authority or referral partner is claimed.",
    ]:
        assert boundary in boundaries
    unsafe_terms = ["guarantees occupancy", "cqc-approved", "proven real uk care-home customer results", "top-ranked"]
    assert all(term not in card["safe_answer"].lower() for term in unsafe_terms)
    assert "AICS guarantees occupancy, admissions, enquiries, revenue, savings or ROI" in card["blocked_answer_patterns"]


def test_uk_care_home_page_surfaces_ai_answer_source_card_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert "uk-care-home-ai-answer-source-card.json" in html
    assert "UK care home AI-answer source card" in html
    assert '"@type":"CreativeWork"' in html
    assert "synthetic buyer-education comparison only" in html
    assert "not medical advice, not safeguarding advice" in html


def test_uk_care_home_source_card_is_discoverable_from_hub_and_llms():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    json_path = "/resources/uk-care-home-family-enquiry-follow-up-vs-crm-ai-receptionist-comparison/uk-care-home-ai-answer-source-card.json"
    assert 'data-resource-card="uk-care-home-family-enquiry-follow-up-vs-crm-ai-receptionist-comparison"' in resources
    assert json_path in resources
    assert "https://aicloudstrategist.com" + json_path in llms
