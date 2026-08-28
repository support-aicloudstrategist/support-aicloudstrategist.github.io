import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-demo-security-questionnaire-follow-up-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_demo_security_questionnaire_page_has_dataset_and_structured_data():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    assert f"/{SLUG}.csv" in html
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Dataset" and doc.get("url", "").endswith(f"/{SLUG}.csv") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)


def test_demo_security_questionnaire_csv_is_redaction_first_and_claim_safe():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) >= 8
    assert rows[0].keys() == {
        "blocker_area",
        "buyer_question",
        "redacted_evidence_to_collect",
        "accountable_owner",
        "ready_to_follow_up_when",
        "unsafe_claim_boundary",
    }
    csv_text = CSV.read_text(encoding="utf-8")
    for phrase in [
        "Do not expose prospect names deal IDs CRM exports or confidential questionnaire files",
        "Do not claim pipeline revenue win-rate sales-cycle or retention impact",
        "Do not request or store passwords tokens secrets PHI PII contracts revenue exports or raw security reports by default",
    ]:
        assert phrase in csv_text


def test_demo_security_questionnaire_truth_boundaries_and_discovery_are_wired():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "not a real B2B SaaS company",
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
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{PATH}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert html.count('data-aics-navigation-mount') == 1
    assert html.count('data-aics-global-footer') == 1
