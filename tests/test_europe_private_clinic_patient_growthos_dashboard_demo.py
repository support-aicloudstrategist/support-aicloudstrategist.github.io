from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-private-clinic-patient-growthos-dashboard-demo"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
SVG = ROOT / "resources" / SLUG / f"{SLUG}.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"

def html() -> str:
    return PAGE.read_text(encoding="utf-8")

def json_ld_blocks(source: str) -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    return [json.loads(block) for block in blocks]

def test_page_is_indexable_and_canonical() -> None:
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"/>' in source
    assert "Europe private clinic Patient GrowthOS owner dashboard demo" in source
    assert "Request review scope" in source

def test_structured_data_and_dataset_are_parseable() -> None:
    blocks = json_ld_blocks(html())
    as_text = json.dumps(blocks)
    assert "Article" in as_text
    assert "Dataset" in as_text
    assert "FAQPage" in as_text
    assert URL in as_text
    assert f"{SLUG}.csv" in as_text
    assert "GDPR patient engagement" in as_text

def test_synthetic_csv_and_svg_assets_exist() -> None:
    assert CSV.is_file()
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) >= 6
    assert {"source", "country_context", "patient_request_type", "owner", "gdrp_adviser_question", "ai_boundary", "decision_status"} <= set(rows[0])
    assert any("Missed phone call" in row["source"] for row in rows)
    assert SVG.is_file()
    svg = SVG.read_text(encoding="utf-8")
    assert "Synthetic Europe private clinic Patient GrowthOS owner dashboard demo" in svg
    assert "Truth boundary" in svg

def test_truth_boundary_prevents_fake_proof() -> None:
    source = html().lower()
    for phrase in [
        "synthetic demo",
        "not a real client case study",
        "not production clinic data",
        "not patient data",
        "not gdpr compliance proof",
        "not booking uplift evidence",
        "not revenue evidence",
        "not roi evidence",
        "no outreach was sent",
    ]:
        assert phrase in source

def test_discovery_links_are_wired() -> None:
    resource_index = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    checklist = (ROOT / "resources" / "europe-private-clinic-gdpr-patient-growthos-evidence-checklist" / "index.html").read_text(encoding="utf-8")
    for source in [resource_index, llms, sitemap_builder, sitemap, checklist]:
        assert f"/resources/{SLUG}/" in source

def test_related_cluster_links_exist() -> None:
    source = html()
    for target in [
        "/resources/europe-private-clinic-gdpr-patient-growthos-evidence-checklist/",
        "/healthcare-growthos/",
        "/case-studies/",
        "/free-business-review/?package=europe-private-clinic-patient-growthos-dashboard-demo",
    ]:
        assert target in source
