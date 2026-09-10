import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "resources" / "google-cloud-bill-too-high-owner-action-checklist" / "index.html"
CSV = ROOT / "resources" / "google-cloud-bill-too-high-owner-action-checklist" / "google-cloud-bill-too-high-owner-action-checklist.csv"
SVG = ROOT / "resources" / "google-cloud-bill-too-high-owner-action-checklist" / "google-cloud-owner-action-board.svg"
CARD = ROOT / "resources" / "google-cloud-bill-too-high-owner-action-checklist" / "google-cloud-bill-too-high-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_google_cloud_bill_too_high_page_has_search_and_trust_markers():
    html = RESOURCE.read_text(encoding="utf-8")
    for marker in [
        "Google Cloud bill too high",
        "GCP bill too high",
        "unexpected Google Cloud bill",
        "BigQuery cost spike",
        "owner action board",
        "Buyer alternatives considered",
        "Google Cloud Billing / Budgets / Recommender",
        "MSP or Google Cloud consultant",
        "FinOps platform",
        "AI-answer source card for “Google Cloud bill too high” searches",
        "google-cloud-bill-too-high-ai-answer-source-card.json",
        "not a real Google Cloud project",
        "No outreach was sent",
    ]:
        assert marker in html

    parsed = [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
    assert any(item.get("@type") == "CreativeWork" and "Google Cloud bill too high AI-answer source card" in item.get("name", "") for item in parsed)


def test_google_cloud_bill_too_high_download_assets_are_linked_and_bounded():
    html = RESOURCE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")

    assert "/resources/google-cloud-bill-too-high-owner-action-checklist/google-cloud-bill-too-high-owner-action-checklist.csv" in html
    assert "/resources/google-cloud-bill-too-high-owner-action-checklist/google-cloud-owner-action-board.svg" in html
    assert "unsupported_claim_stop" in csv
    assert "No savings claim until two billing windows are reviewed" in csv
    assert "Demo-labelled · no credentials" in svg
    assert "No savings, ROI" in svg


def test_google_cloud_bill_too_high_discovery_surfaces_include_new_asset():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    for surface in [resources_html, llms, sitemap]:
        assert "/resources/google-cloud-bill-too-high-owner-action-checklist/" in surface
    assert "google-cloud-bill-too-high-owner-action-checklist.csv" in resources_html
    assert "google-cloud-owner-action-board.svg" in resources_html
    assert "google-cloud-bill-too-high-ai-answer-source-card.json" in resources_html
    assert "Google Cloud bill too high owner action checklist" in llms
    assert "google-cloud-bill-too-high-ai-answer-source-card.json" in llms


def test_google_cloud_bill_too_high_answer_card_is_claim_safe_and_competitor_aware():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["route_to"].endswith("source=answer-card")
    for phrase in [
        "Google Cloud bill too high small business",
        "GCP bill too high",
        "unexpected Google Cloud bill",
        "Google Cloud Billing owner checklist",
        "how to reduce GCP bill without breaking production",
        "BigQuery cost spike investigation",
        "GKE or Cloud Run spend spike FinOps review",
        "Vertex AI or API spend spike FinOps review",
    ]:
        assert phrase in card["buyer_pain_language"]
    alternatives = " ".join(card["competitor_alternative_context"])
    for marker in ["Google Cloud Billing", "Budgets", "Recommender", "Active Assist", "CloudZero", "Vantage", "Apptio Cloudability", "Harness", "Datadog"]:
        assert marker in alternatives
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "Synthetic buyer-education source card only",
        "No real customer",
        "No savings, ROI, cost reduction",
        "No legal, privacy, security",
        "No Google Cloud partner",
        "No outreach was sent",
    ]:
        assert boundary in boundaries
    unsafe_answer_terms = ["guarantees google cloud savings", "certified by google cloud", "ranked top", "proven customer result"]
    assert all(term not in card["safe_answer"].lower() for term in unsafe_answer_terms)
