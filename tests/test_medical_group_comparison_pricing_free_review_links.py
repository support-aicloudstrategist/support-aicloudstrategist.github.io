from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW_INDEX = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"

COMPARISON_HREF = "/resources/us-medical-group-referral-prior-auth-vs-patient-engagement-rcm-ai-receptionist-comparison/"
HANDOFF_HREF = "/resources/us-medical-group-referral-prior-auth-owner-handoff-faq/"


def test_pricing_medical_group_bridge_links_to_comparison_and_handoff_route():
    html = PRICING.read_text(encoding="utf-8")

    assert 'data-revenue-bridge="us-medical-group-referral-prior-auth-owner-handoff"' in html
    assert HANDOFF_HREF in html
    assert COMPARISON_HREF in html
    assert "Compare patient engagement, RCM and AI receptionist routes" in html
    assert "Request free medical-group handoff review" in html


def test_free_review_medical_group_route_links_to_comparison_in_both_entrypoints():
    for path in (FREE_REVIEW_INDEX, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        assert "Referral + prior-auth owner-handoff review" in html
        assert HANDOFF_HREF in html
        assert COMPARISON_HREF in html
        assert "Compare buyer routes" in html
