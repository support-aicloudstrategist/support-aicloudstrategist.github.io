from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-veterinary-clinic-vaccination-followup-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_veterinary_vaccination_proof_asset_has_boundaries_metrics_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India veterinary-clinic vaccination follow-up + DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real veterinary clinic, no real pet owner, no real animal patient" in html
    assert "no customer data, no production export" in html
    assert "no DPDP compliance claim" in html
    assert "no vaccination outcome, no appointment growth, no ranking, no revenue and no ROI promise" in html
    assert "total_enquiries=1696" in html
    assert "callback_coverage_pct=32.7" in html
    assert "vaccination_confirmation_pct=40.0" in html
    assert "appointment_confirmation_pct=51.7" in html
    assert "surgery_followup_logging_pct=35.6" in html
    assert "4c5f00aea06bcb2ba8e4a82ad14a17c5fa904f46b9b404aaf022ff0c1195768c" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=veterinary-clinic-vaccination-followup-dpdp-diagnostic"' in html


def test_veterinary_vaccination_proof_asset_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_veterinary_vaccination_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-veterinary-clinic-vaccination-followup-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India veterinary-clinic vaccination follow-up and DPDP evidence diagnostic" in hub
    assert "<strong>45</strong>" in hub
    assert "<em>20 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
