from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "saas-security-questionnaire-takes-too-long-ai-evidence-checklist" / "index.html"
CSV = ROOT / "resources" / "saas-security-questionnaire-takes-too-long-ai-evidence-checklist" / "saas-security-questionnaire-owner-evidence.csv"
HUB = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_saas_security_questionnaire_page_has_buyer_pain_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "SaaS security questionnaire takes too long" in html
    assert "No customer, contract, security report, production system, private audit or compliance certification is claimed" in html
    assert "Request a no-credentials evidence gap review" in html
    assert "FAQPage" in html
    assert "Dataset" in html
    assert "saas-security-questionnaire-owner-evidence.csv" in html


def test_saas_security_questionnaire_csv_has_owner_routes():
    csv = CSV.read_text(encoding="utf-8")
    assert "buyer_question,route,approved_source_type,owner_role,do_not_claim" in csv
    assert "adviser-needed" in csv
    assert "Do not imply certification without current evidence" in csv


def test_saas_security_questionnaire_discovery_routes_are_wired():
    path = "/resources/saas-security-questionnaire-takes-too-long-ai-evidence-checklist/"
    assert path in HUB.read_text(encoding="utf-8")
    assert "saas-security-questionnaire-owner-evidence.csv" in HUB.read_text(encoding="utf-8")
    assert path in LLMS.read_text(encoding="utf-8")
    assert path in SITEMAP.read_text(encoding="utf-8")
