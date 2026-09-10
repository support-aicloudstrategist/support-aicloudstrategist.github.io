from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "resources" / "index.html"
SLUG = "clinic-intake-ai-safety-card"
PAGE_URL = f"/publications/2026-09-10/{SLUG}.html"
CSV_URL = f"/publications/2026-09-10/{SLUG}.csv"
ANSWER_CARD_URL = f"/publications/2026-09-10/{SLUG}-answer-card.json"


def test_clinic_intake_publication_is_featured_once_near_top_of_resources_hub() -> None:
    html = RESOURCES.read_text(encoding="utf-8")
    assert html.count(PAGE_URL) == 1
    assert f'data-resource-card="{SLUG}"' in html
    assert CSV_URL in html
    assert ANSWER_CARD_URL in html

    intro = "Proof-first AI, cloud trust, FinOps and growth-system resources"
    first_existing_card = 'data-resource-card="uae-healthtech-cloud-trust-patient-data-evidence-source-map"'
    assert html.index(PAGE_URL) > html.index(intro)
    assert html.index(PAGE_URL) < html.index(first_existing_card)


def test_resources_hub_clinic_intake_copy_preserves_claim_boundaries() -> None:
    html = RESOURCES.read_text(encoding="utf-8")
    card_start = html.index(f'data-resource-card="{SLUG}"')
    next_card = html.index('data-resource-card="uae-healthtech-cloud-trust-patient-data-evidence-source-map"', card_start)
    card = html[card_start:next_card]
    for marker in ["no-PHI", "human review", "before platform or automation spend"]:
        assert marker in card
