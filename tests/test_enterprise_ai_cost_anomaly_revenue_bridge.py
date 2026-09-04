import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/global-enterprise-ai-cost-anomaly-approval-runbook/"
CSV = RESOURCE + "ai-cost-anomaly-approval-log-template.csv"
SVG = RESOURCE + "ai-cost-anomaly-approval-flow.svg"
PACKAGE = "global-enterprise-ai-cost-anomaly-approval-runbook"


def _pricing_item_list(html: str) -> dict:
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)
    return next(json.loads(script) for script in scripts if "pricing#fixed-scope-diagnostics" in script)


def test_pricing_surfaces_enterprise_ai_cost_anomaly_bridge_without_fake_claims():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert f'data-revenue-bridge="{PACKAGE}"' in section
    assert "Enterprise AI cost anomaly approval diagnostic bridge" in section
    assert "Scope before LLM/GPU budget changes, FinOps platform rollout, MSP escalation or unsafe workload shutdown" in section
    assert RESOURCE in section
    assert CSV in section
    assert f"/free-business-review/?package={PACKAGE}&amp;source=pricing-fixed-scope" in section
    for boundary in [
        "no cloud credentials",
        "billing-console access",
        "invoice",
        "production logs",
        "vendor partnership",
        "ranking",
        "demand",
        "revenue",
        "savings",
        "ROI",
        "cost-reduction claim",
    ]:
        assert boundary in section


def test_pricing_schema_lists_enterprise_ai_cost_anomaly_service():
    item_list = _pricing_item_list(PRICING.read_text(encoding="utf-8"))
    urls = [item["url"] for item in item_list["itemListElement"]]

    assert item_list["numberOfItems"] == len(item_list["itemListElement"])
    assert "https://aicloudstrategist.com/resources/global-enterprise-ai-cost-anomaly-approval-runbook/" in urls
    cost_item = next(item for item in item_list["itemListElement"] if item["url"].endswith("/global-enterprise-ai-cost-anomaly-approval-runbook/"))
    assert cost_item["item"]["name"] == "Enterprise AI cost anomaly approval diagnostic"
    assert "no cloud credentials" in cost_item["item"]["offers"]["priceSpecification"]["description"]


def test_free_review_routes_enterprise_ai_finops_buyers_to_public_asset():
    for path in [FREE_REVIEW, FREE_REVIEW_FLAT]:
        html = path.read_text(encoding="utf-8")
        assert f'data-review-route="{PACKAGE}"' in html
        assert "Enterprise AI / FinOps cost owners" in html
        assert "no-credentials owner gate before FinOps platform, MSP or workload-shutdown spend" in html
        assert RESOURCE in html
        assert CSV in html
        assert SVG in html
        assert "/pricing.html#fixed-scope-diagnostics" in html
