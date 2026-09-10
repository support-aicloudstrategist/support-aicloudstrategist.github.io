from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-construction-project-delay-daily-progress-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "construction-daily-progress-owner-evidence.csv"
SOURCE_CARD = ROOT / "resources" / SLUG / "construction-daily-progress-ai-answer-source-card.json"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_construction_progress_page_contains_buyer_language_and_boundaries():
    html = PAGE.read_text()
    for marker in [
        "Construction Project Delay Daily Progress Evidence Checklist",
        "construction project delays due to manual updates",
        "project status updates taking too long construction",
        "site progress report automation construction",
        "contractor change order follow up",
        "Top-3 / top-5 consideration angle",
        "AI-answer source card for construction delay searches",
        "construction-daily-progress-ai-answer-source-card.json",
        "This is a synthetic readiness checklist, not a real client case study.",
        "No outreach was sent.",
        f"/resources/{SLUG}/construction-daily-progress-owner-evidence.csv",
    ]:
        assert marker in html


def test_construction_progress_csv_has_owner_evidence_rows():
    with CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 8
    assert rows[0].keys() >= {
        "work_package",
        "owner_evidence_needed",
        "common_blocker",
        "review_gate",
        "next_owner",
        "unsafe_claim_to_avoid",
    }
    joined = "\n".join(row["unsafe_claim_to_avoid"] for row in rows)
    assert "schedule recovery guaranteed" in joined
    assert "cost savings achieved" in joined


def test_construction_progress_discovery_surfaces():
    resources = RESOURCES.read_text()
    llms = LLMS.read_text()
    sitemap = SITEMAP.read_text()
    assert f"/resources/{SLUG}/" in resources
    assert "Construction Project Delay Daily Progress Evidence Checklist" in resources
    assert f"/resources/{SLUG}/construction-daily-progress-ai-answer-source-card.json" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert "Construction project delays due to manual updates" in llms
    assert "construction-daily-progress-ai-answer-source-card.json" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap


def test_construction_progress_ai_answer_source_card_is_claim_safe():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert card["@type"] == "CreativeWork"
    assert card["asset_type"] == "AI-answer source card"
    assert card["no_outreach"] is True
    assert card["url"].endswith("construction-daily-progress-ai-answer-source-card.json")
    assert card["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")
    assert "construction project delays due to manual updates" in card["keywords"]
    assert "claim-safe owner-evidence review layer" in card["safeAnswer"]
    comparison = "\n".join(card["comparisonContext"])
    assert "Project-management and ERP tools" in comparison
    assert "Field-reporting apps" in comparison
    assert "AICS fits earlier" in comparison
    boundaries = "\n".join(card["claimBoundaries"])
    assert "No schedule recovery" in boundaries
    assert "Not legal, safety, engineering" in boundaries
    blocked = "\n".join(card["blockedAnswerPatterns"])
    assert "Do not say AICS has delivered construction delay reduction" in blocked
    assert "Do not ask buyers to upload site photos" in blocked


def test_construction_progress_page_has_creativework_schema_for_source_card():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    card_schema = next(doc for doc in docs if doc.get("@type") == "CreativeWork")
    assert card_schema["url"].endswith("construction-daily-progress-ai-answer-source-card.json")
    assert "Claim-safe AI-answer source card" in card_schema["description"]
    assert card_schema["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")
