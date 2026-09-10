from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SLUG = "clinic-intake-ai-safety-card"
URL = f"/publications/2026-09-10/{SLUG}.html"


def test_clinic_intake_publication_is_in_evidence_grid_not_hero():
    html = INDEX.read_text(encoding="utf-8")
    assert html.count(URL) == 1
    assert 'data-homepage-publication="clinic-intake-ai-safety-card"' in html

    hero_end = html.index('<section class="section ea-business-system" id="what-we-do">')
    evidence_start = html.index('<section class="section ea-evidence" id="evidence">')
    evidence_end = html.index('<section class="section ea-engagement" id="engagement">', evidence_start)

    assert URL not in html[:hero_end]
    assert URL in html[evidence_start:evidence_end]
    assert html.index(URL) > html.index('data-homepage-resource="uae-healthtech-cloud-trust-executive-summary"')


def test_llms_includes_clinic_intake_answer_card_for_ai_discovery():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "Clinic intake AI safety answer card JSON" in llms
    assert "clinic-intake-ai-safety-card-answer-card.json" in llms
    assert "claim boundaries for clinic-intake AI automation questions" in llms
