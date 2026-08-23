from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "lead-leakage-calculator.html"
TOOLS = ROOT / "tools" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"
SITEMAP_SCRIPT = ROOT / "scripts" / "build_sitemap.py"
URL = "https://aicloudstrategist.com/lead-leakage-calculator"


def test_lead_leakage_calculator_has_canonical_conversion_route_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}">' in html
    assert "Lead Leakage Calculator" in html
    assert "Monthly enquiries" in html
    assert "Estimated missed / unanswered %" in html
    assert "Average value per converted customer" in html
    assert "Conversion chance after good follow-up %" in html
    assert "This is a planning estimate, not a guarantee." in html
    assert '/free-business-review' in html
    assert html.count('<h1>') == 1


def test_lead_leakage_calculator_is_discoverable_without_html_suffix():
    assert "/lead-leakage-calculator" in SITEMAP_SCRIPT.read_text(encoding="utf-8")
    assert f"<loc>{URL}</loc>" in SITEMAP.read_text(encoding="utf-8")
    assert f"Lead leakage calculator: {URL}" in LLMS.read_text(encoding="utf-8")
    assert "/lead-leakage-calculator.html" in TOOLS.read_text(encoding="utf-8")
