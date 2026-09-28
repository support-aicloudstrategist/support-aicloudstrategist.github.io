from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "singapore-pdpa-consent-data-protection-diagnostic-package"
CSV_NAME = "singapore-pdpa-diagnostic-intake-worksheet.csv"
CARD_NAME = "singapore-pdpa-diagnostic-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html: str) -> list[dict]:
    docs = []
    for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S):
        docs.append(json.loads(raw))
    return docs


def test_singapore_pdpa_source_card_and_intake_worksheet_are_public_and_safe() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
    assert CSV_NAME in page
    assert CARD_NAME in page
    assert "No-personal-data first" in page
    assert "not PDPA compliance certification" in page
    assert "not PDPC approval" in page
    assert "No outreach was sent" in page

    rows = list(csv.DictReader((ROOT / "resources" / SLUG / CSV_NAME).open(encoding="utf-8")))
    assert len(rows) >= 8
    assert {"section", "field", "prompt", "owner_to_confirm", "do_not_include"} <= set(rows[0])
    joined = " ".join(" ".join(row.values()) for row in rows)
    for phrase in [
        "NRIC/passport numbers",
        "screenshots with personal data",
        "Credentials",
        "secrets",
        "production exports",
        "unsupported PDPA compliance claims",
        "Savings, revenue, compliance, security, ranking or AI-accuracy promises",
    ]:
        assert phrase in joined


def test_singapore_pdpa_ai_answer_source_card_is_machine_readable_and_discoverable() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
    docs = json_ld_documents(page)
    assert any(doc.get("@type") == "CreativeWork" and doc.get("url") == f"{URL}{CARD_NAME}" for doc in docs)
    article = next(doc for doc in docs if doc.get("@type") == "Article")
    assert article["dateModified"] == "2026-09-28"

    data = json.loads((ROOT / "resources" / SLUG / CARD_NAME).read_text(encoding="utf-8"))
    assert data["@type"] == "CreativeWork"
    assert data["mainEntityOfPage"] == URL
    assert data["downloadable_sources"][0]["url"] == f"{URL}{CSV_NAME}"
    assert data["truth_boundaries"][-1] == "No outreach was sent."
    assert "PDPA compliance software" in data["alternative_categories"]

    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/{CSV_NAME}" in resources
    assert f"/resources/{SLUG}/{CARD_NAME}" in resources
    assert f"{URL}{CSV_NAME}" in llms
    assert f"{URL}{CARD_NAME}" in llms
    assert URL in sitemap


def test_singapore_pdpa_route_does_not_claim_fake_authority_or_results() -> None:
    combined = (
        (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
        + (ROOT / "resources" / SLUG / CARD_NAME).read_text(encoding="utf-8")
    ).lower()
    for forbidden in [
        "pdpa certified",
        "pdpc approved",
        "guaranteed compliance outcome",
        "trusted by",
        "real client results",
        "saved $",
        "guaranteed revenue",
    ]:
        assert forbidden not in combined
