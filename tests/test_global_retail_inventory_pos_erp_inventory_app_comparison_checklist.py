import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-retail-inventory-pos-erp-inventory-app-comparison-checklist"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
HREF = f"/resources/{SLUG}/"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP_BUILDER = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_retail_inventory_comparison_checklist_is_indexable_and_structured():
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{URL}"/>' in PAGE
    assert "Retail Inventory POS vs ERP vs Inventory App Comparison Checklist" in PAGE
    assert "Tool-fit comparison checklist" in PAGE
    docs = json_ld_documents(PAGE)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)


def test_retail_inventory_comparison_targets_tool_fit_buyer_language():
    for phrase in [
        "retail inventory POS ERP comparison",
        "inventory app vs process automation",
        "POS ERP spreadsheet inventory gaps",
        "stock count owner queue",
        "reorder trigger ownership",
        "supplier WhatsApp chasing",
        "purchase order follow up",
        "AI automation for retail store",
        "proof-before-platform boundaries",
        "no credentials first",
    ]:
        assert phrase in PAGE
    for option in ["POS add-on", "ERP module", "Inventory app", "Spreadsheet/BI dashboard", "Process automation or AI agent"]:
        assert option in PAGE


def test_retail_inventory_comparison_has_safe_claim_boundaries():
    for boundary in [
        "not a vendor ranking",
        "not a real retailer case study",
        "not store data",
        "not customer data",
        "not POS data",
        "not ERP data",
        "not a testimonial",
        "not a benchmark",
        "not accounting advice",
        "not evidence of stock accuracy, stockout reduction, sales, margin, savings, revenue, ROI, ranking, demand, leads or customers",
        "No outreach was sent",
        "Do not send passwords, tokens, payment data, raw sales exports or customer data",
    ]:
        assert boundary in PAGE


def test_retail_inventory_comparison_is_wired_to_discovery_surfaces():
    assert HREF in RESOURCES
    assert "Retail Inventory POS vs ERP vs Inventory App Comparison Checklist" in RESOURCES
    assert URL in LLMS
    assert f'"{HREF}"' in SITEMAP_BUILDER
