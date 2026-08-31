import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-security-questionnaire-diagnostic-package"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "b2b-saas-security-questionnaire-diagnostic-intake.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_b2b_saas_security_questionnaire_diagnostic_page_is_indexable_and_sellable():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    for phrase in [
        "B2B SaaS security questionnaire diagnostic",
        "SaaS procurement blocker review",
        "vendor-risk evidence room",
        "DPA MSA blocker handoff",
        "AI-use questionnaire response owner",
        "fixed-scope diagnostic before platform work",
        "Request diagnostic fit check",
        "b2b-saas-security-questionnaire-diagnostic-intake.csv",
    ]:
        assert phrase in html


def test_b2b_saas_security_questionnaire_diagnostic_structured_data_and_discovery():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Dataset" and doc.get("url", "").endswith("b2b-saas-security-questionnaire-diagnostic-intake.csv") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "Service" and doc.get("name") == "B2B SaaS security questionnaire diagnostic package" for doc in docs)
    assert "b2b-saas-security-questionnaire-owner-dashboard.svg" in html
    assert "security questionnaire takes too long" in html
    assert (ROOT / "resources" / SLUG / "b2b-saas-security-questionnaire-owner-dashboard.svg").is_file()
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{PATH}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert html.count('data-aics-navigation-mount') == 1
    assert html.count('data-aics-global-footer') == 1


def test_b2b_saas_security_questionnaire_diagnostic_csv_is_no_credentials_and_owner_led():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 10
    assert rows[0].keys() == {
        "blocker_type",
        "buyer_question",
        "redacted_evidence_to_collect",
        "accountable_owner",
        "safe_follow_up_when",
        "unsafe_claim_boundary",
    }
    csv_text = CSV.read_text(encoding="utf-8")
    for phrase in [
        "Do not expose raw security reports, confidential findings, prospect names, deal IDs, access logs, passwords, tokens or secrets",
        "Do not invent customers, testimonials, rankings, revenue, analytics, logos, savings, outcomes or reference availability",
        "Do not request or store passwords tokens secrets PHI PII contracts revenue exports CRM exports or raw security reports by default",
    ]:
        assert phrase in csv_text


def test_b2b_saas_security_questionnaire_diagnostic_truth_boundaries_prevent_fake_proof():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "not a real SaaS customer case study",
        "not customer data",
        "not CRM data",
        "not product analytics",
        "not security evidence",
        "not a testimonial",
        "not a benchmark",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not compliance advice",
        "not procurement advice",
        "not product advice",
        "not financial advice",
        "lead evidence",
        "customer evidence",
        "conversion evidence",
        "pipeline evidence",
        "revenue evidence",
        "retention evidence",
        "ROI evidence",
        "compliance evidence",
        "ranking evidence",
        "No outreach was sent",
    ]:
        assert phrase in html
    for forbidden in ["trusted by", "guaranteed conversion", "real client results", "increased revenue", "saved "]:
        assert forbidden not in html.lower()
