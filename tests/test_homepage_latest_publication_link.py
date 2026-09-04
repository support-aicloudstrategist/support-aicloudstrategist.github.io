from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
DATE = "2026-09-04"
SLUG = "ai-change-approval-card"
TITLE = "The AI Change Approval Card"
PUBLICATION = ROOT / "publications" / DATE / f"{SLUG}.html"
PNG = ROOT / "publications" / DATE / f"{SLUG}.png"
CSV = ROOT / "publications" / DATE / f"{SLUG}.csv"


def test_homepage_surfaces_latest_ai_change_approval_card_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = f"/publications/{DATE}/{SLUG}.html"
    assert href in home
    assert f'<h3><a href="{href}">{TITLE}</a></h3>' in home
    assert TITLE in home
    assert f"<link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'>" in publication
    assert "ai change approval card" in publication.lower()
    assert "human approval before it affects customers, money, credentials, policy, or live systems" in publication
    assert "not legal, compliance, medical, financial" in publication


def test_morning_publication_has_infographic_and_csv_evidence():
    assert PNG.exists()
    assert PNG.stat().st_size > 1000
    assert CSV.exists()
    csv = CSV.read_text(encoding="utf-8")
    assert "approval_required" in csv
    assert "human_owner" in csv
    assert "safe_to_proceed_without_approval" in csv
