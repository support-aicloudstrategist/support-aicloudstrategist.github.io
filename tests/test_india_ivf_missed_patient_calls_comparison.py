import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-ivf-fertility-missed-patient-calls-vs-crm-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "india-ivf-missed-patient-calls-comparison.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_targets_ivf_missed_call_buyer_language():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "IVF clinic missed patient calls",
        "fertility clinic lead leakage",
        "IVF clinic leads not converting",
        "clinic counsellor follow-up WhatsApp",
        "AI receptionist for IVF clinic",
    ]:
        assert phrase in html


def test_comparison_positions_aics_without_fake_claims():
    html = PAGE.read_text(encoding="utf-8")
    for option in ["Clinic CRM", "WhatsApp automation", "AI receptionist", "Marketing agency", "AICS owner-evidence review"]:
        assert option in html
    for phrase in ["no-credentials source-to-owner evidence queue", "No real IVF clinic", "Exact ranking, AI-answer inclusion"]:
        assert phrase in html
    forbidden = ["guaranteed patient increase", "real IVF clinic result", "certified DPDP", "pregnancy success", "ranking #1"]
    assert all(term not in html for term in forbidden)


def test_csv_is_synthetic_and_linked():
    html = PAGE.read_text(encoding="utf-8")
    assert "india-ivf-missed-patient-calls-comparison.csv" in html
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    assert len(rows) == 5
    assert rows[0]["route"] == "Clinic CRM or fertility software"
    assert all("Synthetic" in row["claim_boundary"] or "Readiness" in row["claim_boundary"] for row in rows)


def test_synthetic_owner_dashboard_is_linked_and_bounded():
    html = PAGE.read_text(encoding="utf-8")
    svg_name = "india-ivf-counsellor-leakage-owner-dashboard.svg"
    assert svg_name in html
    svg = (PAGE.parent / svg_name).read_text(encoding="utf-8")
    for phrase in [
        "Synthetic India IVF counsellor leakage owner dashboard",
        "no patient, clinic, PHI, appointment, revenue or DPDP compliance claim",
        "Human-review stops",
        "Owner handoff proof",
    ]:
        assert phrase in svg


def test_schema_and_discovery_files_include_ivf_resource():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    article = next(doc for doc in docs if doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-01"
    assert "IVF clinic missed patient calls" in article["about"]
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f'"/resources/{SLUG}/"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in (ROOT / "resources" / "ivf-clinic-lead-leakage-checklist" / "index.html").read_text(encoding="utf-8")
