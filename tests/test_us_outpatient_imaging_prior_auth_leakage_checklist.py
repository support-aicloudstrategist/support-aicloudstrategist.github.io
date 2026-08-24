import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-outpatient-imaging-referral-prior-auth-leakage-checklist"
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


def test_page_contains_imaging_buyer_language_and_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "outpatient imaging",
        "prior authorization automation for radiology",
        "patient access referral management",
        "referral-to-scheduled-study visibility",
        "prior-auth ageing queues",
        "eligibility verification workflow",
        "radiology scheduling bottleneck",
        "safe AI callback boundaries",
        "proof-before-platform layer",
    ]:
        assert phrase in html
    for boundary in [
        "not a real customer case study",
        "not a testimonial",
        "not a prior-authorization submission service",
        "not payer-contracting advice",
        "not medical advice",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not proof of HIPAA compliance",
        "not proof of HIPAA compliance, authorization-speed improvement, denial reduction, patient outcome, booked studies, revenue, ROI, ranking, certification, official platform partnership or AI accuracy",
    ]:
        assert boundary in html


def test_sample_csv_is_downloadable_synthetic_and_safe():
    rows = list(csv.DictReader(CSV.read_text(encoding="utf-8").splitlines()))
    assert len(rows) >= 5
    assert {"request_id", "modality_or_service_line", "prior_auth_status", "next_safe_action", "claim_boundary"}.issubset(rows[0])
    assert all("Synthetic row only" in row["claim_boundary"] for row in rows)
    joined = "\n".join(CSV.read_text(encoding="utf-8").splitlines()).lower()
    for forbidden in ["real client", "guaranteed", "patient name", "phi sample"]:
        assert forbidden not in joined


def test_asset_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
