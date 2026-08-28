from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-review-vs-finops-grc-tools-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def _page() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_page_is_indexable_and_structured():
    html = _page()
    assert '<meta name="robots" content="index, follow"' in html
    assert f'<link rel="canonical" href="{URL}"' in html
    assert "Europe Healthtech Cloud Trust Review vs FinOps, GRC and Patient Platforms" in html
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    parsed = [json.loads(block) for block in blocks]
    types = {item["@type"] for item in parsed}
    assert {"Article", "FAQPage"}.issubset(types)


def test_comparison_covers_market_context_and_aics_gap():
    html = _page()
    for marker in [
        "Apptio Cloudability",
        "VMware CloudHealth",
        "OneTrust",
        "Vanta",
        "Drata",
        "Doctolib",
        "Accurx",
        "GDPR/DPIA",
        "EU AI Act",
        "human-review",
        "no-credentials first review",
    ]:
        assert marker in html


def test_truth_boundary_blocks_unsupported_claims():
    html = _page()
    for marker in [
        "not a vendor ranking",
        "not a real client case study",
        "not a platform partnership",
        "does not claim superiority",
        "No legal, privacy, security, clinical, audit or procurement decisions",
    ]:
        assert marker in html
    forbidden = ["guaranteed savings", "certified GDPR compliant", "ranked #1", "our client"]
    lowered = html.lower()
    for phrase in forbidden:
        assert phrase not in lowered


def test_downloadable_csv_has_expected_rows():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    assert len(rows) == 5
    assert {row["competitor_category"] for row in rows} >= {
        "FinOps platforms",
        "GRC trust-centre and questionnaire automation",
        "Patient engagement and practice platforms",
    }
    assert all(row["unsafe_claim_boundary"].startswith("No claim") for row in rows[:4])


def test_discovery_wiring():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    sitemap_builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8") if (ROOT / "sitemap.xml").exists() else ""
    assert f'/resources/{SLUG}/' in resources
    assert f'"/resources/{SLUG}/"' in sitemap_builder
    assert URL in llms
    if sitemap:
        assert URL in sitemap
