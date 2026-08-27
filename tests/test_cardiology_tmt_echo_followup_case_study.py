from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "simulated-india-cardiology-tmt-echo-followup-dpdp-diagnostic"
PAGE = ROOT / "case-studies" / SLUG / "index.html"
HUB = ROOT / "case-studies" / "index.html"
URL = f"https://aicloudstrategist.com/case-studies/{SLUG}/"


def test_cardiology_case_study_page_has_truth_boundaries_and_metrics():
    html = PAGE.read_text(encoding="utf-8")
    assert "Simulated India cardiology TMT/Echo follow-up DPDP diagnostic" in html
    assert "no real clinic" in html
    assert "no real cardiologist" in html
    assert "no real patient" in html
    assert "no PHI" in html
    assert "no DPDP compliance claim" in html
    assert "no revenue or ROI claim" in html
    assert "Synthetic rows" in html
    assert "Admin-safe candidates" in html
    assert "Clinical human-review rows" in html
    assert "Payment/TPA blockers" in html
    assert "rows=12, admin_safe_candidates=4, unsafe_for_automation=8, stale_24h_plus_rows=5" in html
    assert URL in html


def test_cardiology_case_study_is_discoverable_from_proof_hub_but_not_sitemap():
    hub = HUB.read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f"/case-studies/{SLUG}/" in hub
    assert "100</strong> synthetic enquiry and follow-up rows" in hub
    assert "20 methods" in hub
    assert "48</strong><span>existing child routes retained here" in hub
    assert "23 methods" in hub
    assert URL in llms
    assert URL not in sitemap
