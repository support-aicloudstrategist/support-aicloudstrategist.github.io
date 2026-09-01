import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-ivf-fertility-missed-patient-calls-vs-crm-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
QUESTIONNAIRE = PAGE.parent / "india-ivf-owner-handoff-questionnaire.csv"
QUESTIONNAIRE_URL = f"https://aicloudstrategist.com/resources/{SLUG}/india-ivf-owner-handoff-questionnaire.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_ivf_owner_handoff_questionnaire_is_linked_and_described():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "india-ivf-owner-handoff-questionnaire.csv",
        "Download owner handoff questionnaire",
        "safe, non-patient evidence",
        "human-review stops",
        "consent/notice questions",
    ]:
        assert phrase in html


def test_ivf_owner_handoff_questionnaire_dataset_schema_is_present():
    html = PAGE.read_text(encoding="utf-8")
    datasets = [doc for doc in json_ld_documents(html) if doc.get("@type") == "Dataset"]
    questionnaire = next(doc for doc in datasets if doc.get("url") == QUESTIONNAIRE_URL)
    assert questionnaire["name"] == "Synthetic India IVF owner handoff questionnaire"
    assert "no-patient-data questionnaire" in questionnaire["description"]
    assert "IVF owner handoff questionnaire" in questionnaire["keywords"]


def test_ivf_owner_handoff_questionnaire_is_synthetic_and_no_patient_data():
    rows = list(csv.DictReader(QUESTIONNAIRE.open(encoding="utf-8")))
    assert len(rows) == 5
    assert {row["section"] for row in rows} == {
        "Intake routes",
        "Ownership",
        "Human-review stops",
        "Consent and notice",
        "Closure proof",
    }
    forbidden = ["patient names", "phone numbers", "treatment history", "medical reports", "appointment records"]
    for row in rows:
        assert row["safe_non_patient_evidence"]
        assert row["unsafe_do_not_send"]
        assert row["claim_boundary"]
    assert all(term not in " ".join(row["safe_non_patient_evidence"].lower() for row in rows) for term in forbidden)
    assert any("No DPDP compliance claim" in row["claim_boundary"] for row in rows)


def test_llms_txt_exposes_ivf_questionnaire_for_ai_discovery():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert QUESTIONNAIRE_URL in llms
    assert "no-patient-data owner handoff questionnaire" in llms
