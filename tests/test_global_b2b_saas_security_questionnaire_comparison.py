import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-security-questionnaire-vs-grc-trust-center-tools-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "saas-security-questionnaire-comparison-matrix.csv"
SVG = ROOT / "resources" / SLUG / "saas-security-questionnaire-comparison-map.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_saas_security_questionnaire_comparison_is_indexable_and_tool_neutral():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    for phrase in [
        "security questionnaire takes too long",
        "GRC tool vs trust center",
        "AI security questionnaire answers",
        "vendor-risk evidence room",
        "questionnaire automation alternative",
        "AICS owner-evidence review",
        "saas-security-questionnaire-comparison-matrix.csv",
        "saas-security-questionnaire-comparison-map.svg",
        "Request diagnostic fit check",
    ]:
        assert phrase in html


def test_saas_security_questionnaire_comparison_discovery_surfaces():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Dataset" and doc.get("url", "").endswith("saas-security-questionnaire-comparison-matrix.csv") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{PATH}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert html.count('data-aics-navigation-mount') == 1
    assert html.count('data-aics-global-footer') == 1
    assert SVG.is_file()


def test_saas_security_questionnaire_comparison_csv_boundaries():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 8
    assert rows[0].keys() == {
        "buyer_situation",
        "grc_or_trust_center_route",
        "questionnaire_automation_route",
        "aics_owner_evidence_route",
        "unsafe_claim_boundary",
    }
    text = CSV.read_text(encoding="utf-8")
    for phrase in [
        "Do not invent certifications attestations compliance security approval or legal positions",
        "Do not expose confidential reports tokens passwords CRM exports customer names or contract files",
        "Do not request or store passwords tokens secrets PHI PII contracts revenue exports CRM exports or raw security reports by default",
    ]:
        assert phrase in text


def test_saas_security_questionnaire_comparison_truth_boundaries_prevent_fake_proof():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "not a real SaaS customer case study",
        "not customer data",
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
        "security evidence",
        "ranking evidence",
        "No outreach was sent",
    ]:
        assert phrase in html
    for forbidden in ["trusted by", "guaranteed conversion", "real client results", "increased revenue", "saved "]:
        assert forbidden not in html.lower()
