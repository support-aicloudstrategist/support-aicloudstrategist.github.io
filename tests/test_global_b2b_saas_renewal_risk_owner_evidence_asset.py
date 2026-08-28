import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-renewal-risk-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_renewal_risk_page_is_indexable_canonical_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Dataset" and doc.get("url", "").endswith(f"/{SLUG}.csv") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_renewal_risk_page_contains_revenue_buyer_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "B2B SaaS renewal risk",
        "customer-success renewal checklist",
        "SaaS retention evidence",
        "customer health score evidence",
        "expansion blocker owner queue",
        "renewal risk dashboard",
        "executive sponsor gap",
        "source-to-owner evidence layer",
        "no-credentials renewal-risk review",
        "Claim boundaries",
    ]:
        assert phrase in html
    for boundary in [
        "not a real SaaS customer case study",
        "not customer data",
        "not CRM data",
        "not product analytics",
        "not a testimonial",
        "not a benchmark",
        "not evidence of renewal, retention, expansion, revenue, ROI, ranking, leads or customers",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "No outreach was sent",
    ]:
        assert boundary in html


def test_renewal_risk_csv_and_discovery_surfaces_are_wired():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) >= 5
    assert rows[0].keys() == {
        "renewal_stage",
        "risk_signal",
        "blocker_type",
        "accountable_owner",
        "redacted_evidence",
        "next_action",
        "unsafe_claim_boundary",
    }
    csv_text = CSV.read_text(encoding="utf-8")
    assert "Do not claim renewal saved, churn reduced or expansion improved" in csv_text
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{PATH}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
