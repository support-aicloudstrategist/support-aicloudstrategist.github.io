import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "canada-clinic-missed-calls-appointment-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_FILE = ROOT / "resources" / SLUG / "canada-clinic-missed-calls-owner-evidence.csv"
SVG_FILE = ROOT / "resources" / SLUG / "canada-clinic-missed-calls-owner-board.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_canada_clinic_page_exposes_synthetic_owner_evidence_pack():
    html = PAGE.read_text(encoding="utf-8")
    assert "missed patient calls" in html
    assert "Download the owner-evidence pack" in html
    assert "canada-clinic-missed-calls-owner-evidence.csv" in html
    assert "canada-clinic-missed-calls-owner-board.svg" in html
    assert "patient names" in html
    assert "not proof of patient growth, booked appointments, compliance, advertising performance, revenue or ROI" in html
    assert "dateModified\":\"2026-09-04" in html
    assert "https://aicloudstrategist.com/resources/canada-clinic-missed-calls-appointment-follow-up-checklist/canada-clinic-missed-calls-owner-board.svg" in html


def test_canada_clinic_json_ld_has_dataset_and_image_object():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    dataset = next(doc for doc in docs if doc.get("@type") == "Dataset")
    image = next(doc for doc in docs if doc.get("@type") == "ImageObject")
    assert dataset["name"] == "Canada clinic missed-call owner evidence CSV"
    assert dataset["isAccessibleForFree"] is True
    assert "PIPEDA PHIPA questions" in dataset["keywords"]
    assert image["contentUrl"].endswith("canada-clinic-missed-calls-owner-board.svg")
    assert "no-patient-data" in image["caption"]


def test_canada_clinic_csv_and_svg_are_buyer_safe():
    rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8")))
    assert len(rows) == 10
    assert rows[0]["evidence_area"] == "missed_call_capture"
    assert any("not PHIPA/PIPEDA/legal advice" in row["no_patient_data_boundary"] for row in rows)
    svg = SVG_FILE.read_text(encoding="utf-8")
    assert "Demo / synthetic only" in svg
    assert "no patient names" in svg
    assert "AI receptionist, answering service, CRM or more ads" in svg


def test_canada_clinic_pack_is_discoverable_from_hub_and_llms():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    for content in (resources, llms):
        assert f"/resources/{SLUG}/" in content or f"https://aicloudstrategist.com/resources/{SLUG}/" in content
        assert "canada-clinic-missed-calls-owner-evidence.csv" in content
        assert "canada-clinic-missed-calls-owner-board.svg" in content
