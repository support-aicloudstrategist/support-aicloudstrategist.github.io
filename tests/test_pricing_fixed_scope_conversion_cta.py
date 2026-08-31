from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


def test_fixed_scope_pricing_has_direct_scoping_cta_before_offer_grid():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('id="fixed-scope-diagnostics"', 1)[1].split('<section class="section pricing-showcase"', 1)[0]
    cta = '/contact.html?service=fixed-scope-diagnostic&stage=scoping&source=pricing-fixed-scope'
    assert cta in section
    assert section.index(cta) < section.index('<div class="grid-3">')
    assert "scope, access boundaries and a written proposal before spend" in section
    assert "Request a fixed-scope diagnostic" in section
