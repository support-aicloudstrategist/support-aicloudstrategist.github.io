from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "resources" / "google-cloud-bill-too-high-owner-action-checklist" / "index.html"
CSV = ROOT / "resources" / "google-cloud-bill-too-high-owner-action-checklist" / "google-cloud-bill-too-high-owner-action-checklist.csv"
SVG = ROOT / "resources" / "google-cloud-bill-too-high-owner-action-checklist" / "google-cloud-owner-action-board.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_google_cloud_bill_too_high_page_has_search_and_trust_markers():
    html = RESOURCE.read_text(encoding="utf-8")
    for marker in [
        "Google Cloud bill too high",
        "GCP bill too high",
        "unexpected Google Cloud bill",
        "BigQuery cost spike",
        "owner action board",
        "Buyer alternatives considered",
        "Google Cloud Billing / Budgets / Recommender",
        "MSP or Google Cloud consultant",
        "FinOps platform",
        "not a real Google Cloud project",
        "No outreach was sent",
    ]:
        assert marker in html


def test_google_cloud_bill_too_high_download_assets_are_linked_and_bounded():
    html = RESOURCE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")

    assert "/resources/google-cloud-bill-too-high-owner-action-checklist/google-cloud-bill-too-high-owner-action-checklist.csv" in html
    assert "/resources/google-cloud-bill-too-high-owner-action-checklist/google-cloud-owner-action-board.svg" in html
    assert "unsupported_claim_stop" in csv
    assert "No savings claim until two billing windows are reviewed" in csv
    assert "Demo-labelled · no credentials" in svg
    assert "No savings, ROI" in svg


def test_google_cloud_bill_too_high_discovery_surfaces_include_new_asset():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    for surface in [resources_html, llms, sitemap]:
        assert "/resources/google-cloud-bill-too-high-owner-action-checklist/" in surface
    assert "google-cloud-bill-too-high-owner-action-checklist.csv" in resources_html
    assert "google-cloud-owner-action-board.svg" in resources_html
    assert "Google Cloud bill too high owner action checklist" in llms
