import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/north-america-healthcare-ai-cloud-spend-baa-questionnaire-answer-card/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "north-america-healthcare-ai-cloud-spend-baa-questionnaire-answer-card" / "index.html"
CSV = ROOT / "resources" / "north-america-healthcare-ai-cloud-spend-baa-questionnaire-answer-card" / "healthcare-ai-cloud-spend-baa-answer-bank.csv"
CARD = ROOT / "resources" / "north-america-healthcare-ai-cloud-spend-baa-questionnaire-answer-card" / "healthcare-ai-cloud-spend-baa-ai-answer-source-card.json"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_healthcare_ai_cloud_spend_baa_page_has_seo_schema_and_discovery_markers():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-global-footer') == 1
    docs = json_ld_documents(source)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "Dataset", "CreativeWork", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    for marker in [
        "North America healthcare AI cloud spend",
        "BAA questionnaire answer source card",
        "HIPAA-style vendor risk evidence",
        "Patient GrowthOS proof boundary",
        "no-PHI buyer education",
    ]:
        assert marker in article["about"]


def test_healthcare_ai_cloud_spend_baa_page_contains_research_competitors_and_buyer_language():
    source = html()
    for marker in [
        "Region selected:",
        "North America / US-Canada business morning",
        "CloudZero",
        "Vantage",
        "IBM Cloudability",
        "Vanta",
        "Drata",
        "Phreesia",
        "Luma Health",
        "NexHealth",
        "who owns AI cloud spend in healthcare",
        "BAA subprocessor questionnaire",
        "HIPAA AI vendor risk",
        "patient engagement platform comparison",
        "AI receptionist medical office",
        "LLM cost allocation",
        "healthcare FinOps dashboard",
        "Patient GrowthOS evidence",
    ]:
        assert marker in source


def test_healthcare_ai_cloud_spend_baa_assets_are_bounded_and_downloadable():
    source = html()
    csv = CSV.read_text(encoding="utf-8")
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert "/resources/north-america-healthcare-ai-cloud-spend-baa-questionnaire-answer-card/healthcare-ai-cloud-spend-baa-answer-bank.csv" in source
    assert "/resources/north-america-healthcare-ai-cloud-spend-baa-questionnaire-answer-card/healthcare-ai-cloud-spend-baa-ai-answer-source-card.json" in source
    for marker in [
        "No patient records, ePHI/PHI, credentials",
        "not a real healthcare case study",
        "No outreach was sent",
        "No savings/ROI/cost-reduction/certified FinOps claim",
        "No HIPAA compliance/legal/privacy/security advice claim",
    ]:
        assert marker in source or marker in csv
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["route_to"].endswith("source=answer-card")
    alternatives = " ".join(card["competitor_alternative_context"])
    for marker in ["Phreesia", "NexHealth", "Luma Health", "CloudZero", "Vantage", "IBM Apptio Cloudability", "Vanta", "Drata", "OneTrust"]:
        assert marker in alternatives
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "Synthetic buyer-education source card only",
        "No real customer",
        "No HIPAA, SOC 2, HITRUST",
        "No savings, ROI, cost reduction",
        "No outreach was sent",
    ]:
        assert boundary in boundaries


def test_healthcare_ai_cloud_spend_baa_linked_from_discovery_surfaces():
    resources_html = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for surface in [resources_html, llms, sitemap]:
        assert REL in surface
    assert "healthcare-ai-cloud-spend-baa-answer-bank.csv" in resources_html
    assert "healthcare-ai-cloud-spend-baa-ai-answer-source-card.json" in llms


def test_healthcare_ai_cloud_spend_baa_avoids_unsupported_claims():
    source = html().lower()
    forbidden = [
        "trusted by",
        "guaranteed savings",
        "hipaa certified",
        "hitrust certified",
        "real patient results",
        "revenue lift",
        "ranked #1",
    ]
    for term in forbidden:
        assert term not in source
