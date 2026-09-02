from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-private-clinic-ai-receptionist-vs-practice-management-patient-growthos-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
REGISTER = ROOT / "resources" / SLUG / "uk-private-clinic-ai-stop-rule-gdpr-evidence-register.csv"
REGISTER_URL = f"https://aicloudstrategist.com/resources/{SLUG}/uk-private-clinic-ai-stop-rule-gdpr-evidence-register.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_blocks(source: str) -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    return [json.loads(block) for block in blocks]


def test_page_links_new_stop_rule_register_and_research_refresh() -> None:
    source = html()
    assert "Europe / UK buyer research snapshot — refreshed 2 Sep 2026" in source
    assert "Semble positioned" in source
    assert "Pabau positioned" in source
    assert "Doctolib UK did not resolve from this environment" in source
    assert "uk-private-clinic-ai-stop-rule-gdpr-evidence-register.csv" in source
    assert "AI stop-rule + GDPR evidence register" in source
    assert '"dateModified":"2026-09-02"' in source


def test_new_dataset_json_ld_is_parseable() -> None:
    blocks = json_ld_blocks(html())
    as_text = json.dumps(blocks)
    assert "Synthetic UK private clinic AI stop-rule and GDPR evidence register" in as_text
    assert REGISTER_URL in as_text
    assert "No compliance, clinical, no-show, revenue, ranking or ROI claim" in as_text


def test_stop_rule_register_is_synthetic_and_owner_ready() -> None:
    assert REGISTER.is_file()
    rows = list(csv.DictReader(REGISTER.open(newline="", encoding="utf-8")))
    assert len(rows) >= 8
    expected = {
        "risk_route",
        "buyer_search_phrase",
        "stop_rule_trigger",
        "minimum_redacted_evidence",
        "owner_role",
        "adviser_needed_flag",
        "aics_output",
        "no_claim_boundary",
    }
    assert expected <= set(rows[0])
    text = "\n".join(",".join(row.values()) for row in rows).lower()
    for phrase in [
        "no recording no transcript",
        "privacy/legal adviser needed",
        "clinical safety adviser may be needed",
        "cloud/ai cost owner register",
        "no gdpr compliance proof",
        "no no-show reduction",
        "no savings roi",
    ]:
        assert phrase in text


def test_llms_discovery_mentions_new_register() -> None:
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REGISTER_URL in llms
    assert "synthetic AI stop-rule + GDPR evidence register CSV" in llms
