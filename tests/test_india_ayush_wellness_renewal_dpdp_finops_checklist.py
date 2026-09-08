from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-ayush-wellness-package-renewal-dpdp-finops-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "india-ayush-wellness-package-renewal-synthetic.csv"
HUB = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_ayush_wellness_renewal_page_is_claim_safe_and_commercial():
    html = PAGE.read_text(encoding="utf-8")
    assert "India AYUSH Wellness Renewal DPDP + FinOps Checklist" in html
    assert "Stop automating wellness renewals" in html
    assert "simulated proof-of-method" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert "Request no-credentials review" in html
    assert "FAQPage" in html
    assert "Dataset" in html
    assert "INR 587" in html
    assert "appointment-growth proof" in html


def test_ayush_wellness_renewal_synthetic_csv_is_linked():
    csv = CSV.read_text(encoding="utf-8")
    assert "workflow_id,lead_source,package_type" in csv
    assert "AYUSH-001" in csv
    assert "AYUSH-012" in csv
    assert csv.count("\n") == 13
    html = PAGE.read_text(encoding="utf-8")
    assert "india-ayush-wellness-package-renewal-synthetic.csv" in html


def test_ayush_wellness_renewal_asset_is_discoverable():
    route = f"/resources/{SLUG}/"
    url = f"https://aicloudstrategist.com{route}"
    assert route in HUB.read_text(encoding="utf-8")
    assert "Download synthetic renewal workflow CSV" in HUB.read_text(encoding="utf-8")
    assert url in LLMS.read_text(encoding="utf-8")
    assert f'"{route}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert url in SITEMAP.read_text(encoding="utf-8")
