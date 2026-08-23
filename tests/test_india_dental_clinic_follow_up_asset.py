from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "india-dental-clinic-missed-calls-whatsapp-follow-up-checklist" / "index.html"
REL = "/resources/india-dental-clinic-missed-calls-whatsapp-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_india_dental_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "dental clinic missed calls India",
        "WhatsApp dental appointment follow up",
        "Practo leads not converting",
        "treatment-plan follow-up",
        "DPDP consent evidence",
        "Truth boundary",
        "Top-3/top-5 consideration signals",
    ]:
        assert marker in source


def test_india_dental_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "No real dental clinic",
        "patient",
        "testimonial",
        "DPDP compliance",
        "revenue, ROI",
        "ranking",
        "AI-accuracy claim",
        "no medical, legal, privacy, advertising, dental, DPDP, security or compliance advice",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=india-dental-clinic-whatsapp-follow-up" in source
    assert "/case-studies/simulated-india-dental-clinic-whatsapp-no-show-dpdp-diagnostic/" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_india_dental_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
