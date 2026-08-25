from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-home-health-elder-care-referral-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_home_health_proof_asset_has_boundaries_metrics_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India home-health referral + DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real home-health agency, no real elder-care provider, no real caregiver, no real nurse, no real attendant, no real doctor, no real discharge planner, no real patient, no real family member, no PHI" in html
    assert "no DPDP compliance claim" in html
    assert "no clinical outcome, no caregiver-placement outcome, no ranking, no revenue and no ROI promise" in html
    assert "total_referrals=1243" in html
    assert "callback_coverage_pct=38.3" in html
    assert "assessment_schedule_rate_pct=45.0" in html
    assert "caregiver_match_pending=267" in html
    assert "95946ac02729fcdbc9f41a84989cc9a194e1edc32288e94d2a1a0635f7a837a8" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=home-health-elder-care-referral-dpdp-diagnostic"' in html


def test_home_health_proof_asset_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_home_health_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-home-health-elder-care-referral-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India home-health referral and DPDP evidence diagnostic" in hub
    assert "<strong>44</strong>" in hub
    assert "<em>19 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
