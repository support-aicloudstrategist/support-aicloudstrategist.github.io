from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publications" / "2026-09-28"
CONVERSION_URL = "https://aicloudstrategist.com/free-business-review/?source=publication-2026-09-28-crm-handoff-gate"


def test_2026_09_28_support_publication_routes_review_ctas_to_primary_domain():
    for page in [PUB / "index.html", PUB / "meeting-notes-crm-handoff-gate.html"]:
        html = page.read_text(encoding="utf-8")
        assert CONVERSION_URL in html
        assert "href='/free-business-review/'" not in html
        assert 'href="/free-business-review/"' not in html
