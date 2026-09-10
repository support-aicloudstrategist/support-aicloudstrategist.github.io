import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthcare-ai-patient-access-proof-room"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-healthcare-ai-patient-access-proof-room.csv"
SVG = ROOT / "resources" / SLUG / "us-healthcare-ai-patient-access-proof-room.svg"
CARD = ROOT / "resources" / SLUG / "us-healthcare-ai-patient-access-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_us_healthcare_ai_patient_access_proof_room_targets_north_america_buyer_language():
    html = PAGE.read_text(encoding="utf-8")
    assert "7 Sep 2026 North America buyer-search refresh" in html
    assert "patient access leakage" in html
    assert "AI receptionist for medical practices" in html
    assert "prior authorization status" in html
    assert "HIPAA AI vendor risk" in html
    assert "cloud cost allocation" in html
    assert "LLM/API spend" in html
    assert "North America was entering the US Eastern business day" in html


def test_us_healthcare_ai_patient_access_proof_room_records_competitor_categories_and_source_limits():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Direct public-source checks returned HTTP 200 for CMS Interoperability and Prior Authorization",
        "ONC HTI-1",
        "FinOps Foundation Framework",
        "Phreesia, Luma Health, Waystar, Availity, Notable, Vanta",
        "HHS HIPAA pages, Drata healthcare and Azure healthcare returned HTTP 403",
        "one CloudZero healthcare URL returned 404",
        "not negative product or authority claims",
        "CMS interoperability and prior authorization",
        "algorithm transparency language",
        "cloud/LLM/API spend owners before discussing savings",
        "AWS and Google Cloud healthcare pages",
        "AICS should remain the redacted evidence and owner-handoff layer",
        "AICS should not claim to replace these systems",
        "no-credentials evidence room",
    ]:
        assert phrase in html


def test_us_healthcare_ai_patient_access_proof_room_preserves_legacy_vendor_context():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Patient engagement and patient access:",
        "RCM/prior authorization/eligibility:",
        "Healthcare AI automation:",
        "Trust and spend evidence:",
    ]:
        assert phrase in html


def test_us_healthcare_ai_patient_access_proof_room_has_synthetic_csv_and_claim_boundaries():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    assert len(rows) == 7
    assert {row["lane"] for row in rows} >= {
        "Patient access leakage",
        "Referral and prior authorization",
        "AI receptionist boundary",
        "HIPAA evidence boundary",
        "Cloud and AI spend",
    }
    joined = " ".join(row["unsafe_claim_boundary"] for row in rows)
    assert "Do not claim HIPAA SOC 2 HITRUST compliance" in joined
    assert "Do not claim savings ROI" in joined
    assert "Do not claim top-3 ranking demand leads revenue or customer proof" in joined


def test_us_healthcare_ai_patient_access_proof_room_svg_is_demo_synthetic_not_customer_proof():
    svg = SVG.read_text(encoding="utf-8")
    for phrase in [
        "Demo US healthcare AI patient access proof room owner board",
        "Demo/synthetic owner board",
        "No PHI/ePHI",
        "Referral + prior auth",
        "AI receptionist boundary",
        "HIPAA evidence boundary",
        "Cloud + AI spend",
        "Top-3 consideration wedge",
        "Blocked unsafe claims",
        "not a real medical group",
    ]:
        assert phrase in svg
    forbidden = ["real customer", "guaranteed", "HIPAA compliant"]
    assert all(term not in svg for term in forbidden)


def test_us_healthcare_ai_patient_access_proof_room_metadata_and_discovery_files():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    graph_docs = [node for doc in docs if "@graph" in doc for node in doc["@graph"]]
    article = next(node for node in graph_docs if node.get("@type") == "Article")
    dataset = next(node for node in graph_docs if node.get("@type") == "Dataset")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-10"
    assert "US healthcare AI patient access" in article["about"]
    creative = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "CreativeWork")
    assert creative["url"].endswith("/us-healthcare-ai-patient-access-ai-answer-source-card.json")
    assert dataset["url"].endswith("/us-healthcare-ai-patient-access-proof-room.csv")
    resources_html = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "/resources/us-healthcare-ai-patient-access-proof-room/" in resources_html
    assert "us-healthcare-ai-patient-access-ai-answer-source-card.json" in resources_html
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in llms
    assert "us-healthcare-ai-patient-access-ai-answer-source-card.json" in llms


def test_us_healthcare_ai_patient_access_ai_answer_source_card_is_claim_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "North America / US business morning"
    assert card["no_outreach"] is True
    assert card["route_to"].endswith("source=answer-card")
    buyer_language = " ".join(card["buyer_pain_language"])
    for marker in [
        "patient access leakage AI receptionist HIPAA",
        "BAA subprocessor evidence before AI receptionist",
        "LLM API cloud spend ownership healthcare",
        "Healthcare GrowthOS evidence",
    ]:
        assert marker in buyer_language
    alternatives = " ".join(card["competitor_alternative_context"])
    for marker in ["Phreesia", "Luma Health", "Waystar", "Availity", "Notable", "Vanta", "CloudZero", "IBM Apptio Cloudability"]:
        assert marker in alternatives
    blocked = " ".join(card["blocked_answer_patterns"] + card["claim_boundaries"])
    for marker in [
        "No real medical group",
        "No customer",
        "No savings, ROI",
        "No outreach was sent",
    ]:
        assert marker in blocked
