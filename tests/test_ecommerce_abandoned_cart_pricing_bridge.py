from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_FILES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
PACKAGE = "ecommerce-abandoned-cart-whatsapp-evidence"
RESOURCE = "/resources/global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist/"
CSV = RESOURCE + "ecommerce-abandoned-cart-ai-answer-bank.csv"


def _fixed_scope_section(html: str) -> str:
    return html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split('<section class="section"><div class="container faq">', 1)[0]


def test_ecommerce_abandoned_cart_has_visible_pricing_bridge_on_both_pricing_routes():
    for path in PRICING_FILES:
        section = _fixed_scope_section(path.read_text(encoding="utf-8"))
        assert 'data-revenue-bridge="ecommerce-abandoned-cart-whatsapp-evidence"' in section
        assert "Ecommerce abandoned-cart WhatsApp follow-up diagnostic bridge" in section
        assert "Scope before cart-recovery apps, WhatsApp BSPs, email/SMS automation" in section
        assert RESOURCE in section
        assert CSV in section
        assert f"/free-business-review/?package={PACKAGE}&amp;source=pricing-fixed-scope" in section


def test_ecommerce_abandoned_cart_pricing_bridge_keeps_claim_boundaries():
    section = _fixed_scope_section((ROOT / "pricing.html").read_text(encoding="utf-8"))
    card = section.split('data-revenue-bridge="ecommerce-abandoned-cart-whatsapp-evidence"', 1)[1].split("</aside>", 1)[0]
    for boundary in [
        "no real store",
        "customer",
        "order",
        "payment record",
        "WhatsApp chat",
        "platform partnership",
        "ranking",
        "cart recovery",
        "conversion",
        "revenue, savings, ROI",
        "AI-accuracy claim",
    ]:
        assert boundary in card
