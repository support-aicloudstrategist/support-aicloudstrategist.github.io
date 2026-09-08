import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-security-questionnaire-vs-grc-trust-center-tools-comparison"
RESOURCE = ROOT / "resources" / SLUG
CARD = RESOURCE / "saas-security-questionnaire-answer-card.json"
PAGE = RESOURCE / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_saas_security_questionnaire_answer_card_is_buyer_safe_and_routeable():
    data = json.loads(CARD.read_text(encoding="utf-8"))
    assert data["primary_buyer_question"].startswith("What should a B2B SaaS team do")
    assert "no-credentials" in data["safe_answer"]
    assert data["route_to"].endswith("source=saas-security-answer-card")
    assert data["source_page"].endswith(f"/{SLUG}/")
    joined_boundaries = " ".join(data["claim_boundaries"])
    for phrase in [
        "No credentials",
        "customer identifiers",
        "No legal",
        "revenue",
        "ROI",
        "not a customer case study",
        "qualified owner review",
    ]:
        assert phrase in joined_boundaries


def test_saas_security_questionnaire_answer_card_is_discoverable():
    rel = "saas-security-questionnaire-answer-card.json"
    abs_url = f"https://aicloudstrategist.com/resources/{SLUG}/{rel}"
    assert f"/{SLUG}/{rel}" in PAGE.read_text(encoding="utf-8")
    assert abs_url in LLMS.read_text(encoding="utf-8")
    assert abs_url in SITEMAP.read_text(encoding="utf-8")
