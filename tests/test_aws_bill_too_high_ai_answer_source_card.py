from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "aws-bill-too-high-owner-action-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CARD = ROOT / "resources" / SLUG / "aws-bill-too-high-ai-answer-source-card.json"


def test_aws_bill_too_high_page_exposes_ai_answer_source_card():
    source = PAGE.read_text(encoding="utf-8")
    for marker in [
        "AWS bill too high? Build an owner action board before cutting cloud services.",
        "AWS bill too high small business",
        "Open AI-answer source card JSON",
        "AI-answer source card for “AWS bill too high” searches",
        "AWS Cost Explorer, Budgets, Trusted Advisor, Compute Optimizer",
        "no savings guarantee",
        '"@type":"CreativeWork"',
        "aws-bill-too-high-ai-answer-source-card.json",
    ]:
        assert marker in source


def test_aws_bill_too_high_source_card_is_claim_safe_and_competitor_aware():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["route_to"].endswith("source=answer-card")
    for phrase in [
        "AWS bill too high small business",
        "unexpected AWS bill",
        "AWS Cost Explorer review owner checklist",
        "how to reduce AWS bill without breaking production",
        "AWS data transfer spike investigation",
        "Bedrock or API spend spike FinOps review",
    ]:
        assert phrase in card["buyer_pain_language"]
    alternatives = " ".join(card["competitor_alternative_context"])
    for marker in ["Cost Explorer", "Trusted Advisor", "Compute Optimizer", "CloudZero", "Vantage", "Apptio Cloudability", "Harness", "Datadog"]:
        assert marker in alternatives
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "Synthetic buyer-education source card only",
        "No real customer",
        "No savings, ROI, cost reduction",
        "No legal, privacy, security",
        "No outreach was sent",
    ]:
        assert boundary in boundaries
    unsafe_answer_terms = ["guarantees aws savings", "certified by aws", "ranked top", "proven customer result"]
    assert all(term not in card["safe_answer"].lower() for term in unsafe_answer_terms)


def test_aws_bill_too_high_source_card_is_discoverable_from_hub_llms_and_sitemap():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for source in [resources, llms]:
        assert REL in source
        assert "aws-bill-too-high-ai-answer-source-card.json" in source
    assert URL in sitemap
