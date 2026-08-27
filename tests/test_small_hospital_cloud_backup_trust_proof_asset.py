from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-studies" / "simulated-india-small-hospital-cloud-backup-trust-dpdp-diagnostic" / "index.html"
HUB = ROOT / "case-studies" / "index.html"
LLMS = ROOT / "llms.txt"


def test_small_hospital_cloud_backup_asset_has_boundaries_metrics_and_reproducibility():
    html = PAGE.read_text(encoding="utf-8")

    assert "Simulated India small-hospital cloud backup + DPDP trust diagnostic" in html
    assert "not a customer case study" in html
    assert "no real hospital, no real patient, no PHI" in html
    assert "no DPDP compliance claim" in html
    assert "no backup success, no restore success, no breach prevention" in html
    assert "no cloud savings, no ranking, no revenue and no ROI promise" in html
    assert "total_records=54885" in html
    assert "patient_records=54365" in html
    assert "backup_gap_records=21265" in html
    assert "stale_restore_records=47585" in html
    assert "public_link_risk_records=28665" in html
    assert "high_attention_rows=7" in html
    assert "2124b7ac8b1271d8afd70048d3ecf8db94b767f9572086a0f40387482750fa97" in html
    assert 'href="/contact.html?service=business-growth-systems&proof=small-hospital-cloud-backup-trust-dpdp-diagnostic"' in html


def test_small_hospital_cloud_backup_asset_structured_data_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert len(blocks) == 3
    parsed = [json.loads(block) for block in blocks]
    assert parsed[0]["@type"] == "Article"
    assert parsed[1]["@type"] == "FAQPage"
    assert parsed[2]["@type"] == "BreadcrumbList"


def test_small_hospital_cloud_backup_asset_is_linked_from_evidence_hub_and_llms():
    route = "/case-studies/simulated-india-small-hospital-cloud-backup-trust-dpdp-diagnostic/"
    hub = HUB.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert route in hub
    assert "India small-hospital cloud backup and DPDP trust evidence diagnostic" in hub
    assert "<strong>47</strong>" in hub
    assert "<em>22 methods</em>" in hub
    assert f"https://aicloudstrategist.com{route}" in llms
