from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "publications" / "2026-09-03" / "ai-source-evidence-card.html"
CSV_PATH = ROOT / "publications" / "2026-09-03" / "ai-source-evidence-register-template.csv"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"
PAGE_URL = "https://aicloudstrategist.com/publications/2026-09-03/ai-source-evidence-card.html"
CSV_URL = "https://aicloudstrategist.com/publications/2026-09-03/ai-source-evidence-register-template.csv"


def test_ai_source_evidence_page_links_downloadable_register() -> None:
    html = PAGE.read_text(encoding="utf-8")
    assert "Download the source evidence register" in html
    assert "ai-source-evidence-register-template.csv" in html
    assert "Truth boundary" in html
    assert "not legal, compliance, medical, financial, security" in html


def test_ai_source_evidence_register_has_safe_operating_columns() -> None:
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 3
    assert rows[0].keys() >= {
        "source_name",
        "source_owner",
        "date_checked",
        "permission_level",
        "allowed_use",
        "answer_boundary",
        "human_reviewer",
        "evidence_saved",
        "correction_or_update_note",
    }
    assert {row["permission_level"] for row in rows} == {"Public", "Internal", "Customer confidential"}
    assert any("Pause" in row["answer_boundary"] for row in rows)


def test_ai_source_evidence_daily_index_links_card_and_register() -> None:
    index = (ROOT / "publications" / "2026-09-03" / "index.html").read_text(encoding="utf-8")
    assert "ai-source-evidence-card.html" in index
    assert "ai-source-evidence-register-template.csv" in index
    assert "downloadable owner-evidence templates" in index
    assert "not legal, compliance, medical, financial, security" in index


def test_ai_source_evidence_asset_is_discoverable_without_overclaiming() -> None:
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert PAGE_URL in llms
    assert CSV_URL in llms
    assert PAGE_URL in sitemap
    assert "client outcomes" in llms
    assert "does not guarantee search rankings" in llms
