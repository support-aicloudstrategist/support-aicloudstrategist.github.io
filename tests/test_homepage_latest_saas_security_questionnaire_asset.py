from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-09-09" / "saas-security-questionnaire-evidence-pack.html"
CSV = ROOT / "publications" / "2026-09-09" / "saas-security-questionnaire-evidence-pack.csv"
PNG = ROOT / "publications" / "2026-09-09" / "saas-security-questionnaire-evidence-pack.png"


def test_homepage_surfaces_latest_saas_security_questionnaire_asset():
    html = HOME.read_text(encoding="utf-8")
    assert 'data-homepage-resource="saas-security-questionnaire-evidence-pack"' in html
    assert "/publications/2026-09-09/saas-security-questionnaire-evidence-pack.html" in html
    assert "SaaS Security Questionnaire Evidence Pack: 7 Red Flags Before AI Answers" in html
    assert "approved sources, proof links and human approval" in html


def test_latest_saas_security_questionnaire_asset_files_exist():
    assert PUBLICATION.exists()
    assert CSV.exists()
    assert PNG.exists()
    publication_html = PUBLICATION.read_text(encoding="utf-8")
    assert "Download CSV worksheet" in publication_html
    assert "When this should become a paid diagnostic" in publication_html
