from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-ent-clinic-surgery-counselling-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_ent_proof_asset_has_claim_boundaries_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India ENT clinic surgery-counselling + DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real clinic, patient, PHI" in html
    assert "no appointment, no surgery, no advertising, no ranking, no revenue and no ROI promise" in html
    assert "total_enquiries=1610" in html
    assert "callback_coverage_pct=30.7" in html
    assert "counselling_completion_pct=39.6" in html
    assert "0ea1d81c3dd515b7b9b7fe3ee836e659fe3bb55077a4bfca811ca725f7fc99ff" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=ent-surgery-counselling-dpdp-diagnostic"' in html


def test_ent_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-ent-clinic-surgery-counselling-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India ENT surgery-counselling and DPDP evidence diagnostic" in hub
    assert "<strong>42</strong>" in hub
    assert "<em>17 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
