import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-retail-inventory-manual-work-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_retail_inventory_page_is_indexable_canonical_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Dataset" and doc.get("url", "").endswith(f"/{SLUG}.csv") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_retail_inventory_page_contains_buyer_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "retail inventory manual work",
        "shop inventory follow up checklist",
        "stock count owner queue",
        "purchase order follow up",
        "supplier WhatsApp chasing",
        "AI automation for retail store",
        "POS ERP spreadsheet inventory gaps",
        "source-to-owner evidence layer",
        "no-credentials retail workflow review",
        "Claim boundaries",
    ]:
        assert phrase in html
    for boundary in [
        "not a real retailer case study",
        "not store data",
        "not customer data",
        "not POS data",
        "not ERP data",
        "not a testimonial",
        "not a benchmark",
        "not evidence of sales, margin, stock accuracy, savings, revenue, ROI, ranking, leads or customers",
        "not accounting advice",
        "No outreach was sent",
    ]:
        assert boundary in html


def test_retail_inventory_csv_and_discovery_surfaces_are_wired():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) >= 8
    assert rows[0].keys() == {
        "inventory_stage",
        "manual_work_signal",
        "blocker_type",
        "accountable_owner",
        "redacted_evidence",
        "next_action",
        "unsafe_claim_boundary",
    }
    csv_text = CSV.read_text(encoding="utf-8")
    assert "Do not claim stock accuracy improved without measured before/after evidence" in csv_text
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{PATH}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
