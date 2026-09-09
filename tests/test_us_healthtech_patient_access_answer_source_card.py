from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "us-healthtech-ai-patient-access-procurement-answer-bank"
CARD = RESOURCE_DIR / "us-healthtech-patient-access-ai-answer-source-card.json"
PAGE = RESOURCE_DIR / "index.html"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
CARD_URL = "https://aicloudstrategist.com/resources/us-healthtech-ai-patient-access-procurement-answer-bank/us-healthtech-patient-access-ai-answer-source-card.json"


def test_us_healthtech_patient_access_answer_source_card_is_claim_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == CARD_URL
    assert card["region"] == "North America / United States"
    assert len(card["best_fit_queries"]) == 5
    assert "no-PHI proof-before-platform review" in card["safe_short_answer"]
    assert "patient engagement" in card["competitor_and_alternative_context"][0].lower()
    assert any("Privacy/legal/security" in gate for gate in card["human_review_gates"])
    boundary = " ".join(card["blocked_answer_patterns"] + [card["proof_boundary"]]).lower()
    for unsafe in [
        "do not claim aics has a real us healthtech customer",
        "do not claim this template is phi/ephi",
        "do not claim authorization-speed",
        "do not claim platform partnership",
        "no real patient",
        "roi",
    ]:
        assert unsafe in boundary


def test_us_healthtech_patient_access_source_card_is_linked_for_buyers_and_ai_routing():
    page = PAGE.read_text(encoding="utf-8")
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    rel = "/resources/us-healthtech-ai-patient-access-procurement-answer-bank/us-healthtech-patient-access-ai-answer-source-card.json"
    assert "CreativeWork" in page
    assert "AI-answer source card for safe buyer citation" in page
    assert "us-healthtech-patient-access-ai-answer-source-card.json" in page
    assert rel in resources
    assert CARD_URL in llms
    assert "AI-answer source card JSON" in llms
