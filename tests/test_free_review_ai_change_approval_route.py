from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "ai-change-approval-readiness-diagnostic"
PUBLICATION = "/publications/2026-09-04/ai-change-approval-card.html"
CSV = "/publications/2026-09-04/ai-change-approval-card.csv"


def _free_review_sources():
    return [
        (ROOT / "free-business-review" / "index.html").read_text(encoding="utf-8"),
        (ROOT / "free-business-review.html").read_text(encoding="utf-8"),
    ]


def test_free_review_surfaces_ai_change_approval_route_on_both_public_paths():
    for html in _free_review_sources():
        assert f'data-review-route="{PACKAGE}"' in html
        assert "AI change approval readiness fit check" in html
        assert "human owner gates before AI changes touch customers, money, credentials, policy, data handling or live systems" in html
        assert PUBLICATION in html
        assert CSV in html
        assert "/pricing.html#fixed-scope-diagnostics" in html


def test_pricing_link_package_context_has_matching_free_review_route():
    pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
    assert f"/free-business-review/?package={PACKAGE}&amp;source=pricing-fixed-scope" in pricing
    for html in _free_review_sources():
        assert f'data-review-route="{PACKAGE}"' in html
