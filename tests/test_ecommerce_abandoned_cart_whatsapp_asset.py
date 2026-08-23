from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist" / "index.html"
REL = "/resources/global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_ecommerce_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "ecommerce abandoned cart WhatsApp follow up checklist",
        "D2C COD confirmation owner dashboard",
        "Shopify abandoned checkout recovery evidence",
        "WhatsApp opt-in",
        "COD confirmation queue",
        "Truth boundary",
    ]:
        assert marker in source


def test_ecommerce_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "No real ecommerce store",
        "customer",
        "payment record",
        "testimonial",
        "revenue, ROI",
        "AI-accuracy claim",
        "no legal, privacy, tax, payment, advertising, marketplace-policy, product-safety or consumer-protection advice",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=ecommerce-abandoned-cart-whatsapp-evidence" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_ecommerce_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
