import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-enterprise-ai-model-evaluation-regression-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "evidence-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_model_evaluation_regression_page_is_indexable_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_model_evaluation_regression_asset_contains_search_intent_and_truth_boundary():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Enterprise AI model evaluation regression evidence checklist",
        "AI model evaluation regression checklist",
        "LLM regression testing evidence",
        "prompt change approval evidence",
        "retrieval quality evaluation",
        "AI release gate evidence",
        "model, prompt, retrieval source or agent tool change",
        "Release and rollback ownership",
        "evidence-template.csv",
    ]:
        assert phrase in html
    for boundary in [
        "not a real customer case study",
        "not customer proof",
        "not a testimonial",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not compliance advice",
        "not AI performance proof",
        "not ROI proof",
        "not a guarantee of model accuracy, safety, compliance, revenue, adoption or production success",
        "No outreach was sent",
    ]:
        assert boundary in html


def test_model_evaluation_regression_csv_template_is_complete():
    csv = CSV.read_text(encoding="utf-8")
    assert csv.startswith("lane,check,green_evidence,score_status,owner,release_decision,notes")
    for lane in [
        "Baseline behavior",
        "Regression test set",
        "Safety and policy gates",
        "Retrieval and source quality",
        "Cost and latency impact",
        "Release and rollback ownership",
    ]:
        assert lane in csv
    assert csv.count("\n") >= 18


def test_model_evaluation_regression_asset_is_discoverable():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
