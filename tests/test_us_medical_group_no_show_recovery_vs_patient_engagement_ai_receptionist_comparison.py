import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-medical-group-no-show-recovery-comparison.csv"
SVG = ROOT / "resources" / SLUG / "demo-no-show-recovery-owner-dashboard.svg"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_has_north_america_buyer_language_and_competitor_categories():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "31 Aug 2026 North America buyer-language refresh",
        "reduce patient no-shows",
        "appointment reminder automation",
        "waitlist fill owner queue",
        "patient engagement platform comparison",
        "AI receptionist HIPAA boundary",
        "Waystar RCM/financial-clearance language",
        "Luma Health patient success/platform language",
        "Phreesia was reachable but the sampled URL returned a 404",
        "Search pages were blocked/noisy",
    ]:
        assert phrase in html


def test_comparison_matrix_positions_aics_without_fake_proof():
    html = PAGE.read_text(encoding="utf-8")
    for option in ["Patient engagement / access platforms", "AI receptionist / voice / texting vendors", "EHR/PMS reminder modules", "Call centers / answering services", "RCM / prior-authorization services"]:
        assert option in html
    for phrase in ["source-to-status ageing", "human-review boundary", "No-credentials intake", "Fixed-scope diagnostic offer", "not a customer case study"]:
        assert phrase in html
    forbidden = ["guaranteed no-show reduction", "certified HIPAA compliant", "Acme Medical Group", "customer testimonial says"]
    assert all(term not in html for term in forbidden)


def test_csv_is_synthetic_and_has_expected_rows():
    text = CSV.read_text(encoding="utf-8")
    assert "comparison_option,credible_for,leadership_gap,aics_wedge,proof_boundary" in text
    assert text.count("Synthetic row only") >= 5
    assert "not HIPAA proof" in text
    assert "not payer, claims or denial evidence" in text


def test_demo_dashboard_svg_is_linked_and_truth_bounded():
    html = PAGE.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")
    assert "demo-no-show-recovery-owner-dashboard.svg" in html
    for phrase in [
        "Demo owner dashboard SVG",
        "demo/synthetic",
        "without touching patient data or production credentials",
    ]:
        assert phrase in html
    for phrase in [
        "DEMO / SYNTHETIC ONLY",
        "no PHI, ePHI, patient file, payer file, EHR export, call recording, client data or compliance proof",
        "No no-show, ROI or compliance claim",
        "not a customer case study",
    ]:
        assert phrase in svg


def test_schema_and_discovery_files_include_resource():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    graph_docs = [node for doc in docs if "@graph" in doc for node in doc["@graph"]]
    article = next(node for node in graph_docs if node.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-08-31"
    assert "patient engagement platform comparison" in article["about"]
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f'"/resources/{SLUG}/"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
