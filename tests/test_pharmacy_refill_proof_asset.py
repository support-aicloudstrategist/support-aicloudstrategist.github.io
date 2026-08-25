from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-pharmacy-prescription-refill-whatsapp-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_pharmacy_refill_proof_asset_has_claim_boundaries_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India pharmacy prescription refill + WhatsApp DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real pharmacy" in html
    assert "no patient" in html
    assert "no PHI" in html
    assert "no prescription data" in html
    assert "no medicine-delivery outcome" in html
    assert "no DPDP attestation" in html
    assert "no revenue, no ROI" in html
    assert "total_requests=1736" in html
    assert "callback_coverage_pct=33.9" in html
    assert "prescription_verification_logging_pct=36.5" in html
    assert "stockout_followup_logging_pct=28.0" in html
    assert "aa2405956e29acc761c421022154cf5385ad3172d2384d6cb61302a142e72130" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=pharmacy-prescription-refill-whatsapp-dpdp-diagnostic"' in html


def test_pharmacy_refill_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-pharmacy-prescription-refill-whatsapp-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India pharmacy prescription refill and WhatsApp DPDP evidence diagnostic" in hub
    assert "<strong>43</strong>" in hub
    assert "<em>18 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
