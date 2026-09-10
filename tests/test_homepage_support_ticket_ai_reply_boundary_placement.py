from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
SLUG = "support-ticket-ai-reply-boundary-card"
PAGE_URL = f"/publications/2026-09-10/{SLUG}.html"


def test_homepage_surfaces_latest_support_ticket_ai_reply_boundary_card() -> None:
    html = HOME.read_text(encoding="utf-8")
    assert html.count(PAGE_URL) == 1
    assert f'data-homepage-publication="{SLUG}"' in html
    assert "SLA updates" in html
    assert "refund responses" in html
    assert "commitment-bearing helpdesk messages" in html

    proof_section = "Representative engagement output"
    clinic_card = 'data-homepage-publication="clinic-intake-ai-safety-card"'
    assert html.index(PAGE_URL) > html.index(proof_section)
    assert html.index(PAGE_URL) < html.index(clinic_card)
