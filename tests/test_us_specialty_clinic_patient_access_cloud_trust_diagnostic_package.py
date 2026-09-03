from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-specialty-clinic-patient-access-cloud-trust-diagnostic-package"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_PATH = ROOT / "resources" / SLUG / "us-specialty-clinic-diagnostic-scope-matrix.csv"
PAGE_URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"https://aicloudstrategist.com/resources/{SLUG}/us-specialty-clinic-diagnostic-scope-matrix.csv"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_blocks() -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source(), re.S)
    return [json.loads(block) for block in blocks]


def test_page_has_us_buyer_language_research_and_boundaries() -> None:
    html = source()
    assert "US Specialty Clinic Patient Access + Cloud Trust Diagnostic Package" in html
    assert "North America business-hours build" in html
    for phrase in [
        "US specialty clinic prior authorization automation",
        "referral leakage",
        "HIPAA AI receptionist vendor risk",
        "healthcare security questionnaire",
        "cloud LLM FinOps healthcare SaaS",
    ]:
        assert phrase in html
    for competitor in ["Waystar", "Luma Health", "Phreesia", "NexHealth", "Notable", "FinOps Foundation", "OneTrust"]:
        assert competitor in html
    assert "AICS still has no verified top-3/top-5 ranking" in html
    assert "No outreach was sent" in html
    assert "not a real US clinic" in html
    assert "not PHI/ePHI" in html
    assert "not HIPAA, SOC 2, HITRUST" in html


def test_json_ld_dataset_service_and_faq_are_scope_safe() -> None:
    blocks = json_ld_blocks()
    text = json.dumps(blocks)
    assert PAGE_URL in text
    assert CSV_URL in text
    assert "No-PHI/ePHI evidence review" in text
    assert "Synthetic buyer-education template only" in text
    assert "It is not a HIPAA compliance attestation" in text
    assert "no payment, PHI/ePHI, patient records" in text


def test_csv_is_synthetic_scope_matrix_with_blocked_material() -> None:
    rows = list(csv.DictReader(CSV_PATH.open(newline="", encoding="utf-8")))
    assert len(rows) >= 8
    assert {
        "diagnostic_lane",
        "buyer_question",
        "safe_first_review_input",
        "excluded_material",
        "deliverable",
        "owner_or_adviser_route",
        "external_claim_boundary",
    } <= set(rows[0])
    text = "\n".join(",".join(row.values()) for row in rows).lower()
    for marker in [
        "phi/ephi",
        "no hipaa compliance proof",
        "no authorization-speed",
        "no denial-reduction",
        "no soc 2/hitrust/certification",
        "no savings",
        "no customer",
        "no ranking",
    ]:
        assert marker in text
    blocked = " ".join(row["excluded_material"].lower() for row in rows)
    assert "credentials" in blocked
    assert "ehr/pms exports" in blocked
    assert "cloud-console access" in blocked
    assert "private audit reports" in blocked


def test_discoverability_routes_are_registered() -> None:
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert PAGE_URL in llms
    assert CSV_URL in llms
    assert "/resources/us-specialty-clinic-patient-access-cloud-trust-diagnostic-package/" in resources
    assert "/resources/us-specialty-clinic-patient-access-cloud-trust-diagnostic-package/" in sitemap_script
