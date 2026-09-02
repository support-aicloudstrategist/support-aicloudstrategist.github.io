import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "small-business-owner-ai-automation-readiness-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "small-business-ai-automation-readiness-owner-register.csv"
SVG = ROOT / "resources" / SLUG / "small-business-ai-automation-owner-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_targets_small_business_ai_automation_buyer_language_and_visibility_boundary():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "AI automation for small business",
        "how to automate my small business manual work",
        "small business AI automation readiness checklist",
        "too much manual admin",
        "missed customer calls",
        "Bing returned HTTP 200",
        "sampled result HTML did not show an AICS marker",
        "rankings, AI-answer inclusion, impressions, clicks, leads, customers and demand remain unverified",
    ]:
        assert phrase in html


def test_csv_and_svg_are_synthetic_forwardable_owner_assets():
    html = PAGE.read_text(encoding="utf-8")
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    svg = SVG.read_text(encoding="utf-8")
    assert "small-business-ai-automation-readiness-owner-register.csv" in html
    assert "small-business-ai-automation-owner-dashboard.svg" in html
    assert len(rows) == 6
    assert set(rows[0]) == {
        "workflow_signal",
        "buyer_question",
        "redacted_evidence_to_collect",
        "accountable_owner",
        "ready_to_automate_when",
        "unsafe_claim_boundary",
    }
    assert all("Synthetic row only" in row["unsafe_claim_boundary"] for row in rows)
    for phrase in [
        "DEMO / SYNTHETIC ONLY",
        "no real leads, chats, calls, CRM export, revenue, savings or ROI proof",
        "No customer case study",
    ]:
        assert phrase in svg


def test_schema_discovery_and_claim_boundaries_are_clean():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "Dataset", "ImageObject", "FAQPage"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-02"
    assert "AI automation for small business" in article["about"]
    dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
    image = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "ImageObject")
    assert dataset["url"] == f"{URL}small-business-ai-automation-readiness-owner-register.csv"
    assert image["contentUrl"] == f"{URL}small-business-ai-automation-owner-dashboard.svg"
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f"{URL}small-business-ai-automation-readiness-owner-register.csv" in llms
    assert f"{URL}small-business-ai-automation-owner-dashboard.svg" in llms
    assert f'"/resources/{SLUG}/"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    for phrase in [
        "No real client",
        "customer data",
        "CRM export",
        "certification",
        "ranking",
        "demand",
        "AI-accuracy claim",
        "No outreach was sent",
    ]:
        assert phrase in html
    forbidden = ["guaranteed revenue", "trusted by", "certified partner", "100% conversion", "real client results"]
    assert all(term not in html.lower() for term in forbidden)
