from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-budget-overrun-approval-log-template"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-pilot-budget-overrun-approval-log-template.csv"
SVG = ROOT / "resources" / SLUG / "ai-pilot-budget-overrun-owner-board.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
SVG_URL = f"{URL}ai-pilot-budget-overrun-owner-board.svg"


def json_ld_blocks(html: str):
    pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
    return [json.loads(match.group(1)) for match in pattern.finditer(html)]


def test_ai_pilot_budget_overrun_page_and_csv_exist_with_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    assert "AI pilot budget overrun approval log template" in html
    assert "Download CSV template" in html
    assert "Budget overrun approval fields" in html
    assert "Scale-cost scenario" in html
    assert "LLM usage" in html
    assert "Open owner-board visual" in html
    assert "Owner-board visual for the first budget meeting" in html
    assert "ai-pilot-budget-overrun-owner-board.svg" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert URL in html
    assert SVG.exists()
    svg = SVG.read_text(encoding="utf-8")
    assert "Synthetic AI pilot budget overrun owner board" in svg
    assert "opportunity estimates are not delivered value" in svg
    assert "Boundary: synthetic visual only" in svg
    assert "control_id,control_area,evidence_to_collect,owner" in csv
    assert "Variance driver" in csv
    assert "Adviser questions" in csv


def test_ai_pilot_budget_overrun_structured_data_and_discovery():
    html = PAGE.read_text(encoding="utf-8")
    blocks = json_ld_blocks(html)
    assert any(block.get("@type") == "BreadcrumbList" for block in blocks)
    graph = next(block["@graph"] for block in blocks if "@graph" in block)
    article = next(item for item in graph if item.get("@type") == "Article")
    image = next(item for item in graph if item.get("@type") == "ImageObject")
    assert article["mainEntityOfPage"] == URL
    assert article["image"] == SVG_URL
    assert image["contentUrl"] == SVG_URL
    assert any("AI pilot budget overrun" in topic for topic in article["about"])
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert "Open owner-board SVG" in resources
    assert URL in llms
    assert SVG_URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
    assert URL in sitemap


def test_ai_pilot_budget_overrun_internal_links_are_existing_targets():
    html = PAGE.read_text(encoding="utf-8")
    for href in [
        "/resources/cloud-ai-economics-decision-pack/",
        "/services/cloud-finops/",
        "/resources/global-enterprise-ai-cost-anomaly-approval-runbook/",
        "/resources/ai-cost-savings-claim-boundary-worksheet/",
        "/resources/global-ai-pilot-production-go-no-go-decision-record-template/",
        "/resources/",
    ]:
        assert href in html
        target = ROOT / href.strip("/") / "index.html"
        assert target.exists(), href
