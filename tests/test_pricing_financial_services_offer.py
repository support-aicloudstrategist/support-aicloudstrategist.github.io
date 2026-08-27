import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def _pricing_html() -> str:
    return PRICING.read_text(encoding="utf-8")


def _fixed_scope_section(html: str) -> str:
    match = re.search(r'<section class="section" id="fixed-scope-diagnostics">(.*?)<section class="section pricing-showcase">', html, re.S)
    assert match, "fixed-scope diagnostics section missing"
    return match.group(1)


def test_pricing_surfaces_financial_services_intake_approval_as_sellable_first_step():
    section = _fixed_scope_section(_pricing_html())
    assert "Fifteen concrete first offers buyers can understand before a custom build." in section
    assert "Financial services AI intake approval evidence review" in section
    assert "/resources/global-financial-services-ai-intake-approval-evidence-checklist/" in section
    assert "client intake, document chasing, AI draft boundaries" in section
    assert "risk-review queues, approval evidence and cloud/AI spend ownership" in section
    assert "no legal, financial-advice, compliance, regulated-approval, ranking, revenue or ROI claims" in section


def test_pricing_itemlist_structured_data_includes_financial_services_offer():
    html = _pricing_html()
    match = re.search(r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList".*?})</script>', html)
    assert match, "pricing ItemList structured data missing"
    data = json.loads(match.group(1))
    offer_url = "https://aicloudstrategist.com/resources/global-financial-services-ai-intake-approval-evidence-checklist/"
    assert data["numberOfItems"] == 15
    urls = [item["url"] for item in data["itemListElement"]]
    assert offer_url in urls
    item = next(item for item in data["itemListElement"] if item["url"] == offer_url)
    assert item["item"]["name"] == "Financial services AI intake approval evidence review"
    assert item["item"]["offers"]["priceSpecification"]["description"].startswith("Scope before quote")
