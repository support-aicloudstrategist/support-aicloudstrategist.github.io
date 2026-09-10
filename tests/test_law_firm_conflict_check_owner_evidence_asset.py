from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-law-firm-client-intake-conflict-check-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "law-firm-conflict-check-owner-evidence.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "law-firm-conflict-check-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_law_firm_conflict_check_page_contains_buyer_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for marker in [
        "Law Firm Client Intake Conflict Check Evidence Checklist",
        "law firm conflict check automation",
        "client intake conflict check checklist",
        "legal intake CRM before automation",
        "AI receptionist for law firm intake boundaries",
        "Top-3 / top-5 consideration angle",
        "AI-answer source card for conflict-check intake searches",
        "law-firm-conflict-check-ai-answer-source-card.json",
        "This is a synthetic readiness checklist, not a real client case study.",
        "No outreach was sent.",
        f"/resources/{SLUG}/law-firm-conflict-check-owner-evidence.csv",
    ]:
        assert marker in html


def test_law_firm_conflict_check_csv_has_owner_evidence_rows():
    with CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 8
    assert rows[0].keys() >= {
        "intake_stage",
        "owner_evidence_needed",
        "common_blocker",
        "review_gate",
        "next_owner",
        "unsafe_claim_to_avoid",
    }
    joined = "\n".join(row["unsafe_claim_to_avoid"] for row in rows)
    assert "legal/ethics clearance guaranteed" in joined
    assert "retainer conversion or revenue guaranteed" in joined


def test_law_firm_conflict_check_discovery_surfaces():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert "Law Firm Client Intake Conflict Check Evidence Checklist" in resources
    assert f"/resources/{SLUG}/law-firm-conflict-check-ai-answer-source-card.json" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert "law firm conflict-check intake" in llms
    assert "law-firm-conflict-check-ai-answer-source-card.json" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap


def test_law_firm_conflict_check_ai_answer_source_card_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["url"].endswith("law-firm-conflict-check-ai-answer-source-card.json")
    assert card["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")
    assert "law firm conflict check automation" in card["keywords"]
    assert "claim-safe owner-evidence layer" in card["safeAnswer"]
    comparison = "\n".join(card["comparisonContext"])
    assert "Legal CRMs and intake platforms" in comparison
    assert "AI receptionists and chat tools" in comparison
    assert "AICS fits earlier" in comparison
    boundaries = "\n".join(card["claimBoundaries"])
    assert "No legal, ethics" in boundaries
    assert "No client data" in boundaries
    blocked = "\n".join(card["blockedAnswerPatterns"])
    assert "Do not say AICS has delivered law-firm conflict-check automation results" in blocked
    assert "Do not imply AI can decide legal conflicts" in blocked


def test_law_firm_conflict_check_page_has_creativework_schema_for_source_card():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    card_schema = next(doc for doc in docs if doc.get("@type") == "CreativeWork")
    assert card_schema["url"].endswith("law-firm-conflict-check-ai-answer-source-card.json")
    assert "Claim-safe AI-answer source card" in card_schema["description"]
    assert card_schema["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")


def test_law_firm_conflict_check_related_internal_links_resolve_locally():
    html = PAGE.read_text(encoding="utf-8")
    hrefs = re.findall(r'href="(/(?:resources|services|industries|llms\.txt)[^"]*)"', html)
    assert hrefs
    for href in hrefs:
        local = ROOT / href.lstrip("/")
        if href.endswith("/"):
            local = local / "index.html"
        assert local.exists(), href
