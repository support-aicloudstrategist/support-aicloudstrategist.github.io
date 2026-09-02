from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "small-business-owner-ai-automation-readiness"
RESOURCE = "/resources/small-business-owner-ai-automation-readiness-checklist/"
CSV = "/resources/small-business-owner-ai-automation-readiness-checklist/small-business-ai-automation-readiness-owner-register.csv"
DASHBOARD = "/resources/small-business-owner-ai-automation-readiness-checklist/small-business-ai-automation-owner-dashboard.svg"


def test_small_business_ai_automation_assets_are_linked_and_claim_safe():
    page = (ROOT / "resources" / "small-business-owner-ai-automation-readiness-checklist" / "index.html").read_text(
        encoding="utf-8"
    )
    csv = ROOT / "resources" / "small-business-owner-ai-automation-readiness-checklist" / "small-business-ai-automation-readiness-owner-register.csv"
    svg = ROOT / "resources" / "small-business-owner-ai-automation-readiness-checklist" / "small-business-ai-automation-owner-dashboard.svg"

    assert csv.exists()
    assert svg.exists()
    assert "Download the synthetic owner register CSV" in page
    assert "Open demo owner dashboard SVG" in page
    assert "No real client, customer data, lead, WhatsApp chat, call log, CRM export" in page
    assert "Synthetic row only" in csv.read_text(encoding="utf-8")
    assert "DEMO / SYNTHETIC ONLY" in svg.read_text(encoding="utf-8")


def test_pricing_surfaces_small_business_ai_automation_readiness_bridge():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert f'data-revenue-bridge="{SLUG}"' in section
    assert "Small business AI automation readiness diagnostic bridge" in section
    assert "Scope before CRM, chatbot or automation spend" in section
    assert RESOURCE in section
    assert CSV in section
    assert DASHBOARD in section
    assert f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope" in section
    assert "no customer data, WhatsApp chat, call log, CRM export" in section


def test_free_business_review_routes_small_business_automation_buyers_to_proof_asset():
    for relative in ["free-business-review/index.html", "free-business-review.html"]:
        html = (ROOT / relative).read_text(encoding="utf-8")
        assert f'data-review-route="{SLUG}"' in html
        assert "Small business owners / manual admin" in html
        assert "AI automation readiness + owner-register review" in html
        assert RESOURCE in html
        assert "synthetic owner register and dashboard demo" in html
        assert '<span class="fbr-flow-number">H</span>' in html


def test_free_business_review_entrypoints_stay_in_sync():
    assert (ROOT / "free-business-review.html").read_text(encoding="utf-8") == (
        ROOT / "free-business-review" / "index.html"
    ).read_text(encoding="utf-8")
