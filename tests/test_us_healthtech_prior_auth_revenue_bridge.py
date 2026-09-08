from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/us-healthtech-prior-auth-denial-ai-human-review-checklist/"
SOURCE_MAP = RESOURCE + "us-prior-auth-automation-source-map.csv"
ANSWER_BANK = RESOURCE + "prior-auth-trust-answer-bank.csv"
PROBLEM = "us-healthtech-prior-auth-denial-human-review"


def test_pricing_has_us_prior_auth_denial_human_review_bridge():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert 'data-revenue-bridge="us-healthtech-prior-auth-denial-human-review"' in section
    assert "US healthtech prior-auth denial human-review diagnostic bridge" in section
    assert "Scope before prior-authorization automation, AI appeal drafting, RCM workqueue cleanup" in section
    assert "HIPAA trust-centre tooling or cloud/LLM FinOps spend" in section
    assert "prior authorization delay" in section
    assert "denial follow-up" in section
    assert "claim-denial owner queues" in section
    assert "BAA/subprocessor AI data-use questions" in section
    assert RESOURCE in section
    assert SOURCE_MAP in section
    assert ANSWER_BANK in section
    assert f"/free-business-review/?problem={PROBLEM}&amp;source=pricing-fixed-scope" in section
    assert "no real medical group, clinic, hospital, healthtech customer, patient, payer, PHI/ePHI" in section
    assert "no real" in section
    assert "HIPAA/SOC2/HITRUST/BAA compliance proof" in section
    assert "authorization-speed, denial-reduction, recovered-revenue, savings, ROI or AI-accuracy claim" in section
    assert "trusted by" not in section.lower()
    assert "increased revenue" not in section.lower()


def test_free_review_routes_us_prior_auth_buyers_to_no_phi_assets_and_flat_copy_synced():
    html = FREE_REVIEW.read_text(encoding="utf-8")
    flat = FREE_REVIEW_FLAT.read_text(encoding="utf-8")
    assert html == flat
    workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
    assert 'data-review-route="us-healthtech-prior-auth-denial-human-review"' in workflow
    assert "US healthtech / medical group prior-auth teams" in workflow
    assert "Prior-auth denial human-review fit check" in workflow
    assert "AI appeal drafting boundaries" in workflow
    assert "HIPAA vendor-risk sources" in workflow
    assert "cloud/LLM FinOps owner evidence" in workflow
    assert "See the no-PHI prior-auth checklist" in workflow
    assert SOURCE_MAP in workflow
    assert ANSWER_BANK in workflow
