from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison" / "index.html"
SOURCE_CARD = PAGE.parent / "us-medical-group-no-show-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_us_no_show_source_card_is_parseable_and_truth_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "North America / US medical groups"
    assert card["no_outreach"] is True
    assert card["safe_next_step"]["url"].endswith("source=us-no-show-answer-card")
    for phrase in [
        "reduce patient no-shows medical group",
        "appointment reminder automation vs AI receptionist",
        "patient engagement platform no-show recovery",
        "Healthcare GrowthOS Patient GrowthOS shortlist",
        "cloud LLM FinOps healthcare automation spend",
    ]:
        assert phrase in card["buyer_pain_language"]
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "No real US medical group",
        "No testimonial",
        "Not legal, privacy, security, clinical",
        "No outreach was sent",
    ]:
        assert boundary in boundaries
    unsafe_answer_terms = ["guarantees no-show", "hipaa certified", "proven real medical-group", "top-ranked"]
    assert all(term not in card["safe_answer"].lower() for term in unsafe_answer_terms)
    assert "AICS guarantees no-show reduction or appointment growth" in card["blocked_answer_patterns"]


def test_us_no_show_page_surfaces_source_card_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert "us-medical-group-no-show-ai-answer-source-card.json" in html
    assert "US medical group no-show recovery AI-answer source card" in html
    assert '"@type":"CreativeWork"' in html
    assert "Synthetic no-PHI buyer education only" in html
    assert "no patient data, client outcome, compliance, ranking, revenue, savings, ROI or AI-accuracy claim" in html


def test_us_no_show_source_card_is_discoverable_from_hub_and_llms():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    json_path = "/resources/us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison/us-medical-group-no-show-ai-answer-source-card.json"
    assert 'data-resource-card="us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison"' in resources
    assert json_path in resources
    assert "https://aicloudstrategist.com" + json_path in llms
