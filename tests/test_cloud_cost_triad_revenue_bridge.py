import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
CLOUD_FINOPS = ROOT / "services" / "cloud-finops" / "index.html"

ROUTES = {
    "aws-bill-too-high-owner-action-checklist": {
        "label": "AWS bill too high owner-action diagnostic bridge",
        "resource": "/resources/aws-bill-too-high-owner-action-checklist/",
        "csv": "/resources/aws-bill-too-high-owner-action-checklist/aws-bill-too-high-owner-action-checklist.csv",
        "owner": "SMB / scale-up AWS cost owners",
        "schema_name": "AWS bill too high owner-action diagnostic",
        "boundary": "no AWS credentials",
    },
    "google-cloud-bill-too-high-owner-action-checklist": {
        "label": "Google Cloud bill too high owner-action diagnostic bridge",
        "resource": "/resources/google-cloud-bill-too-high-owner-action-checklist/",
        "csv": "/resources/google-cloud-bill-too-high-owner-action-checklist/google-cloud-bill-too-high-owner-action-checklist.csv",
        "owner": "SMB / scale-up Google Cloud cost owners",
        "schema_name": "Google Cloud bill too high owner-action diagnostic",
        "boundary": "no Google Cloud credentials",
    },
}


def _pricing_item_list(html: str) -> dict:
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)
    return next(json.loads(script) for script in scripts if "pricing#fixed-scope-diagnostics" in script)


def test_pricing_surfaces_aws_and_google_cloud_cost_diagnostics_without_fake_claims():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    for slug, route in ROUTES.items():
        assert f'data-revenue-bridge="{slug}"' in section
        assert route["label"] in section
        assert route["resource"] in section
        assert route["csv"] in section
        assert f"/free-business-review/?package={slug}&amp;source=pricing-fixed-scope" in section
        assert route["boundary"] in section
        for claim_boundary in ["ranking", "demand", "revenue", "savings", "ROI", "cost-reduction claim"]:
            assert claim_boundary in section


def test_pricing_schema_lists_cloud_cost_triad_services():
    item_list = _pricing_item_list(PRICING.read_text(encoding="utf-8"))
    urls = [item["url"] for item in item_list["itemListElement"]]

    assert item_list["numberOfItems"] == len(item_list["itemListElement"])
    for slug, route in ROUTES.items():
        url = "https://aicloudstrategist.com" + route["resource"]
        assert url in urls
        item = next(item for item in item_list["itemListElement"] if item["url"] == url)
        assert item["item"]["name"] == route["schema_name"]
        assert route["boundary"] in item["item"]["offers"]["priceSpecification"]["description"]


def test_free_review_routes_aws_and_google_cloud_cost_buyers_to_public_assets():
    for path in [FREE_REVIEW, FREE_REVIEW_FLAT]:
        html = path.read_text(encoding="utf-8")
        for slug, route in ROUTES.items():
            assert f'data-review-route="{slug}"' in html
            assert route["owner"] in html
            assert route["resource"] in html
            assert route["csv"] in html
            assert "/pricing.html#fixed-scope-diagnostics" in html


def test_cloud_finops_service_page_routes_cloud_cost_triad_to_scoped_reviews():
    html = CLOUD_FINOPS.read_text(encoding="utf-8")
    section = html.split('data-finops-revenue-bridge="cloud-finops-public-entry-paths"', 1)[1]

    for slug, route in ROUTES.items():
        assert route["resource"] in section
        assert f"/free-business-review/?package={slug}&amp;source=cloud-finops-service" in section
        assert route["boundary"] in section
