from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-multispecialty-clinic-referral-tpa-followup-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_multispecialty_referral_tpa_proof_asset_has_boundaries_metrics_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India multispecialty-clinic referral + TPA follow-up DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real clinic, no real patient, no PHI" in html
    assert "no customer data, no production export" in html
    assert "no DPDP compliance claim" in html
    assert "no referral conversion outcome, no TPA approval outcome, no appointment growth, no ranking, no revenue and no ROI promise" in html
    assert "total_enquiries=1843" in html
    assert "callback_coverage_pct=29.7" in html
    assert "specialist_confirmation_pct=52.5" in html
    assert "tpa_followup_logging_pct=30.2" in html
    assert "owner_gap_enquiries=1139" in html
    assert "8b324ecd367c79b660f92e66549fb08d06fa40c95f41512da0e647bef73cf9bc" in html
    assert "73d3223c236a78ef6532d4af341dc446c877bf2d15bb1379ad2314e37d606691" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=multispecialty-referral-tpa-followup-dpdp-diagnostic"' in html


def test_multispecialty_referral_tpa_proof_asset_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_multispecialty_referral_tpa_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-multispecialty-clinic-referral-tpa-followup-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India multispecialty-clinic referral and TPA follow-up DPDP evidence diagnostic" in hub
    assert "<strong>48</strong>" in hub
    assert "<em>23 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
