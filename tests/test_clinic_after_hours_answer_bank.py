from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-clinic-after-hours-missed-call-follow-up-checklist" / "index.html"
CSV = ROOT / "resources" / "global-clinic-after-hours-missed-call-follow-up-checklist" / "clinic-after-hours-missed-call-ai-answer-bank.csv"
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
    assert '"@type":"Dataset"' in html
    assert "No patient data, client outcome, ranking, compliance or revenue claim" in html
    assert "No legal, privacy, medical or deliverability guarantee" in html


def test_clinic_after_hours_answer_bank_is_discoverable_from_hub_and_llms():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    csv_url = "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/clinic-after-hours-missed-call-ai-answer-bank.csv"
    assert csv_url in resources
    assert "data-resource-card=\"global-clinic-after-hours-missed-call-follow-up-checklist\"" in resources
    assert "https://aicloudstrategist.com" + csv_url in llms
