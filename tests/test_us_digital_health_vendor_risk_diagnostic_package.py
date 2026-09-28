from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-digital-health-vendor-risk-diagnostic-package"
CSV_NAME = "us-digital-health-vendor-risk-diagnostic-intake-worksheet.csv"
CARD_NAME = "us-digital-health-vendor-risk-diagnostic-ai-answer-source-card.json"


def test_vendor_risk_diagnostic_intake_worksheet_is_linked_and_no_phi_first() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
    assert CSV_NAME in page
    assert "without requesting PHI/ePHI, credentials, secrets, raw audit files or production exports" in page
    assert "Starting from USD 2,500" in page

    rows = list(csv.DictReader((ROOT / "resources" / SLUG / CSV_NAME).open(encoding="utf-8")))
    assert len(rows) >= 8
    assert {"section", "field", "prompt", "owner_to_confirm", "do_not_include"} <= set(rows[0])
    joined = " ".join(" ".join(row.values()) for row in rows)
    assert "PHI/ePHI" in joined
    assert "credentials" in joined
    assert "raw audit" in joined
    assert "Unsupported compliance claims" in joined


def test_vendor_risk_diagnostic_source_card_exposes_download_with_boundaries() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD_NAME).read_text(encoding="utf-8"))
    downloads = data["downloadable_sources"]
    urls = [item["url"] for item in downloads]
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CSV_NAME}" in urls
    worksheet = next(item for item in downloads if item["url"].endswith(CSV_NAME))
    assert "No-PHI/ePHI first" in worksheet["boundary"]
    assert "do not include credentials" in worksheet["boundary"]
    assert data["truth_boundaries"][-1] == "No outreach was sent."

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CSV_NAME}" in llms
