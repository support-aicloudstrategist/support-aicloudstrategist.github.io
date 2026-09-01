from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
PUBLICATION = ROOT / "publications" / "2026-09-01" / "missed-lead-follow-up-ladder.html"


def test_homepage_surfaces_latest_missed_lead_follow_up_ladder_publication():
    home = HOME.read_text(encoding="utf-8")
    publication = PUBLICATION.read_text(encoding="utf-8")

    href = "/publications/2026-09-01/missed-lead-follow-up-ladder.html"
    assert href in home
    assert "The Missed Lead Follow-Up Ladder" in home
    assert "<link rel='canonical' href='https://aicloudstrategist.com/publications/2026-09-01/missed-lead-follow-up-ladder.html'>" in publication
    assert "missed lead follow-up ladder" in publication.lower()
    assert "not legal, compliance, medical, financial" in publication
