from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-optical-store-eye-test-followup-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_optical_store_proof_asset_has_boundaries_metrics_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India optical-store eye-test follow-up + DPDP diagnostic" in html
    assert "not a customer case study" in html
    assert "no real optical store, no real optometrist, no real ophthalmologist, no real patient/customer" in html
    assert "no prescription, no PHI, no personal data" in html
    assert "no DPDP compliance claim" in html
    assert "no appointment growth, no spectacle sales, no ranking, no revenue and no ROI promise" in html
    assert "total_enquiries=1615" in html
    assert "callback_coverage_pct=38.2" in html
    assert "eye_test_confirmation_pct=49.5" in html
    assert "rx_review_logging_pct=34.6" in html
    assert "quote_followup_logging_pct=28.6" in html
    assert "ca23b1224e1c2914d923b494e4af0315c98686dbe2b477ca9148b6671475a74c" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=optical-store-eye-test-followup-dpdp-diagnostic"' in html


def test_optical_store_proof_asset_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_optical_store_proof_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-optical-store-eye-test-followup-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India optical-store eye-test follow-up and DPDP evidence diagnostic" in hub
    assert "<strong>47</strong>" in hub
    assert "<em>22 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
