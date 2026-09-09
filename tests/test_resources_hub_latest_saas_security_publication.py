from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "resources" / "index.html"
PUBLICATION = ROOT / "publications" / "2026-09-09" / "saas-security-questionnaire-evidence-pack.html"
CSV = ROOT / "publications" / "2026-09-09" / "saas-security-questionnaire-evidence-pack.csv"
ANSWER_CARD = ROOT / "publications" / "2026-09-09" / "saas-security-questionnaire-answer-card.json"


def test_resources_hub_features_latest_saas_security_publication():
    html = HUB.read_text(encoding="utf-8")
    assert 'data-featured-publication="saas-security-questionnaire-evidence-pack"' in html
    assert "/publications/2026-09-09/saas-security-questionnaire-evidence-pack.html" in html
    assert "Featured: SaaS Security Questionnaire Evidence Pack" in html
    assert "approved sources, proof links and human approval" in html
    assert "/publications/2026-09-09/saas-security-questionnaire-evidence-pack.csv" in html
    assert "/publications/2026-09-09/saas-security-questionnaire-answer-card.json" in html


def test_latest_saas_security_publication_assets_exist_and_are_claim_safe():
    page = PUBLICATION.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    answer = ANSWER_CARD.read_text(encoding="utf-8")
    assert "customer-result" in page.lower()
    assert "legal advice" in page.lower()
    assert "safe_first_action" in csv
    assert "boundary" in answer
    for forbidden in ["trusted by", "guaranteed compliance", "increased revenue"]:
        assert forbidden not in page.lower()
