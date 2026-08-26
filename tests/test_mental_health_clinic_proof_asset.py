from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-mental-health-clinic-counselling-triage-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_mental_health_proof_asset_has_claim_boundaries_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India mental-health clinic counselling triage + DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real clinic" in html
    assert "no crisis intervention" in html
    assert "no counselling, no diagnosis" in html
    assert "no therapy outcome" in html
    assert "total_enquiries=1590" in html
    assert "callback_coverage_pct=47.3" in html
    assert "risk_triage_logging_pct=40.5" in html
    assert "68cab3dccd6afcc95ea191f19b1d0eba0998df1211b278e88baffd4fffd832c0" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=mental-health-counselling-triage-dpdp-diagnostic"' in html


def test_mental_health_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-mental-health-clinic-counselling-triage-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India mental-health counselling triage and DPDP evidence diagnostic" in hub
    assert "<strong>46</strong>" in hub
    assert "<em>21 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms