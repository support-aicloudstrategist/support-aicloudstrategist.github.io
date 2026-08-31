from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")
FREE_REVIEW = (ROOT / "free-business-review" / "index.html").read_text(encoding="utf-8")
FREE_REVIEW_FLAT = (ROOT / "free-business-review.html").read_text(encoding="utf-8")


def test_pricing_routes_whatsapp_lead_leakage_into_scoped_review():
    assert 'data-revenue-bridge="whatsapp-lead-follow-up-owner-evidence"' in PRICING
    assert "WhatsApp lead follow-up owner-evidence diagnostic bridge" in PRICING
    assert "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/" in PRICING
    assert "/free-business-review/?problem=whatsapp-lead-follow-up-owner-evidence&amp;source=pricing-fixed-scope" in PRICING
    assert "no customer, WhatsApp chat, call recording, CRM export, conversion-rate, booked-call, ranking, lead, revenue or ROI claim" in PRICING


def test_free_review_surfaces_whatsapp_lead_follow_up_as_specific_next_step():
    for html in (FREE_REVIEW, FREE_REVIEW_FLAT):
        assert "Small business / WhatsApp leads" in html
        assert "Lead follow-up owner-evidence diagnostic" in html
        assert "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/" in html

    assert FREE_REVIEW == FREE_REVIEW_FLAT