import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-retail-inventory-manual-work-diagnostic-package"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
HREF = f"/resources/{SLUG}/"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP_BUILDER = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_retail_inventory_diagnostic_package_is_indexable_structured_and_sellable():
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{URL}"/>' in PAGE
    assert "Retail Inventory Manual Work Diagnostic Package" in PAGE
    assert "Fixed-scope package deliverables" in PAGE
    docs = json_ld_documents(PAGE)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Service" and doc.get("name") == "Retail Inventory Manual Work Diagnostic Package" for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)


def test_retail_inventory_diagnostic_package_targets_buyer_language_and_safe_boundaries():
    for phrase in [
        "retail inventory manual work",
        "stock count owner queue",
        "reorder trigger ownership",
        "supplier WhatsApp chasing",
        "purchase order follow up",
        "POS ERP spreadsheet inventory gaps",
        "AI automation for retail store",
        "inventory app vs process automation",
        "source-to-owner evidence layer",
        "no credentials first",
    ]:
        assert phrase in PAGE
    for boundary in [
        "not a real retailer case study",
        "not store data",
        "not customer data",
        "not POS data",
        "not ERP data",
        "not a testimonial",
        "not a benchmark",
        "not accounting advice",
        "not evidence of sales, margin, stock accuracy, stockout reduction, savings, revenue, ROI, ranking, demand, leads or customers",
        "No outreach was sent",
    ]:
        assert boundary in PAGE


def test_retail_inventory_diagnostic_package_is_wired_to_discovery_surfaces():
    assert HREF in RESOURCES
    assert "Retail Inventory Manual Work Diagnostic Package" in RESOURCES
    assert URL in LLMS
    assert f'"{HREF}"' in SITEMAP_BUILDER
