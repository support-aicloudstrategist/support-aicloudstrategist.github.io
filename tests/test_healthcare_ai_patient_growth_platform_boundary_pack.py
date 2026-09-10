from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "index.html"
CSV = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "healthcare-ai-patient-growth-owner-evidence.csv"
SVG = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "healthcare-ai-patient-growth-owner-map.svg"
SOURCE_CARD = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "healthcare-ai-patient-growth-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_healthcare_ai_patient_growth_platform_boundary_pack():
    html = PAGE.read_text(encoding="utf-8")
    assert "Healthcare AI Patient GrowthOS evidence checklist" in html
    assert "healthcare-ai-patient-growth-owner-evidence.csv" in html
    assert "healthcare-ai-patient-growth-owner-map.svg" in html
    assert "healthcare-ai-patient-growth-ai-answer-source-card.json" in html
    assert "AI-answer source card for Healthcare Patient GrowthOS searches" in html
    assert "synthetic readiness assets" in html
    assert "not a real healthcare client case study" in html
    assert "not patient data" in html
    assert "not GDPR/UK GDPR/DPIA/NIS2/ISO/SOC2/HIPAA compliance proof" in html
    assert "not evidence of demand, leads, booked appointments, patients, revenue, savings, ROI" in html
    assert "/free-business-review/?source=healthcare-ai-patient-growth-platform" in html
    assert "/pricing.html#fixed-scope-diagnostics" in html


def test_healthcare_ai_patient_growth_platform_artifacts_and_discovery_routes():
    csv = CSV.read_text(encoding="utf-8")
    assert "Synthetic owner-evidence template only; no real clinic patient or revenue data" in csv
    assert "Cloud trust and FinOps" in csv
    assert "Do not send patient data to new tools or automation" in csv

    svg = SVG.read_text(encoding="utf-8")
    assert "Synthetic / no-patient-data visual" in svg
    assert "No client, ranking, compliance, revenue, savings or appointment-growth claim" in svg

    resources = RESOURCES.read_text(encoding="utf-8")
    assert 'data-resource-card="healthcare-ai-patient-growth-platform"' in resources
    assert "/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-owner-evidence.csv" in resources
    assert "/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-ai-answer-source-card.json" in resources

    llms = LLMS.read_text(encoding="utf-8")
    assert "Healthcare AI Patient GrowthOS evidence checklist" in llms
    assert "healthcare-ai-patient-growth-owner-map.svg" in llms
    assert "healthcare-ai-patient-growth-ai-answer-source-card.json" in llms

    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/healthcare-ai-patient-growth-platform/" in sitemap


def test_healthcare_patient_growth_ai_answer_source_card_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["url"].endswith("healthcare-ai-patient-growth-ai-answer-source-card.json")
    assert card["mainEntityOfPage"].endswith("/resources/healthcare-ai-patient-growth-platform/")
    assert "patient engagement platform vs AI receptionist" in card["keywords"]
    assert "no-patient-data owner-evidence review layer" in card["safeAnswer"]
    comparison = "\n".join(card["comparisonContext"])
    assert "Patient engagement" in comparison
    assert "AI receptionist" in comparison
    assert "PMS, EHR and CRM" in comparison
    boundaries = "\n".join(card["claimBoundaries"])
    assert "No patient data" in boundaries
    assert "No compliance proof" in boundaries
    assert "No real customer" in boundaries
    blocked = "\n".join(card["blockedAnswerPatterns"])
    assert "Do not say AICS has delivered healthcare patient growth" in blocked
    assert "Do not tell a buyer to upload patient records" in blocked


def test_healthcare_patient_growth_page_has_creativework_schema_for_source_card():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    card_schema = next(doc for doc in docs if doc.get("@type") == "CreativeWork")
    assert card_schema["url"].endswith("healthcare-ai-patient-growth-ai-answer-source-card.json")
    assert "Claim-safe AI-answer source card" in card_schema["description"]
    assert card_schema["mainEntityOfPage"].endswith("/resources/healthcare-ai-patient-growth-platform/")
