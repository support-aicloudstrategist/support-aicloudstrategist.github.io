from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "simulated-india-diabetology-hba1c-footcare-followup-dpdp-diagnostic"
PAGE = ROOT / "case-studies" / SLUG / "index.html"
HUB = ROOT / "case-studies" / "index.html"
URL = f"https://aicloudstrategist.com/case-studies/{SLUG}/"


def test_diabetology_case_study_page_has_truth_boundaries_and_metrics():
    html = PAGE.read_text(encoding="utf-8")
    assert "Simulated India diabetology HbA1c + foot-care follow-up DPDP diagnostic" in html
    assert "no real diabetology clinic" in html
    assert "no real doctor" in html
    assert "no real patient" in html
    assert "no PHI" in html
    assert "no DPDP compliance claim" in html
    assert "no HbA1c outcome claim" in html
    assert "no wound-care outcome claim" in html
    assert "no revenue or ROI claim" in html
    assert "Synthetic rows" in html
    assert "Monthly items represented" in html
    assert "HbA1c logging coverage" in html
    assert "Foot-care logging coverage" in html
    assert "Human-review rows" in html
    assert "rows=12, synthetic_monthly_items=1754, callback_coverage_pct=34.6" in html
    assert "consent_not_ready_rows=10, owner_gap_rows=3, stale_24h_rows=6" in html
    assert URL in html


def test_diabetology_case_study_is_discoverable_from_proof_hub_but_not_sitemap():
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


def test_diabetology_case_study_internal_links_exist():
    html = PAGE.read_text(encoding="utf-8")
    for href in ["/case-studies/", "/healthcare-growthos/", "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/"]:
        assert href in html
        target = ROOT / href.strip("/") / "index.html"
        assert target.exists(), href
