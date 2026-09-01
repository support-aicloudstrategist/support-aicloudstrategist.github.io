import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthtech-ai-patient-access-procurement-answer-bank"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = PAGE.parent / "us-healthtech-ai-patient-access-procurement-answer-bank.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"
CSV_URL = f"{URL}us-healthtech-ai-patient-access-procurement-answer-bank.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_us_healthtech_answer_bank_is_indexable_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    flat = []
    for doc in docs:
        flat.extend(doc.get("@graph", [doc]))
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in flat)
    assert any(doc.get("@type") == "Dataset" and doc.get("url") == CSV_URL for doc in flat)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_page_contains_buyer_language_competitors_and_truth_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "US Healthtech AI + Patient Access Procurement Answer Bank",
        "HIPAA AI questionnaire",
        "patient engagement platform comparison",
        "healthcare AI vendor risk",
        "cloud FinOps for healthcare SaaS",
        "PHI/ePHI boundary",
        "BAA/subprocessor evidence",
        "AI human review",
        "security questionnaire",
        "cloud/LLM FinOps",
        "Luma Health",
        "Notable",
        "Phreesia",
        "NexHealth",
        "Artera",
        "Vanta",
        "Drata",
        "OneTrust",
        "CloudZero",
        "Download CSV answer bank",
        "us-healthtech-ai-patient-access-procurement-answer-bank.csv",
        "No outreach was sent",
    ]:
        assert phrase in html
    for boundary in [
        "synthetic/demo procurement answer-bank template",
        "not a real healthtech customer case study",
        "not patient data",
        "not PHI/ePHI",
        "not production cloud data",
        "not a testimonial",
        "not certification",
        "not HIPAA compliance attestation",
        "not SOC 2 or HITRUST proof",
        "not legal/privacy/security/medical/billing/coding/procurement advice",
        "not ranking evidence",
        "not procurement approval",
        "not questionnaire approval",
        "not savings evidence",
        "not ROI evidence",
        "not revenue evidence",
    ]:
        assert boundary in html


def test_csv_answer_bank_is_synthetic_and_operational():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    assert len(rows) >= 10
    assert set(rows[0]) == {
        "Lane",
        "Buyer question or claim",
        "Allowed answer source",
        "Approved answer owner",
        "Adviser route",
        "Freshness rule",
        "Blocked claim",
    }
    lanes = {row["Lane"] for row in rows}
    for lane in ["Patient access", "HIPAA PHI BAA", "Security questionnaire", "AI human review", "Cloud LLM FinOps", "Procurement boundary"]:
        assert lane in lanes
    combined = "\n".join(",".join(row.values()) for row in rows)
    for phrase in [
        "No-credentials intake policy",
        "Do not claim HIPAA compliance",
        "Do not claim authorization speed denial reduction or appointment growth",
        "Do not claim SOC 2 HITRUST ISO HIPAA or audit compliance",
        "Do not claim savings ROI runway impact or cost reduction without verified baseline",
        "Do not request sensitive access before scope and approvals",
    ]:
        assert phrase in combined


def test_answer_bank_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert CSV_URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    comparison = (ROOT / "resources" / "us-healthtech-growthos-vs-patient-engagement-grc-finops-comparison" / "index.html").read_text(encoding="utf-8")
    assert PATH in comparison
