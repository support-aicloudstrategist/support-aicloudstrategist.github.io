from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "resources" / "aws-bill-too-high-owner-action-checklist" / "index.html"
CSV = ROOT / "resources" / "aws-bill-too-high-owner-action-checklist" / "aws-bill-too-high-owner-action-checklist.csv"
SVG = ROOT / "resources" / "aws-bill-too-high-owner-action-checklist" / "aws-owner-action-board.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_aws_bill_too_high_page_has_search_and_trust_markers():
    html = RESOURCE.read_text(encoding="utf-8")
    for marker in [
        "AWS bill too high",
        "unexpected AWS bill",
        "AWS Cost Explorer review",
        "AWS cost optimization small business",
        "owner action board",
        "Buyer alternatives considered",
        "AWS Cost Explorer / Budgets / Trusted Advisor",
        "MSP or AWS consultant",
        "FinOps platform",
        "not a real AWS account",
        "No outreach was sent",
    ]:
        assert marker in html


def test_aws_bill_too_high_download_assets_are_linked_and_bounded():
    html = RESOURCE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")

    assert "/resources/aws-bill-too-high-owner-action-checklist/aws-bill-too-high-owner-action-checklist.csv" in html
    assert "/resources/aws-bill-too-high-owner-action-checklist/aws-owner-action-board.svg" in html
    assert "unsupported_claim_stop" in csv
    assert "No savings claim until two billing windows are reviewed" in csv
    assert "Demo-labelled · no credentials" in svg
    assert "No savings, ROI" in svg


def test_aws_bill_too_high_discovery_surfaces_include_new_asset():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    for surface in [resources_html, llms, sitemap]:
        assert "/resources/aws-bill-too-high-owner-action-checklist/" in surface
    assert "aws-bill-too-high-owner-action-checklist.csv" in resources_html
    assert "aws-owner-action-board.svg" in resources_html
    assert "AWS bill too high owner action checklist" in llms
