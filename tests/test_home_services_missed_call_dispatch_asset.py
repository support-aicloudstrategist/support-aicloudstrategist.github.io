from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-home-services-missed-call-dispatch-evidence-checklist" / "index.html"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_home_services_asset_has_public_seo_and_schema_markers():
    html = source()
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/global-home-services-missed-call-dispatch-evidence-checklist/"' in html
    assert '<meta name="robots" content="index, follow"' in html
    assert len(re.findall(r'<script type="application/ld\+json">', html)) >= 4
    assert html.count("<h1>") == 1
    for marker in [
        "HVAC company missed calls booking software dispatch CRM",
        "plumbing company missed calls scheduling software owner dashboard",
        "field-service dispatch handoff evidence",
        "answering service owner queue",
        "AI receptionist human review boundary",
        "Truth boundary",
    ]:
        assert marker in html


def test_home_services_asset_has_truth_boundaries_and_conversion_route():
    html = source()
    for boundary in [
        "No real HVAC contractor",
        "customer data",
        "testimonial",
        "revenue, ROI",
        "AI-accuracy claim",
        "no legal, privacy, security, employment, trade-licensing or safety advice",
    ]:
        assert boundary in html
    assert "/free-business-review/?package=home-services-missed-call-dispatch-evidence" in html
    assert "/resources/" in html
    assert "/llms.txt" in html


def test_home_services_asset_is_linked_from_discovery_surfaces():
    rel = "/resources/global-home-services-missed-call-dispatch-evidence-checklist/"
    assert rel in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert rel in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
