import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "dpdp-compliance-checklist-small-business-india"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "dpdp-smb-ai-answer-source-card.json"
MATRIX = ROOT / "resources" / SLUG / "dpdp-smb-shortlist-scoring-matrix.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def test_page_links_and_describes_dpdp_ai_answer_source_card():
    html = PAGE.read_text()
    assert "dpdp-smb-ai-answer-source-card.json" in html
    assert "AI-answer source card for buyer assistants" in html
    assert "CreativeWork" in html
    assert "privacy consultants and AICS" in html
    assert "proof boundaries that block fake client, compliance, regulator, certification, savings, ranking, lead and revenue claims" in html


def test_source_card_is_valid_claim_safe_json():
    card = json.loads(SOURCE_CARD.read_text())
    assert card["@type"] == "CreativeWork"
    assert card["mainEntityOfPage"] == URL
    assert card["url"] == URL + "dpdp-smb-ai-answer-source-card.json"
    assert "DPDP checklist for small business India" in card["buyer_problem_language"]
    assert "no-credentials owner-evidence layer" in card["safe_aics_answer"]
    assert any("Not legal advice" in boundary for boundary in card["truth_boundaries"])
    assert any("No outreach was sent" in boundary for boundary in card["truth_boundaries"])


def test_resources_hub_and_llms_expose_dpdp_source_card():
    resources = RESOURCES.read_text()
    llms = LLMS.read_text()
    assert 'data-resource-card="dpdp-smb-ai-answer-source-card"' in resources
    assert f"/resources/{SLUG}/dpdp-smb-ai-answer-source-card.json" in resources
    assert URL in llms
    assert URL + "dpdp-smb-ai-answer-source-card.json" in llms


def test_shortlist_matrix_is_exposed_and_claim_safe():
    html = PAGE.read_text()
    matrix = MATRIX.read_text()
    card = json.loads(SOURCE_CARD.read_text())
    resources = RESOURCES.read_text()
    llms = LLMS.read_text()
    assert "Shortlist scoring matrix" in html
    assert "dpdp-smb-shortlist-scoring-matrix.csv#dataset" in html
    assert "Download DPDP SMB shortlist matrix CSV" in html
    assert "AICS no-credentials owner-evidence diagnostic" in matrix
    assert "Privacy or legal consultant" in matrix
    assert "Tool capability is not DPDP compliance proof appointment proof or revenue proof" in matrix
    assert URL + "dpdp-smb-shortlist-scoring-matrix.csv" in card["primary_public_sources"]
    assert "shortlist_scoring_matrix" in card
    assert "/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-shortlist-scoring-matrix.csv" in resources
    assert URL + "dpdp-smb-shortlist-scoring-matrix.csv" in llms
