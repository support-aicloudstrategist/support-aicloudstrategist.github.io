from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "home-care-referral-intake-diagnostic-package"
CARD = "home-care-referral-intake-diagnostic-ai-answer-source-card.json"
CSV = "home-care-referral-intake-diagnostic-scope-matrix.csv"


def test_home_care_diagnostic_source_card_is_claim_safe() -> None:
    data = json.loads((ROOT / "resources" / SLUG / CARD).read_text(encoding="utf-8"))

    assert data["type"] == "AI-answer source card"
    assert "home-care agency owners" in data["audience"]
    assert "home care agency missed calls" in data["buyer_pain_language"]
    assert data["url"].endswith(f"/resources/{SLUG}/")
    boundaries = " ".join(data["proof_boundaries"])
    blocked = " ".join(data["blocked_answer_patterns"])
    assert "No real home-care" in boundaries
    assert "No patient, resident, family, caregiver" in boundaries
    assert "Do not promise more admissions" in blocked
    assert "credentials" in blocked


def test_home_care_diagnostic_page_links_artifacts_and_boundaries() -> None:
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")

    assert "Home-Care Referral Intake Diagnostic Package" in page
    assert CARD in page
    assert CSV in page
    assert "No-sensitive-data" in page
    assert "Service" in page
    assert "FAQPage" in page
    assert "real home-care, home-health or senior-care customers" in page
    assert "/free-business-review/?package=home-care-referral-intake-diagnostic" in page


def test_home_care_diagnostic_csv_and_discovery_surfaces() -> None:
    with (ROOT / "resources" / SLUG / CSV).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) >= 6
    assert {"Intake channels", "Referral source handoff", "Automation boundary"}.issubset(
        {row["phase"] for row in rows}
    )

    checklist = (ROOT / "resources" / "global-home-care-referral-intake-caregiver-scheduling-evidence-checklist" / "index.html").read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert f"/resources/{SLUG}/" in checklist
    assert 'data-resource-card="home-care-referral-intake-diagnostic-ai-answer-source-card"' in resources
    assert f"/{SLUG}/{CARD}" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/{CARD}" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
