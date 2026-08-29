from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "simulated-india-nephrology-dialysis-followup-dpdp-diagnostic"
PAGE = ROOT / "case-studies" / SLUG / "index.html"
HUB = ROOT / "case-studies" / "index.html"
URL = f"https://aicloudstrategist.com/case-studies/{SLUG}/"


def test_nephrology_dialysis_case_study_page_has_truth_boundaries_and_metrics():
    html = PAGE.read_text(encoding="utf-8")
    assert "Simulated India nephrology / dialysis follow-up DPDP diagnostic" in html
    assert "no real nephrology clinic" in html
    assert "no real dialysis unit" in html
    assert "no real doctor" in html
    assert "no real nurse" in html
    assert "no real patient" in html
    assert "no caregiver" in html
    assert "no PHI" in html
    assert "no DPDP compliance claim" in html
    assert "no patient outcome claim" in html
    assert "no dialysis adherence claim" in html
    assert "no revenue or ROI claim" in html
    assert "Synthetic rows" in html
    assert "Monthly items represented" in html
    assert "Dialysis confirmation logging" in html
    assert "Lab/report follow-up logging" in html
    assert "Human-review rows" in html
    assert "rows=12, synthetic_monthly_items=1558, callback_coverage_pct=25.6" in html
    assert "consent_not_ready_rows=10, owner_gap_rows=8, stale_24h_rows=9" in html
    assert "payment_or_tpa_blocker_rows=1, closure_gap_rows=10" in html
    assert "f7676accdd5c8b8f351f0eeda29b40b8740eb3b9f8bf2850a49fc21760a71de8" in html
    assert URL in html


def test_nephrology_dialysis_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)
    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_nephrology_dialysis_case_study_is_discoverable_from_proof_hub_but_not_sitemap():
    hub = HUB.read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f"/case-studies/{SLUG}/" in hub
    assert "India nephrology and dialysis follow-up DPDP evidence diagnostic" in hub
    assert "50</strong><span>existing child routes retained here" in hub
    assert "25 methods" in hub
    assert URL in llms
    assert URL not in sitemap


def test_nephrology_dialysis_case_study_internal_links_exist():
    html = PAGE.read_text(encoding="utf-8")
    for href in ["/case-studies/", "/healthcare-growthos/", "/resources/india-clinic-lab-dpdp-whatsapp-followup-evidence-checklist/"]:
        assert href in html
        target = ROOT / href.strip("/") / "index.html"
        assert target.exists(), href
