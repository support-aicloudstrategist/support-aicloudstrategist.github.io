import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-construction-contractor-quote-change-order-follow-up-checklist" / "index.html"
URL = "https://aicloudstrategist.com/resources/global-construction-contractor-quote-change-order-follow-up-checklist/"
REL = "/resources/global-construction-contractor-quote-change-order-follow-up-checklist/"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_construction_asset_has_public_seo_and_schema_markers():
    html = source()
    assert f'<link rel="canonical" href="{URL}"' in html
    assert '<meta name="robots" content="index, follow"' in html
    assert len(re.findall(r'<script type="application/ld\+json">', html)) >= 4
    assert html.count("<h1>") == 1
    for marker in [
        "construction contractor missed calls",
        "contractor quote follow-up checklist",
        "construction CRM follow up",
        "change order tracking spreadsheet",
        "WhatsApp contractor quote follow-up",
        "field service software vs CRM for contractors",
        "construction project management handoff checklist",
        "AI assistant for contractors",
    ]:
        assert marker in html


def test_construction_asset_has_truth_boundaries_and_conversion_route():
    html = source()
    for boundary in [
        "No real contractor",
        "customer data",
        "client result",
        "testimonial",
        "revenue, ROI, ranking",
        "AI-accuracy claim",
        "not legal, contract, engineering, safety",
    ]:
        assert boundary in html
    assert "/free-business-review/?package=construction-contractor-quote-change-order-follow-up" in html
    assert "/growth-control-os/" in html
    assert "/llms.txt" in html


def test_construction_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
