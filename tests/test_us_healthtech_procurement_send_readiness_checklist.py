from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "us-healthtech-ai-patient-access-procurement-answer-bank"
PAGE = RESOURCE_DIR / "index.html"
CHECKLIST = RESOURCE_DIR / "us-healthtech-procurement-send-readiness-checklist.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_us_healthtech_answer_bank_links_procurement_send_readiness_checklist():
    html = PAGE.read_text(encoding="utf-8")
    assert "Updated 2026-09-03" in html
    assert "Synthetic US healthtech procurement send readiness checklist CSV" in html
    assert "us-healthtech-procurement-send-readiness-checklist.csv" in html
    assert "Procurement send-readiness checklist" in html
    assert "final owner gate before any AI-assisted answer bank row" in html
    assert "not a real healthtech customer case study" in html
    assert "No outreach was sent" in html


def test_us_healthtech_procurement_send_readiness_checklist_is_synthetic_and_safe():
    rows = list(csv.DictReader(CHECKLIST.open(encoding="utf-8")))
    assert len(rows) == 6
    assert {row["row_type"] for row in rows} == {"synthetic_send_gate"}
    joined = "\n".join(",".join(row.values()) for row in rows)
    assert "HIPAA/PHI and BAA boundaries" in joined
    assert "prior authorization" in joined
    assert "AI human review" in joined
    assert "cloud/LLM spend governance" in joined
    assert "Do not invent certification" in joined
    assert "Do not claim savings ROI" in joined
    assert "without owner approval" in joined


def test_us_healthtech_procurement_checklist_is_discoverable_from_resources_and_llms():
    marker = "us-healthtech-procurement-send-readiness-checklist.csv"
    assert marker in RESOURCES.read_text(encoding="utf-8")
    assert marker in LLMS.read_text(encoding="utf-8")
