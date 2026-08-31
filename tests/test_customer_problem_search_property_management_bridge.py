from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "resources" / "customer-problem-search" / "index.html"
PROPERTY_ASSET = ROOT / "resources" / "property-management-maintenance-request-follow-up-checklist" / "index.html"
REL = "/resources/property-management-maintenance-request-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL


def test_customer_problem_search_map_links_property_management_asset():
    source = MAP.read_text(encoding="utf-8")
    assert REL in source
    assert "Tenant maintenance requests are not followed up" in source
    assert "property management missed maintenance calls" in source
    assert "contractor SLA dashboard" in source
    assert URL in source


def test_property_management_asset_has_buyer_safe_conversion_and_discovery_routes():
    source = PROPERTY_ASSET.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert "/free-business-review/?package=property-management-maintenance-request-follow-up-checklist" in source
    assert "/resources/customer-problem-search/manual-work-wasting-staff-time/" in source
    for boundary in [
        "not a real customer case study",
        "not a testimonial",
        "not a ranking claim",
        "not proof of faster repairs",
        "revenue lift",
        "AI-accuracy claim",
    ]:
        assert boundary in source


def test_property_management_asset_is_discoverable_from_sitemap_and_llms():
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
