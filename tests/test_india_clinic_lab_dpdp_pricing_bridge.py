from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_FLAT = ROOT / "free-business-review.html"
RESOURCE = "/resources/india-clinic-lab-dpdp-whatsapp-followup-evidence-checklist/"
CSV = RESOURCE + "india-clinic-lab-dpdp-whatsapp-followup-evidence-checklist.csv"
SVG = RESOURCE + "demo-owner-evidence-room.svg"
PACKAGE = "india-clinic-lab-dpdp-whatsapp-followup"


def test_pricing_surfaces_india_clinic_lab_dpdp_fixed_scope_bridge_without_fake_proof():
    html = PRICING.read_text(encoding="utf-8")
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section pricing-showcase">', 1
    )[0]

    assert 'data-revenue-bridge="india-clinic-lab-dpdp-whatsapp-followup"' in section
    assert "India clinic/lab DPDP-aware WhatsApp follow-up diagnostic bridge" in section
    assert "Scope before clinic software, WhatsApp automation, AI receptionist or new ads" in section
    assert RESOURCE in section
    assert CSV in section
    assert SVG in section
    assert f"/free-business-review/?package={PACKAGE}&amp;source=pricing-fixed-scope" in section
    for forbidden_or_boundary in [
        "no patient data",
        "DPDP compliance proof",
        "appointment growth",
        "ranking",
        "revenue",
        "savings",
        "ROI claim",
    ]:
        assert forbidden_or_boundary in section
    # The fixed list still has twenty grid cards; this India route is a revenue bridge above the grid.
    assert len(section.split('<div class="grid-3">', 1)[1].split('<article class="card"><h3>')) == 21


def test_free_review_routes_india_clinic_labs_to_dpdp_owner_evidence_assets():
    for path in (FREE_REVIEW, FREE_REVIEW_FLAT):
        html = path.read_text(encoding="utf-8")
        assert FREE_REVIEW.read_text(encoding="utf-8") == FREE_REVIEW_FLAT.read_text(encoding="utf-8")
        workflow = html.split('id="diagnostic-bridge-title"', 1)[1].split('id="request-title"', 1)[0]
        assert 'data-review-route="india-clinic-lab-dpdp-whatsapp-followup"' in workflow
        assert "India clinics / diagnostic labs" in workflow
        assert "DPDP-aware WhatsApp follow-up + report-pickup review" in workflow
        assert "See the no-patient-data clinic/lab checklist" in workflow
        assert "View demo owner evidence room" in workflow
        assert RESOURCE in workflow
        assert SVG in workflow
        assert "/resources/india-clinic-ad-to-appointment-diagnostic-package/" in workflow
