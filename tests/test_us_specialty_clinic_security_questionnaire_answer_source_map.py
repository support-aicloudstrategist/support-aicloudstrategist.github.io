from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-specialty-clinic-security-questionnaire-answer-source-map"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_PATH = ROOT / "resources" / SLUG / "us-specialty-clinic-security-questionnaire-answer-source-map.csv"
CSV_URL = f"https://aicloudstrategist.com/resources/{SLUG}/us-specialty-clinic-security-questionnaire-answer-source-map.csv"
PAGE_URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_blocks() -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source(), re.S)
    return [json.loads(block) for block in blocks]


def test_page_has_buyer_language_competitors_and_boundaries() -> None:
    html = source()
    assert "US specialty clinic security-questionnaire answer-source map" in html
    assert "North America / US Pacific entering business hours" in html
    assert "HIPAA AI receptionist vendor risk" in html
    assert "prior authorization workflow automation" in html
    assert "referral leakage owner queue" in html
    for competitor in ["Waystar", "Luma Health", "Phreesia", "NexHealth", "Notable", "CloudZero", "Vanta", "Drata", "OneTrust"]:
        assert competitor in html
    assert "AICS still has no verified top-3/top-5 ranking" in html
    assert "No outreach was sent" in html
    assert "no real clinic" in html
    assert "not HIPAA compliance attestation" not in html  # ensure wording remains explicit elsewhere, not hidden as an attestation
    assert "No HIPAA compliance proof" in html


def test_dataset_json_ld_points_to_synthetic_csv() -> None:
    blocks = json_ld_blocks()
    text = json.dumps(blocks)
    assert PAGE_URL in text
    assert CSV_URL in text
    assert "Synthetic US specialty clinic security questionnaire answer-source map CSV" in text
    assert "HIPAA AI receptionist evidence boundary" in text


def test_csv_is_synthetic_no_phi_owner_map() -> None:
    rows = list(csv.DictReader(CSV_PATH.open(newline="", encoding="utf-8")))
    assert len(rows) >= 8
    assert {
        "question_id",
        "buyer_search_phrase",
        "answer_topic",
        "allowed_first_pass_evidence",
        "blocked_first_pass_material",
        "accountable_owner",
        "adviser_needed_flag",
        "aics_output",
        "external_claim_boundary",
    } <= set(rows[0])
    text = "\n".join(",".join(row.values()) for row in rows).lower()
    for phrase in [
        "no hipaa compliance proof",
        "no authorization-speed",
        "clinical safety adviser may be needed",
        "no soc 2/hitrust/certification",
        "no savings",
        "no customer",
    ]:
        assert phrase in text
    blocked = " ".join(row["blocked_first_pass_material"].lower() for row in rows)
    assert "phi/ephi" in blocked
    assert "ehr/pms exports" in blocked
    assert "private soc 2 reports" in blocked


def test_llms_resources_and_sitemap_discoverability() -> None:
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert PAGE_URL in llms
    assert CSV_URL in llms
    assert "/resources/us-specialty-clinic-security-questionnaire-answer-source-map/" in resources
    assert "/resources/us-specialty-clinic-security-questionnaire-answer-source-map/" in sitemap_script
