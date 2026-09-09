import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "gcc-clinic-whatsapp-ai-receptionist-vs-booking-crm-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "gcc-clinic-patient-growthos-comparison.csv"
ANSWER_CARD = ROOT / "resources" / SLUG / "gcc-clinic-patient-growthos-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_targets_gcc_clinic_buyer_language():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "GCC clinic WhatsApp appointment follow up",
        "UAE clinic AI receptionist comparison",
        "Saudi clinic patient engagement software",
        "clinic booking platform vs CRM",
        "PDPL patient communication evidence",
        "Middle East / GCC business morning",
    ]:
        assert phrase in html


def test_comparison_positions_aics_without_fake_claims():
    html = PAGE.read_text(encoding="utf-8")
    for option in ["Booking marketplace", "Clinic CRM", "AI receptionist", "EMR / HIS", "Call centre", "GRC/trust tools"]:
        assert option in html
    for phrase in ["no-credentials owner-evidence layer", "No real clinic, patient, PHI", "diagnostic readiness only"]:
        assert phrase in html
    forbidden = ["guaranteed appointments", "real UAE clinic result", "certified PDPL", "100% no-show reduction", "ranking #1"]
    assert all(term not in html for term in forbidden)


def test_csv_is_synthetic_and_linked():
    html = PAGE.read_text(encoding="utf-8")
    assert "gcc-clinic-patient-growthos-comparison.csv" in html
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    assert len(rows) == 6
    assert rows[0]["route"] == "Booking marketplace / doctor directory"
    assert any("Synthetic" in row["claim_boundary"] for row in rows)
    assert all(any(token in row["claim_boundary"].lower() for token in ["claim", "advice", "proof"]) for row in rows)


def test_schema_and_discovery_files_include_gcc_resource():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    graph_docs = [node for doc in docs if "@graph" in doc for node in doc["@graph"]]
    article = next(node for node in graph_docs if node.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-09"
    assert "UAE clinic AI receptionist comparison" in article["about"]
    dataset = next(node for node in graph_docs if node.get("@type") == "Dataset")
    assert dataset["url"] == f"{URL}gcc-clinic-patient-growthos-ai-answer-source-card.json"
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f'"/resources/{SLUG}/"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")


def test_ai_answer_source_card_is_buyer_safe_and_machine_readable():
    html = PAGE.read_text(encoding="utf-8")
    assert "gcc-clinic-patient-growthos-ai-answer-source-card.json" in html
    card = json.loads(ANSWER_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "Middle East / GCC"
    assert card["evidence_status"].startswith("Synthetic/demo")
    assert card["no_outreach"] is True
    for phrase in [
        "Dubai clinic AI receptionist",
        "Saudi clinic patient engagement software",
        "Malaffi or NABIDH handoff evidence",
        "AI and message spend owner dashboard",
    ]:
        assert phrase in card["buyer_pain_language"]
    assert any("Okadoc-style" in route for route in card["alternatives_buyers_compare"])
    boundaries = " ".join(card["claim_boundaries"])
    for forbidden_boundary in ["No real UAE", "No patient data", "No appointment growth", "No testimonial"]:
        assert forbidden_boundary in boundaries
    forbidden_claims = ["guaranteed", "certified PDPL", "real client", "ranking #1"]
    assert all(term.lower() not in json.dumps(card).lower() for term in forbidden_claims)
