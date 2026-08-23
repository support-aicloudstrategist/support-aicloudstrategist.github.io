from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "restaurant-missed-bookings-whatsapp-follow-up-checklist" / "index.html"
REL = "/resources/restaurant-missed-bookings-whatsapp-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_restaurant_missed_bookings_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "restaurant missed calls booking follow up",
        "restaurant WhatsApp reservation follow up",
        "restaurant no-show recovery checklist",
        "restaurant private event enquiry owner dashboard",
        "restaurant delivery app complaint handoff",
        "Top-3/top-5 consideration signals",
        "Truth boundary",
    ]:
        assert marker in source


def test_restaurant_missed_bookings_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "No real restaurant",
        "customer",
        "testimonial",
        "official platform partnership",
        "revenue, ROI",
        "ranking",
        "advertising performance",
        "AI-accuracy claim",
        "no legal, tax, food-safety, labour, advertising, privacy, security or platform-policy advice",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=restaurant-missed-bookings-whatsapp-follow-up" in source
    assert "/growth-control-os/" in source
    assert "/resources/customer-problem-search/restaurant-local-service-customers-increase/" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_restaurant_missed_bookings_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
