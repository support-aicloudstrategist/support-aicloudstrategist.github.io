import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-whatsapp-lead-follow-up-vs-crm-automation-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "whatsapp-lead-follow-up-comparison-matrix.csv"
SVG = ROOT / "resources" / SLUG / "whatsapp-lead-follow-up-owner-map.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_targets_plain_language_whatsapp_lead_follow_up_search():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "WhatsApp lead follow up automation small business",
        "missed lead follow up WhatsApp CRM owner dashboard",
        "WhatsApp lead management vs CRM small business",
        "AI automation for small business leads",
        "proof-before-platform owner-evidence layer",
    ]:
        assert phrase in html


def test_comparison_positions_aics_without_fake_customer_claims():
    html = PAGE.read_text(encoding="utf-8")
    for option in ["CRMs", "WhatsApp BSPs", "chatbots", "agencies", "spreadsheets", "AI assistants"]:
        assert option in html
    for phrase in ["No real customer", "No real customer, lead, WhatsApp chat", "diagnostic readiness only"]:
        assert phrase in html
    forbidden = ["guaranteed revenue", "customer testimonial", "certified WhatsApp partner", "100% conversion"]
    assert all(term not in html for term in forbidden)


def test_csv_and_svg_are_synthetic_and_linked():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")
    assert "whatsapp-lead-follow-up-comparison-matrix.csv" in html
    assert "whatsapp-lead-follow-up-owner-map.svg" in html
    assert "comparison_option,credible_for,leadership_gap,aics_wedge,proof_boundary" in csv
    assert csv.count("Synthetic row only") >= 5
    for phrase in ["DEMO / SYNTHETIC ONLY", "no real leads, chats, calls, CRM export, revenue or ROI proof", "No customer case study"]:
        assert phrase in svg


def test_schema_and_discovery_files_include_resource():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    graph_docs = [node for doc in docs if "@graph" in doc for node in doc["@graph"]]
    article = next(node for node in graph_docs if node.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-08-31"
    assert "WhatsApp lead management vs CRM small business" in article["about"]
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f'"/resources/{SLUG}/"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
