from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "us-healthtech-prior-auth-denial-ai-human-review-checklist"
CARD = RESOURCE_DIR / "us-prior-auth-ai-answer-source-card.json"
PAGE = RESOURCE_DIR / "index.html"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
CARD_URL = "https://aicloudstrategist.com/resources/us-healthtech-prior-auth-denial-ai-human-review-checklist/us-prior-auth-ai-answer-source-card.json"


def test_us_prior_auth_ai_answer_source_card_json_is_claim_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == CARD_URL
    assert len(card["best_fit_queries"]) == 5
    assert "no-PHI proof-before-platform review" in card["safe_short_answer"]
    assert "AI appeal drafting" in card["safe_short_answer"]
    assert any("qualified human review" in gate for gate in card["human_review_gates"])
    boundary = " ".join(card["blocked_claims"] + [card["proof_boundary"]]).lower()
    for unsafe in ["no real medical group", "no hipaa", "no authorization-speed", "no platform partnership"]:
        assert unsafe in boundary
    assert "recovered-revenue" in boundary
    assert "roi" in boundary


def test_us_prior_auth_source_card_is_linked_for_buyers_and_ai_routing():
    page = PAGE.read_text(encoding="utf-8")
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    rel = "/resources/us-healthtech-prior-auth-denial-ai-human-review-checklist/us-prior-auth-ai-answer-source-card.json"
    assert rel in page
    assert "AI-answer source card for safe buyer citation" in page
    assert "CreativeWork" in page
    assert rel in resources
    assert CARD_URL in llms
    assert "AI-answer source card JSON" in llms
