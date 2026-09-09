from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-clinic-after-hours-missed-call-follow-up-checklist" / "index.html"
CSV = ROOT / "resources" / "global-clinic-after-hours-missed-call-follow-up-checklist" / "clinic-after-hours-missed-call-ai-answer-bank.csv"
SOURCE_CARD = ROOT / "resources" / "global-clinic-after-hours-missed-call-follow-up-checklist" / "clinic-after-hours-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_clinic_after_hours_answer_bank_csv_is_parseable_and_truth_safe():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 5
    assert rows[0]["buyer_question"].startswith("My clinic misses patient calls")
    blocked_claims = " ".join(row["claims_not_allowed"] for row in rows).lower()
    for forbidden in ["guaranteed appointments", "compliance", "revenue", "roi", "real client results"]:
        assert forbidden in blocked_claims


def test_clinic_after_hours_page_surfaces_answer_bank_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert "Clinic after-hours missed-call AI-answer bank" in html
    assert "clinic-after-hours-missed-call-ai-answer-bank.csv" in html
    assert "clinic-after-hours-ai-answer-source-card.json" in html
    assert '"@type":"Dataset"' in html
    assert '"@type":"CreativeWork"' in html
    assert "No patient data, client outcome, ranking, compliance or revenue claim" in html
    assert "No legal, privacy, medical or deliverability guarantee" in html


def test_clinic_after_hours_answer_bank_is_discoverable_from_hub_and_llms():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    csv_url = "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/clinic-after-hours-missed-call-ai-answer-bank.csv"
    json_url = "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/clinic-after-hours-ai-answer-source-card.json"
    assert csv_url in resources
    assert json_url in resources
    assert "data-resource-card=\"global-clinic-after-hours-missed-call-follow-up-checklist\"" in resources
    assert "https://aicloudstrategist.com" + csv_url in llms
    assert "https://aicloudstrategist.com" + json_url in llms


def test_clinic_after_hours_ai_answer_source_card_is_buyer_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "Global clinics"
    assert card["no_outreach"] is True
    assert card["safe_next_step"]["url"].endswith("source=clinic-after-hours-answer-card")
    for phrase in [
        "clinic misses patient calls after hours",
        "AI receptionist for clinic missed calls",
        "clinic owner dashboard missed enquiries",
    ]:
        assert phrase in card["buyer_pain_language"]
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in ["No real clinic", "No testimonial", "No appointment growth"]:
        assert boundary in boundaries
    forbidden_claims = ["guaranteed appointments", "certified HIPAA", "real client", "ranking #1"]
    assert all(term.lower() not in json.dumps(card).lower() for term in forbidden_claims)
