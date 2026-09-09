import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-diagnostic-lab-report-delay-whatsapp-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_FILE = ROOT / "resources" / SLUG / "diagnostic-lab-report-follow-up-owner-evidence.csv"
SVG_FILE = ROOT / "resources" / SLUG / "diagnostic-lab-report-follow-up-owner-board.svg"
JSON_CARD = ROOT / "resources" / SLUG / "diagnostic-lab-report-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_diagnostic_lab_report_followup_page_has_buyer_language_and_truth_boundary():
    html = PAGE.read_text(encoding="utf-8")
    assert "diagnostic lab report delay WhatsApp follow up" in html
    assert "pathology lab report status calls" in html
    assert "lab report pickup automation India" in html
    assert "sample collection follow-up" in html
    assert "DPDP checklist diagnostic lab WhatsApp" in html
    assert "No real diagnostic lab" in html
    assert "No outreach was sent" not in html  # this asset is a synthetic checklist, not an outreach log
    assert "provides no legal, privacy, security, medical, laboratory, clinical, diagnostic, billing, advertising, procurement or compliance advice" in html
    assert "dateModified\":\"2026-09-09" in html


def test_diagnostic_lab_report_followup_json_ld_has_article_dataset_creativework_and_faq():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    types = {doc.get("@type") for doc in docs}
    assert {"Article", "Dataset", "CreativeWork", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if doc.get("@type") == "Article")
    dataset = next(doc for doc in docs if doc.get("@type") == "Dataset")
    source_card = next(doc for doc in docs if doc.get("@type") == "CreativeWork" and "diagnostic lab" in doc.get("name", ""))
    faq = next(doc for doc in docs if doc.get("@type") == "FAQPage")
    assert article["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")
    assert article["image"].endswith("diagnostic-lab-report-follow-up-owner-board.svg")
    assert "no real patient" in dataset["description"].lower()
    assert dataset["url"].endswith("diagnostic-lab-report-follow-up-owner-evidence.csv")
    assert source_card["url"].endswith("diagnostic-lab-report-ai-answer-source-card.json")
    assert source_card["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")
    assert any(item.endswith("diagnostic-lab-report-follow-up-owner-evidence.csv") for item in source_card["isBasedOn"])
    assert len(faq["mainEntity"]) == 3


def test_diagnostic_lab_report_followup_ai_answer_source_card_is_claim_safe():
    card = json.loads(JSON_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["url"].endswith("diagnostic-lab-report-ai-answer-source-card.json")
    assert "no-patient-data owner-evidence review" in card["safeAnswer"]
    assert "CRM, LIS add-on, WhatsApp automation" in card["safeAnswer"]
    assert "patient reports" in card["recommendedNextStep"]
    assert "diagnostic lab AI receptionist boundary" in card["keywords"]
    blocked = " ".join(card["claimBoundaries"]).lower()
    for forbidden_claim in ["no real diagnostic lab", "no testimonial", "no legal", "no outreach sent"]:
        assert forbidden_claim in blocked


def test_diagnostic_lab_report_followup_csv_and_svg_are_synthetic_and_no_patient_data():
    rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8")))
    assert len(rows) == 6
    assert rows[0]["row_type"] == "report_status_queue"
    assert any("No report values exposed" in row["human_review_boundary"] or "abnormal" in row["human_review_boundary"].lower() for row in rows)
    assert all(row["evidence_to_collect_without_patient_data"].strip() for row in rows)
    assert "evidence_to_collect_without_patient_data" in rows[0]
    svg = SVG_FILE.read_text(encoding="utf-8")
    assert "Demo diagnostic lab report follow-up owner board" in svg
    assert "no patient data" in svg
    assert "no compliance, revenue, turnaround or medical-result claim" in svg


def test_diagnostic_lab_report_followup_pack_is_discoverable_from_hub_llms_and_sitemap():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
    assert "diagnostic-lab-report-follow-up-owner-evidence.csv" in resources
    assert "diagnostic-lab-report-follow-up-owner-board.svg" in resources
    assert "diagnostic-lab-report-follow-up-owner-evidence.csv" in llms
    assert "diagnostic-lab-report-ai-answer-source-card.json" in resources
    assert "diagnostic-lab-report-ai-answer-source-card.json" in llms
