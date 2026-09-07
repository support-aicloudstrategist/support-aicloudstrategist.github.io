from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FACTORY = ROOT / "resources" / "customer-problem-search" / "factory-manual-work-reduce" / "index.html"
CSV = ROOT / "resources" / "customer-problem-search" / "factory-manual-work-reduce" / "factory-manual-work-owner-evidence.csv"


def test_pricing_surfaces_factory_manual_work_revenue_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split('<section class="section pricing-showcase">', 1)[0]
    assert "Thirty-five concrete first offers" in section
    assert 'data-revenue-bridge="factory-manual-work-reduction"' in section
    assert "Factory manual-work reduction diagnostic bridge" in section
    assert "/resources/customer-problem-search/factory-manual-work-reduce/" in section
    assert "/resources/customer-problem-search/factory-manual-work-reduce/factory-manual-work-owner-evidence.csv" in section
    assert "/free-business-review/?package=factory-manual-work-reduction&amp;source=pricing-fixed-scope" in section
    assert "/services/workflow-automation/" in section
    forbidden_claims = ["guaranteed saving", "productivity gain", "delivery improvement", "real factory client"]
    assert "no real factory client" in section
    assert "job-cut, savings, productivity, delivery, revenue" in section


def test_factory_manual_work_offer_is_in_fixed_scope_json_ld():
    html = PRICING.read_text(encoding="utf-8")
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)
    item_lists = [json.loads(script) for script in scripts if 'pricing#fixed-scope-diagnostics' in script]
    assert len(item_lists) == 1
    item_list = item_lists[0]
    assert item_list["numberOfItems"] == 35
    item = next(entry for entry in item_list["itemListElement"] if entry["url"].endswith("/resources/customer-problem-search/factory-manual-work-reduce/"))
    assert item["position"] == 35
    assert item["item"]["name"] == "Factory manual-work reduction evidence review"
    assert item["item"]["offers"]["availability"] == "https://schema.org/InStock"
    assert "no factory client data" in item["item"]["offers"]["priceSpecification"]["description"]


def test_factory_problem_page_points_back_to_pricing_bridge():
    html = FACTORY.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert "/free-business-review/?package=factory-manual-work-reduction" in html
    assert "evidence_area" in csv
    assert "database credentials" in csv
