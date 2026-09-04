from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-cloud-cost-optimization-tool-shortlist-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "north-america-cloud-cost-shortlist-evidence.csv"
SVG = ROOT / "resources" / SLUG / "cloud-cost-tool-shortlist-owner-board.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
CLOUD_FINOPS = ROOT / "services" / "cloud-finops" / "index.html"
SITEMAP = ROOT / "sitemap.xml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_north_america_cloud_cost_shortlist_page_has_safe_positioning_and_schema():
    html = read(PAGE)
    assert "North America Cloud Cost Tool Shortlist Evidence Checklist" in html
    assert "cloud cost optimization tools" in html
    assert "FinOps managed service" in html
    assert "native AWS/Azure/GCP cost tools" in html
    for vendor in ["CloudZero", "Vantage", "IBM Apptio Cloudability", "Flexera"]:
        assert vendor in html
    for route in ["AWS Cloud Financial Management", "Microsoft Azure Cost Management", "Google Cloud Cost Management"]:
        assert route in html
    assert "Bing checks for unbranded searches returned HTTP 200 with no sampled AICS marker" in html
    assert "not a real North America client case study" in html
    for boundary in ["testimonial", "certification", "partner proof", "ranking evidence", "savings result", "ROI result", "cost-reduction claim"]:
        assert boundary in html
    assert '"@type":"Dataset"' in html
    assert '"@type":"ImageObject"' in html
    assert '"@type":"FAQPage"' in html


def test_north_america_cloud_cost_shortlist_artifacts_are_synthetic_and_no_credentials():
    csv = read(CSV)
    svg = read(SVG)
    assert "row_id,buyer_question,evidence_to_collect" in csv
    assert "No credentials no secrets no PHI/ePHI no personal data no production logs" in csv
    assert "No savings or cost reduction claim" in csv
    assert "Demo / synthetic artifact" in svg
    assert "no real cloud account, bill, client, ranking, savings or ROI claim" in svg


def test_shortlist_resource_is_discoverable_from_resources_llms_service_and_sitemap():
    resource_path = f"/resources/{SLUG}/"
    csv_path = f"/resources/{SLUG}/north-america-cloud-cost-shortlist-evidence.csv"
    svg_path = f"/resources/{SLUG}/cloud-cost-tool-shortlist-owner-board.svg"
    for html in [read(RESOURCES), read(LLMS), read(CLOUD_FINOPS)]:
        assert resource_path in html
        assert csv_path in html or "cloud-finops-service" in html
    resources = read(RESOURCES)
    assert csv_path in resources
    assert svg_path in resources
    llms = read(LLMS)
    assert csv_path in llms
    assert svg_path in llms
    service = read(CLOUD_FINOPS)
    assert "/free-business-review/?package=north-america-cloud-cost-tool-shortlist&amp;source=cloud-finops-service" in service
    sitemap = read(SITEMAP)
    assert f"https://aicloudstrategist.com{resource_path}" in sitemap
