import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-ophthalmology-cataract-retina-followup-dpdp-finops-checklist"
PATH = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com{PATH}"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_PATH = PAGE.parent / "india-ophthalmology-cataract-retina-followup-synthetic.csv"
CSV_URL = f"{URL}india-ophthalmology-cataract-retina-followup-synthetic.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_ophthalmology_page_is_indexable_and_safely_positioned():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    for phrase in [
        "Truth boundary",
        "simulated proof-of-method",
        "not a real customer case study",
        "No real eye hospital",
        "Ophthalmologist review",
        "Red-flag/emergency-language rows",
        "Request no-credentials review",
    ]:
        assert phrase in html


def test_ophthalmology_dataset_schema_matches_public_csv():
    html = PAGE.read_text(encoding="utf-8")
    datasets = [doc for doc in json_ld_documents(html) if doc.get("@type") == "Dataset"]
    dataset = next(doc for doc in datasets if doc.get("url") == CSV_URL)
    assert dataset["name"] == "Synthetic India ophthalmology cataract retina follow-up CSV"
    assert "Synthetic 14-row ophthalmology workflow sample" in dataset["description"]
    assert "No real patient data" in dataset["description"]


def test_ophthalmology_csv_is_synthetic_and_matches_claimed_counts():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    assert len(rows) == 14
    assert sum(int(row["monthly_items"]) for row in rows) == 903
    assert sum(row["ophthalmologist_review_needed"] == "yes" for row in rows) == 7
    assert sum(row["red_flag_or_emergency_language"] == "yes" for row in rows) == 2
    assert sum(row["cloud_storage_or_link_gap"] == "yes" for row in rows) == 3
    assert all("patient" not in row.get("workflow_id", "").lower() for row in rows)


def test_ophthalmology_asset_is_discoverable():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert PATH in resources
    assert URL in llms
    assert CSV_URL in llms
    assert URL in sitemap
    assert f'"{PATH}"' in builder
