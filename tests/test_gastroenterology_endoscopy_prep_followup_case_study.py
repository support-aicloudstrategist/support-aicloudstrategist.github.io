from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "simulated-india-gastroenterology-endoscopy-prep-followup-dpdp-diagnostic"
PAGE = ROOT / "case-studies" / SLUG / "index.html"
HUB = ROOT / "case-studies" / "index.html"
URL = f"https://aicloudstrategist.com/case-studies/{SLUG}/"


def test_gastroenterology_case_study_page_has_truth_boundaries_and_metrics():
    html = PAGE.read_text(encoding="utf-8")
    assert "Simulated India gastroenterology endoscopy prep follow-up DPDP diagnostic" in html
    assert "no real clinic" in html
    assert "no real patient" in html
    assert "no PHI" in html
    assert "no DPDP compliance claim" in html
    assert "no revenue or ROI claim" in html
    assert "Synthetic rows" in html
    assert "Prep gaps" in html
    assert "Human review rows" in html
    assert "Admin-only automation candidates" in html
    assert "rows=12, consent_gaps=1, prep_ack_gaps=5, human_review_rows=5" in html
    assert URL in html


def test_gastroenterology_case_study_is_discoverable_from_proof_hub_but_not_sitemap():
    hub = HUB.read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f"/case-studies/{SLUG}/" in hub
    assert "76</strong> synthetic enquiry and follow-up rows" in hub
    assert "18 methods" in hub
    assert URL not in sitemap
