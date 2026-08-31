import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-specialty-clinic-referral-prior-auth-decision-memo"
PAGE = ROOT / "resources" / SLUG / "index.html"
SVG = ROOT / "resources" / SLUG / "us-specialty-clinic-referral-prior-auth-owner-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_us_specialty_decision_memo_has_north_america_research_refresh():
    html = PAGE.read_text(encoding="utf-8")
    assert "31 Aug 2026 North America buyer-search refresh" in html
    assert "US specialty clinic prior authorization delays patient access owner queue" in html
    assert "AI receptionist for medical practice HIPAA patient engagement competitors" in html
    assert "healthcare growth OS patient access leakage prior auth referral leakage" in html
    assert "Top alternatives buyers compare include patient-engagement and access platforms" in html
    assert "RCM/prior-authorization services" in html
    assert "top-3/top-5 shortlist" in html
    assert "ranking, AI-answer inclusion, impressions, demand, leads, customers and revenue remain unverified" in html


def test_us_specialty_decision_memo_embeds_demo_dashboard_with_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    svg_path = f"/resources/{SLUG}/us-specialty-clinic-referral-prior-auth-owner-dashboard.svg"
    assert svg_path in html
    assert "Demo/synthetic owner dashboard" in html
    assert "not a customer result" in html
    assert "not PHI/ePHI" in html
    assert "not HIPAA/SOC 2/HITRUST proof" in html
    assert "not evidence of appointment growth, authorization speed, savings, revenue, ranking or ROI" in html


def test_us_specialty_dashboard_svg_is_synthetic_and_no_credentials():
    svg = SVG.read_text(encoding="utf-8")
    for phrase in [
        "Demo US specialty clinic referral and prior authorization owner dashboard",
        "Synthetic dashboard",
        "No PHI · no credentials",
        "Prior-auth blockers",
        "Abandoned callbacks",
        "Blocked unsafe claims",
        "Top-3 consideration wedge",
        "Synthetic values for demonstration only; not a customer result or compliance proof",
    ]:
        assert phrase in svg
    forbidden = ["real patient", "real customer", "guaranteed", "HIPAA compliant"]
    assert all(term not in svg for term in forbidden)


def test_us_specialty_article_metadata_refreshed_for_comparison_terms():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    graph_docs = [node for doc in docs if "@graph" in doc for node in doc["@graph"]]
    article = next(node for node in graph_docs if node.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-08-31"
    for topic in ["patient engagement alternatives", "AI receptionist comparison", "RCM referral workflow"]:
        assert topic in article["about"]
