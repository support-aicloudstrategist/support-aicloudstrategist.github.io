import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "pricing.html"
URL = "https://aicloudstrategist.com/resources/global-retail-inventory-manual-work-owner-evidence-checklist/"
ROUTE = "/resources/global-retail-inventory-manual-work-owner-evidence-checklist/"


def _pricing_html() -> str:
    return HTML.read_text(encoding="utf-8")


def _ld_json_docs(source: str):
    return [json.loads(match) for match in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source)]


def test_pricing_surfaces_retail_inventory_as_sellable_diagnostic():
    html = _pricing_html()
    section = html.split('id="fixed-scope-diagnostics"', 1)[1].split('</section>', 1)[0]

    assert "Twenty concrete first offers buyers can understand before a custom build." in section
    assert "Retail inventory manual-work owner evidence diagnostic" in section
    assert ROUTE in section
    assert "stock-count delays, reorder triggers, supplier WhatsApp chasing" in section
    assert "purchase-order approvals, dead-stock decisions and POS/ERP spreadsheet gaps" in section
    assert "before buying ERP, inventory or AI automation tools" in section
    assert "no savings, stock-accuracy, revenue, supplier, compliance or ranking claims" in section


def test_pricing_itemlist_structured_data_includes_retail_inventory_offer():
    docs = _ld_json_docs(_pricing_html())
    itemlist = next(doc for doc in docs if doc.get("@type") == "ItemList")

    assert itemlist["numberOfItems"] == 20
    item = itemlist["itemListElement"][-1]
    assert item["position"] == 20
    assert item["url"] == URL
    assert item["item"]["name"] == "Retail inventory manual-work owner evidence diagnostic"
    assert item["item"]["areaServed"] == ["Global"]
    assert item["item"]["offers"]["priceSpecification"]["description"] == "Scope before quote; no credentials, live POS/ERP access or supplier/customer data required for first review."
