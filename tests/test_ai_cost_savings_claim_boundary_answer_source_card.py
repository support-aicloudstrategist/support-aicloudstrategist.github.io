from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-cost-savings-claim-boundary-worksheet"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-cost-savings-claim-boundary-worksheet.csv"
CARD = ROOT / "resources" / SLUG / "ai-cost-savings-claim-boundary-answer-source-card.json"


def test_ai_cost_savings_claim_boundary_page_routes_answer_source_card():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert 'data-ai-answer-source-card="ai-cost-savings-claim-boundary"' in source
    assert "ai-cost-savings-claim-boundary-answer-source-card.json" in source
    for marker in [
        "AI Cost Savings Claim Boundary Worksheet",
        "LLM spend reduction",
        "GPU optimization",
        "cloud savings evidence",
        "FinOps ROI claim",
        "verified evidence",
        "Truth boundary",
    ]:
        assert marker in source


def test_ai_cost_savings_claim_boundary_answer_card_is_claim_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["canonical_url"] == URL
    assert card["no_outreach"] is True
    assert card["route_to"].endswith("source=answer-card")
    pain_language = " ".join(card["buyer_pain_language"])
    for phrase in [
        "AI cost savings claim evidence",
        "LLM spend reduction proof boundary",
        "GPU optimization runway claim review",
        "cloud savings ROI claim approval",
        "FinOps savings claim worksheet",
    ]:
        assert phrase in pain_language
    boundaries = " ".join(card["claim_boundaries"])
    for boundary in [
        "No real client case study",
        "No guaranteed savings, ROI, revenue",
        "Not financial, legal, procurement",
        "No outreach was sent",
    ]:
        assert boundary in boundaries
    assert "aics guarantees" not in card["safe_answer"].lower()
    assert "AICS guarantees AI cost reduction, savings, ROI or runway extension" in card["blocked_answer_patterns"]


def test_ai_cost_savings_claim_boundary_resource_is_discoverable():
    csv_source = CSV.read_text(encoding="utf-8")
    assert "claim_requested" in csv_source
    assert "safe_note" in csv_source
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "ai-cost-savings-claim-boundary-answer-source-card.json" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{REL}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
