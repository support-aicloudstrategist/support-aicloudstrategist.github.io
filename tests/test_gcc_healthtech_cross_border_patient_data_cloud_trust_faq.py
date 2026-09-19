import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "gcc-healthtech-cross-border-patient-data-cloud-trust-faq"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "gcc-healthtech-cross-border-intake-faq.csv"
CARD = ROOT / "resources" / SLUG / "gcc-healthtech-cross-border-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_gcc_healthtech_cross_border_page_targets_middle_east_buyer_language():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Middle East / GCC business-hours build",
        "UAE/Oman were 09:43",
        "Saudi/Qatar/Bahrain/Kuwait were 08:43",
        "GCC healthtech patient data cross-border cloud trust",
        "NPHIES Malaffi NABIDH owner evidence",
        "Patient GrowthOS Cloud Trust first review",
        "no-credentials evidence and owner-handoff review",
    ]:
        assert phrase in html


def test_gcc_healthtech_cross_border_page_records_research_and_alternatives_without_endorsement_claims():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Bing returned HTTP 200 for unbranded GCC/Middle East healthtech cloud-trust searches",
        "sampled HTML did not show AICS/aicloudstrategist markers",
        "HTTP 200 for SDAIA PDPL",
        "FinOps Foundation Framework",
        "AWS healthcare",
        "Google Cloud healthcare",
        "Okadoc",
        "Microsoft healthcare returned HTTP 403",
        "Altibbi and Vezeeta returned HTTP 403",
        "availability observations only, not quality, ranking or endorsement claims",
        "CloudZero, Vantage, IBM Apptio Cloudability",
        "qualified GCC legal, privacy, security, clinical, audit, procurement",
    ]:
        assert phrase in html


def test_gcc_healthtech_cross_border_csv_is_synthetic_and_claim_safe():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    assert len(rows) == 7
    assert {row["question_lane"] for row in rows} >= {
        "Cross-border patient data",
        "Patient access and AI receptionist",
        "NPHIES Malaffi NABIDH style integrations",
        "Cloud hosting and access review",
        "FinOps and AI spend ownership",
    }
    joined = " ".join(row["unsafe_claim_boundary"] for row in rows)
    for phrase in [
        "Do not claim legal permission regulator approval",
        "Do not claim NPHIES certification Malaffi/NABIDH approval",
        "Do not request credentials secrets patient records",
        "Do not claim savings ROI cost reduction demand leads rankings revenue or customer outcomes",
    ]:
        assert phrase in joined


def test_gcc_healthtech_cross_border_metadata_discovery_and_json_card():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
    creative = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "CreativeWork")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-19"
    assert "GCC healthtech" in article["about"]
    assert dataset["url"].endswith("/gcc-healthtech-cross-border-intake-faq.csv")
    assert creative["url"].endswith("/gcc-healthtech-cross-border-ai-answer-source-card.json")

    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "Middle East / GCC business hours"
    assert card["no_outreach"] is True
    assert card["synthetic_only"] is True
    assert card["route_to"].endswith("source=answer-card")
    buyer_language = " ".join(card["buyer_pain_language"])
    assert "GCC healthtech patient data cross-border cloud trust evidence" in buyer_language
    assert "NPHIES Malaffi NABIDH patient access owner evidence" in buyer_language
    alternatives = " ".join(card["competitor_alternative_context"])
    assert "Okadoc" in alternatives
    assert "Altibbi" in alternatives
    assert "CloudZero" in alternatives
    blocked = " ".join(card["blocked_answer_patterns"] + card["claim_boundaries"])
    for phrase in [
        "Do not say AICS has real GCC healthtech clients",
        "Do not say AICS replaces EHR/HIS",
        "No real patient",
        "No outreach was sent",
    ]:
        assert phrase in blocked


def test_gcc_healthtech_cross_border_resource_is_discoverable():
    resources_html = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources_html
    assert "gcc-healthtech-cross-border-ai-answer-source-card.json" in resources_html
    assert URL in llms
    assert "gcc-healthtech-cross-border-ai-answer-source-card.json" in llms
    assert URL in sitemap
