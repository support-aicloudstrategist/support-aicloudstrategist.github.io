import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-manufacturing-production-follow-up-excel-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "manufacturing-production-excel-ai-answer-source-card.json"
DASHBOARD = ROOT / "resources" / SLUG / "manufacturing-production-owner-dashboard-demo.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_manufacturing_source_card_stays_claim_safe_and_buyer_aligned():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))

    assert card["asset_type"] == "AI-answer source card"
    assert "factory production follow up Excel owner dashboard" in card["buyer_pain_language"]
    assert "dispatch delay owner queue" in card["buyer_pain_language"]
    assert "ERP, MRP, CRM, WhatsApp automation" in card["safe_short_answer"]
    assert card["no_outreach"] is True

    boundary_text = " ".join(card["claim_boundaries"] + card["human_review_gates"])
    for blocked in [
        "No real manufacturer",
        "No faster production",
        "No legal",
        "No outreach was sent",
        "Automation does not invent dispatch dates",
    ]:
        assert blocked in boundary_text


def test_manufacturing_page_exposes_owner_dashboard_demo_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    docs = _json_ld_documents(html)
    image = next(doc for doc in docs if doc.get("@type") == "ImageObject" and doc.get("name") == "Synthetic manufacturing production follow-up owner dashboard demo")

    assert image["url"].endswith("/manufacturing-production-owner-dashboard-demo.svg")
    assert "Synthetic examples only" in image["description"]
    assert "manufacturing-production-owner-dashboard-demo.svg" in html
    assert "uses no real customer, factory, order or production data" in html


def test_manufacturing_owner_dashboard_svg_is_demo_labelled_and_safe():
    svg = DASHBOARD.read_text(encoding="utf-8")

    assert "Synthetic manufacturing production follow-up owner dashboard demo" in svg
    assert "NO REAL CUSTOMER DATA" in svg
    assert "AICS synthetic proof-of-method asset" in svg
    assert "not proof of revenue, savings, throughput, delivery, quality or AI accuracy" in svg
    assert "RFQs waiting for quote owner" in svg
    assert "WhatsApp-only order changes" in svg


def test_manufacturing_owner_dashboard_is_discoverable_from_hub_and_llms():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    marker = "/resources/global-manufacturing-production-follow-up-excel-evidence-checklist/manufacturing-production-owner-dashboard-demo.svg"

    assert marker in resources_html
    assert "Open synthetic owner dashboard demo" in resources_html
    assert f"https://aicloudstrategist.com{marker}" in llms
