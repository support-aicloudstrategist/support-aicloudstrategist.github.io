from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-03"
SLUG = "ai-procurement-answer-boundary-card"
TITLE = "The AI Procurement Answer Boundary Card"
PAGE = ROOT / "publications" / DATE / f"{SLUG}.html"
CSV_PATH = ROOT / "publications" / DATE / f"{SLUG}.csv"
PNG = ROOT / "publications" / DATE / f"{SLUG}.png"
MANIFEST = ROOT / "publications" / DATE / "manifest.json"
HOME = ROOT / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"
PAGE_URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html"
CSV_URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv"


def test_ai_procurement_answer_boundary_page_is_downloadable_and_safe() -> None:
    html = PAGE.read_text(encoding="utf-8")
    assert TITLE in html
    assert "Download the procurement answer boundary CSV" in html
    assert f"{SLUG}.csv" in html
    assert "Truth boundary" in html
    assert "not legal, compliance, medical, financial, security" in html
    assert "procurement-approval" in html
    assert "customer-result" in html


def test_ai_procurement_answer_boundary_csv_routes_risky_answers_to_owners() -> None:
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 3
    assert rows[0].keys() >= {
        "question_area",
        "buyer_question",
        "answer_route",
        "source_required",
        "pause_trigger",
        "human_owner",
        "safe_note",
    }
    joined = "\n".join(" ".join(row.values()) for row in rows)
    assert "Security / technical owner" in joined
    assert "Privacy / legal / data owner" in joined
    assert "Do not invent capability, date, discount, or guarantee" in joined
    assert "Pause" in joined


def test_afternoon_publication_is_discoverable_from_home_llms_sitemap_and_manifest() -> None:
    assert PNG.exists()
    assert PNG.stat().st_size > 1000
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert any(entry["slot"] == "afternoon" and entry["slug"] == SLUG for entry in manifest)
    assert f'/publications/{DATE}/{SLUG}.html' in HOME.read_text(encoding="utf-8")
    assert PAGE_URL in LLMS.read_text(encoding="utf-8")
    assert CSV_URL in LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert PAGE_URL in sitemap
    assert CSV_URL not in sitemap
