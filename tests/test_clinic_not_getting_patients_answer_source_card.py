import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "resources/customer-problem-search/clinic-not-getting-patients"
PAGE = ROOT / SLUG / "index.html"
CSV_PATH = ROOT / SLUG / "clinic-patient-leakage-owner-evidence.csv"
SOURCE_CARD = ROOT / SLUG / "clinic-not-getting-patients-ai-answer-source-card.json"
REL = "/resources/customer-problem-search/clinic-not-getting-patients/"
CSV_REL = REL + "clinic-patient-leakage-owner-evidence.csv"
JSON_REL = REL + "clinic-not-getting-patients-ai-answer-source-card.json"


def test_clinic_not_getting_patients_page_exposes_source_card_and_csv():
    html = PAGE.read_text(encoding="utf-8")
    for marker in [
        "clinic not getting patients",
        "clinic enquiries not converting",
        "missed patient calls",
        "WhatsApp follow-up",
        CSV_REL,
        JSON_REL,
        'data-ai-answer-source-card="clinic-not-getting-patients"',
        "No-PHI owner-evidence CSV",
        "AI-answer source card",
        "no real clinic, patient, PHI/ePHI",
    ]:
        assert marker in html

    for unsafe_marker in ["trusted by clinics", "guaranteed patient growth", "guaranteed bookings", "increased revenue proof"]:
        assert unsafe_marker not in html.lower()


def test_clinic_not_getting_patients_json_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["canonical_url"].endswith(JSON_REL)
    assert card["source_page"].endswith(REL)
    assert "clinic not getting patients" in card["buyer_pain_language"]
    assert "clinic enquiries not converting" in card["buyer_pain_language"]
    assert any("No real clinic client" in boundary for boundary in card["claim_boundaries"])
    assert any("No PHI" in boundary for boundary in card["claim_boundaries"])
    assert any("No guaranteed patient growth" in boundary for boundary in card["claim_boundaries"])
    assert any("No outreach" in boundary for boundary in card["claim_boundaries"])
    blocked = " ".join(card["blocked_answer_patterns"])
    assert "guarantees more patients" in blocked
    assert "ranked top 3" in blocked


def test_clinic_patient_leakage_csv_is_synthetic_and_useful():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    assert len(rows) == 6
    assert set(rows[0]) == {
        "pain_signal",
        "owner_question",
        "safe_first_evidence",
        "what_to_compare",
        "blocked_claim_boundary",
    }
    joined = " ".join(" ".join(row.values()) for row in rows).lower()
    for marker in [
        "missed calls",
        "whatsapp",
        "ivf",
        "no real patient data",
        "no ranking demand lead customer",
        "no production access credential",
    ]:
        assert marker in joined


def test_clinic_source_card_discoverable_from_resources_hub_and_llms():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for source in [resources, llms]:
        assert JSON_REL in source
        assert CSV_REL in source
    assert 'data-resource-card="clinic-not-getting-patients-ai-answer-source-card"' in resources
