from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/uk-private-clinic-owner-evidence-decision-memo/"
CSV = RESOURCE + "uk-private-clinic-owner-evidence-decision-memo.csv"
SVG = RESOURCE + "uk-private-clinic-owner-evidence-map.svg"
COMPARISON = "/resources/uk-private-clinic-ai-receptionist-vs-practice-management-patient-growthos-comparison/"
PACKAGE = "uk-private-clinic-owner-evidence-decision-memo"


def test_pricing_surfaces_uk_private_clinic_fixed_scope_bridge_without_fake_proof():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert 'data-revenue-bridge="uk-private-clinic-owner-evidence-decision-memo"' in section
    assert "UK private clinic AI receptionist evidence decision diagnostic bridge" in section
    assert "Scope before AI receptionist, practice-management, patient-engagement, call-centre or agency spend" in section
    assert RESOURCE in section
    assert CSV in section
    assert SVG in section
    assert f"/free-business-review/?package={PACKAGE}&amp;source=pricing-fixed-scope" in section
    for boundary in [
        "no patient data",
        "call recordings",
        "PMS/EMR exports",
        "GDPR/CQC/DTAC/DSPT proof",
        "appointment growth",
        "ranking",
        "revenue",
        "savings",
        "ROI claim",
    ]:
        assert boundary in section


def test_free_review_routes_uk_private_clinics_to_owner_evidence_assets():
    assert FREE_REVIEW.read_text(encoding="utf-8") == FREE_REVIEW_FLAT.read_text(encoding="utf-8")
    for path in (FREE_REVIEW, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert 'data-review-route="uk-private-clinic-owner-evidence-decision-memo"' in workflow
        assert "UK private clinics" in workflow
        assert "AI receptionist evidence decision review" in workflow
        assert "See the no-patient-data UK clinic decision memo" in workflow
        assert "View demo owner evidence map" in workflow
        assert RESOURCE in workflow
        assert SVG in workflow
        assert COMPARISON in workflow