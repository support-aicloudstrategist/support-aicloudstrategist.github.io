from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-dental-treatment-plan-followup-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_dental_treatment_plan_proof_asset_has_boundaries_metrics_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India dental treatment-plan follow-up + DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real dental clinic, no real dentist, no real patient, no PHI, no personal data" in html
    assert "no DPDP compliance claim" in html
    assert "no treatment outcome, no appointment growth, no ranking, no revenue and no ROI promise" in html
    assert "total_enquiries=1662" in html
    assert "callback_coverage_pct=35.1" in html
    assert "treatment_plan_followup_logging_pct=20.2" in html
    assert "price_objection_callback_logging_pct=27.1" in html
    assert "a7039e9e432f8276b5112d23c94881c84270c99df7eea9d6db54804daf3abf8e" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=dental-treatment-plan-followup-dpdp-diagnostic"' in html


def test_dental_treatment_plan_proof_asset_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_dental_treatment_plan_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-dental-treatment-plan-followup-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India dental treatment-plan follow-up and DPDP evidence diagnostic" in hub
    assert "<strong>44</strong>" in hub
    assert "<em>19 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
