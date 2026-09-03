from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/saas-security-questionnaire-takes-too-long-ai-evidence-checklist/"
CSV = "/resources/saas-security-questionnaire-takes-too-long-ai-evidence-checklist/saas-security-questionnaire-owner-evidence.csv"
PROBLEM = "saas-security-questionnaire-takes-too-long"


def test_pricing_routes_saas_questionnaire_delay_buyers_to_diagnostic_fit_check():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert 'data-revenue-bridge="saas-security-questionnaire-takes-too-long"' in section
    assert "B2B SaaS security-questionnaire answer ownership diagnostic bridge" in section
    assert "Scope before questionnaire automation, GRC/trust-centre tooling" in section
    assert RESOURCE in section
    assert CSV in section
    assert f"/free-business-review/?problem={PROBLEM}&amp;source=pricing-fixed-scope" in section
    assert "no customer data, contracts, security reports" in section
    assert "ranking, revenue, savings, sales-cycle, ROI or outcome claim" in section


def test_free_review_routes_saas_questionnaire_delay_to_owner_evidence_on_both_entrypoints():
    for path in (FREE_REVIEW, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert 'data-review-route="saas-security-questionnaire-takes-too-long"' in workflow
        assert "B2B SaaS sales / security / RevOps" in workflow
        assert "Security-questionnaire answer ownership review" in workflow
        assert "no-customer-data SaaS evidence checklist" in workflow
        assert RESOURCE in workflow
        assert CSV in workflow


def test_free_review_flat_file_stays_identical_to_directory_version_for_saas_route():
    assert FREE_REVIEW.read_text(encoding="utf-8") == FREE_REVIEW_FLAT.read_text(encoding="utf-8")
