from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-radiology-centre-report-access-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_radiology_proof_asset_has_boundaries_metrics_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India radiology centre report access + DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real radiology centre, no real imaging centre, no real hospital, no real doctor, no patient, no PHI" in html
    assert "no DPDP compliance claim" in html
    assert "no report turnaround improvement outcome, no ranking, no revenue and no ROI promise" in html
    assert "total_requests=4423" in html
    assert "callback_coverage_pct=25.1" in html
    assert "on_time_report_access_pct=66.6" in html
    assert "critical_escalation_coverage_pct=40.1" in html
    assert "8b7b6c8a44a588b1fd4bed99b1b93c6469c6a6fa7d0ec026b99aee6deb646a36" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=radiology-report-access-dpdp-diagnostic"' in html


def test_radiology_proof_asset_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_radiology_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-radiology-centre-report-access-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India radiology report-access and DPDP evidence diagnostic" in hub
    assert "<strong>40</strong>" in hub
    assert "<em>15 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
