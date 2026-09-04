import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthcare-ai-patient-access-proof-room"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-healthcare-ai-patient-access-proof-room.csv"
SVG = ROOT / "resources" / SLUG / "us-healthcare-ai-patient-access-proof-room.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_us_healthcare_ai_patient_access_proof_room_targets_north_america_buyer_language():
    html = PAGE.read_text(encoding="utf-8")
    assert "4 Sep 2026 North America buyer-search refresh" in html
    assert "patient access leakage" in html
    assert "AI receptionist for medical practices" in html
    assert "prior authorization status" in html
    assert "HIPAA AI vendor risk" in html
    assert "cloud cost allocation" in html
    assert "LLM/API spend" in html
    assert "US East and Central business day was active" in html


def test_us_healthcare_ai_patient_access_proof_room_records_competitor_categories_and_source_limits():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Phreesia positions patient intake around revenue growth, no-show reduction and front-desk chaos",
        "Luma Health frames the market as operational AI",
        "Waystar emphasizes cloud-based revenue cycle management",
        "Availity emphasizes secure exchange between payers, providers and health IT vendors",
        "Notable positions as an AI platform purpose-built for healthcare",
        "Artera and Experian prior-authorization pages returned HTTP 403",
        "not as a negative product claim",
        "AICS should not claim to replace these systems",
        "no-credentials evidence room",
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
    assert article["dateModified"] == "2026-09-04"
    assert "US healthcare AI patient access" in article["about"]
    assert dataset["url"].endswith("/us-healthcare-ai-patient-access-proof-room.csv")
    assert "/resources/us-healthcare-ai-patient-access-proof-room/" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
