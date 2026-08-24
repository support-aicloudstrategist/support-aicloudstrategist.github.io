import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-healthtech-ai-cloud-finops-trust-evidence-room"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "sample.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_is_indexable_canonical_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_page_contains_healthtech_buyer_language_and_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "healthtech cloud cost optimization",
        "healthcare SaaS FinOps",
        "AI spend governance",
        "HIPAA/SOC 2-style questionnaire evidence",
        "LLM/API",
        "AI vendor data-flow register",
        "human-review boundaries",
        "CloudZero, Vantage, Apptio Cloudability",
        "Vanta and Drata",
    ]:
        assert phrase in html
    for boundary in [
        "not a client case study",
        "not legal advice",
        "not HIPAA advice",
        "not privacy advice",
        "not security advice",
        "not a healthcare compliance proof",
        "not a guarantee of savings",
        "not a guarantee of savings, ROI, runway, revenue, ranking, questionnaire approval, procurement success, risk reduction, uptime, patient outcome or AI accuracy",
    ]:
        assert boundary in html


def test_sample_csv_is_downloadable_synthetic_and_safe():
    rows = list(csv.DictReader(CSV.read_text(encoding="utf-8").splitlines()))
    assert len(rows) >= 5
    assert {"row_type", "synthetic_source", "unit_metric", "data_boundary_flag", "claim_boundary"}.issubset(rows[0])
    assert all("Synthetic row only" in row["claim_boundary"] for row in rows)
    joined = "\n".join(CSV.read_text(encoding="utf-8").splitlines()).lower()
    for forbidden in ["real client", "guaranteed", "patient name", "phi sample"]:
        assert forbidden not in joined


def test_asset_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
