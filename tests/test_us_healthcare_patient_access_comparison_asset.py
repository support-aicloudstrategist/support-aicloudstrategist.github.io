from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthcare-patient-access-vs-ai-receptionist-rcm-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-healthcare-patient-access-comparison-matrix.csv"
SVG = ROOT / "resources" / SLUG / "us-healthcare-patient-access-comparison-map.svg"


def test_us_healthcare_comparison_asset_has_top5_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "Patient access, AI receptionist, RCM/prior-auth, GRC or FinOps" in html
    assert "Top-5 buyer decision criteria" in html
    assert "no real medical group" in html
    assert "no-PHI fit check" in html
    assert "/pricing.html#fixed-scope-diagnostics" in html
    assert "No outreach was sent" in html


def test_us_healthcare_comparison_downloadables_and_discovery_routes_are_wired():
    html = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")

    assert CSV.exists()
    assert SVG.exists()
    assert "Synthetic no-PHI readiness row" in CSV.read_text(encoding="utf-8")
    assert "Demo-labelled, no-PHI owner-evidence lens" in SVG.read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/us-healthcare-patient-access-comparison-matrix.csv" in html
    assert f"/resources/{SLUG}/us-healthcare-patient-access-comparison-map.svg" in html
    assert f"/resources/{SLUG}/" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
