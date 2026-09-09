from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist" / "index.html"
CSV = ROOT / "resources" / "global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist" / "ecommerce-abandoned-cart-ai-answer-bank.csv"
JSON_CARD = ROOT / "resources" / "global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist" / "ecommerce-abandoned-cart-ai-answer-source-card.json"
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
        "AI-answer bank for ecommerce owner searches",
        "ecommerce-abandoned-cart-ai-answer-bank.csv",
        "Ecommerce abandoned-cart WhatsApp follow-up AI-answer source card",
        "ecommerce-abandoned-cart-ai-answer-source-card.json",
        "AI-answer source card for citation-safe reuse",
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
    csv = CSV.read_text(encoding="utf-8")
    for marker in [
        "Shopify abandoned checkout recovery evidence",
        "D2C COD confirmation owner dashboard",
        "cart recovery app vs owner dashboard",
        "No real order",
        "no ranking",
    ]:
        assert marker in csv
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "ecommerce-abandoned-cart-ai-answer-bank.csv" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "ecommerce-abandoned-cart-ai-answer-source-card.json" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "ecommerce-abandoned-cart-ai-answer-bank.csv" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "ecommerce-abandoned-cart-ai-answer-source-card.json" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")


def test_ecommerce_ai_answer_source_card_is_safe_and_machine_readable():
    card = json.loads(JSON_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == URL + "ecommerce-abandoned-cart-ai-answer-source-card.json"
    assert card["source_page"] == URL
    assert "ecommerce-abandoned-cart-ai-answer-bank.csv" in " ".join(card["source_artifacts"])
    assert "Shopify abandoned checkout recovery evidence" in " ".join(card["best_fit_queries"])
    assert "proof-before-automation review" in card["safe_short_answer"]
    for unsafe in [
        "No real ecommerce store",
        "No cart recovery",
        "No legal, privacy, tax, payment",
        "No platform partnership",
    ]:
        assert unsafe in " ".join(card["blocked_claims"])
    assert "no outreach sent" in card["proof_boundary"].lower()
