from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"

RESOURCE = "/resources/us-medical-group-referral-prior-auth-owner-handoff-faq/"
PROBLEM = "us-medical-group-referral-prior-auth-owner-handoff"


def test_pricing_adds_medical_group_handoff_bridge_without_expanding_fixed_offer_grid():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert 'data-revenue-bridge="us-medical-group-referral-prior-auth-owner-handoff"' in section
    assert "US medical group referral + prior-auth owner-handoff diagnostic bridge" in section
    assert RESOURCE in section
    assert f"/free-business-review/?problem={PROBLEM}&amp;source=pricing-fixed-scope" in section
    assert "synthetic no-PHI owner-handoff FAQ" in section
    assert "no PHI/ePHI, payer files, claims data, EHR/PMS access" in section
    assert "no PHI/ePHI" in section
    assert len(section.split('<div class="grid-3">', 1)[1].split('<article class="card"><h3>')) == 21


def test_free_review_workflow_routes_us_medical_groups_to_no_phi_handoff_asset():
    for path in (FREE_REVIEW, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert "US medical groups" in workflow
        assert "Referral + prior-auth owner-handoff review" in workflow
        assert "See the no-PHI handoff FAQ" in workflow
        assert RESOURCE in workflow
        assert 'fbr-flow-number">B<' in workflow
        assert 'fbr-flow-number">E<' in workflow
