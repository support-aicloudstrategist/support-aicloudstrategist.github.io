import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-healthcare-dpdp-cloud-trust-evidence-source-map"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_FILE = ROOT / "resources" / SLUG / "india-healthcare-dpdp-cloud-trust-evidence-source-map.csv"
SVG_FILE = ROOT / "resources" / SLUG / "india-healthcare-dpdp-cloud-trust-owner-map.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_india_healthcare_dpdp_cloud_trust_page_has_buyer_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "DPDP compliance healthcare India" in html
    assert "patient data protection hospital" in html
    assert "ABDM / EMR / HIS handoff" in html
    assert "OneTrust" in html and "Digital Anumati" in html and "PrivacyEngine" in html
    assert "not DPDP compliance proof" in html
    assert "No outreach was sent" in html
    assert "not legal, privacy, security, medical, diagnostic, billing, procurement, architecture or FinOps advice" in html
    assert "dateModified\":\"2026-09-07" in html


def test_india_healthcare_dpdp_json_ld_has_dataset_and_image():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    dataset = next(doc for doc in docs if doc.get("@type") == "Dataset")
    image = next(doc for doc in docs if doc.get("@type") == "ImageObject")
    assert dataset["name"] == "India healthcare DPDP cloud trust evidence source map CSV"
    assert dataset["isAccessibleForFree"] is True
    assert "no patient data" in dataset["keywords"]
    assert image["contentUrl"].endswith("india-healthcare-dpdp-cloud-trust-owner-map.svg")
    assert "not DPDP compliance proof" in image["caption"]


def test_india_healthcare_dpdp_csv_and_svg_are_synthetic_and_no_patient_data():
    rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8")))
    assert len(rows) == 8
    assert rows[0]["evidence_area"] == "patient_data_inventory"
    assert any("not DPDP compliance proof" in row["proof_boundary"] for row in rows)
    svg = SVG_FILE.read_text(encoding="utf-8")
    assert "Demo / synthetic only" in svg
    assert "no patient names" in svg
    assert "no compliance proof" in svg


def test_india_healthcare_dpdp_pack_is_discoverable_from_hub_llms_and_sitemap():
    for content in (RESOURCES.read_text(encoding="utf-8"), LLMS.read_text(encoding="utf-8"), SITEMAP.read_text(encoding="utf-8")):
        assert f"/resources/{SLUG}/" in content or f"https://aicloudstrategist.com/resources/{SLUG}/" in content
    llms = LLMS.read_text(encoding="utf-8")
    resources = RESOURCES.read_text(encoding="utf-8")
    assert "india-healthcare-dpdp-cloud-trust-evidence-source-map.csv" in llms
    assert "india-healthcare-dpdp-cloud-trust-owner-map.svg" in llms
    assert "india-healthcare-dpdp-cloud-trust-evidence-source-map.csv" in resources
    assert "india-healthcare-dpdp-cloud-trust-owner-map.svg" in resources
