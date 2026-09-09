from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "uae-healthtech-cloud-trust-patient-data-evidence-source-map"
CARD = RESOURCE_DIR / "uae-healthtech-patient-data-ai-answer-source-card.json"
PAGE = RESOURCE_DIR / "index.html"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
CARD_URL = "https://aicloudstrategist.com/resources/uae-healthtech-cloud-trust-patient-data-evidence-source-map/uae-healthtech-patient-data-ai-answer-source-card.json"
REL = "/resources/uae-healthtech-cloud-trust-patient-data-evidence-source-map/uae-healthtech-patient-data-ai-answer-source-card.json"


def test_uae_healthtech_patient_data_source_card_json_is_claim_safe():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == CARD_URL
    assert len(card["best_fit_queries"]) == 5
    assert "no-credentials, no-patient-data Cloud Trust" in card["safe_short_answer"]
    assert "Malaffi/NABIDH-style handoffs" in card["safe_short_answer"]
    assert any("qualified human review" in gate for gate in card["human_review_gates"])
    boundary = " ".join(card["blocked_claims"] + [card["proof_boundary"]]).lower()
    for unsafe in ["no real uae hospital", "no patient data", "no pdpl", "no ranking"]:
        assert unsafe in boundary
    assert "roi" in boundary
    assert "appointment growth" in boundary


def test_uae_healthtech_patient_data_source_card_is_linked_for_buyers_and_ai_routing():
    page = PAGE.read_text(encoding="utf-8")
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    assert REL in page
    assert "AI-answer source card for safe buyer citation" in page
    assert "CreativeWork" in page
    assert REL in resources
    assert CARD_URL in llms
    assert "UAE healthtech patient-data AI-answer source card JSON" in llms
