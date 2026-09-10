from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-10'
SLUG = 'clinic-intake-ai-safety-card'
TITLE = 'Clinic Intake AI Safety Card: 7 Checks Before Automating Patient Questions'


def test_morning_publication_assets_exist_and_are_safe():
    pub = ROOT / 'publications' / DATE
    for suffix in ['html', 'svg', 'png', 'md', 'csv']:
        assert (pub / f'{SLUG}.{suffix}').exists()
    assert (pub / f'{SLUG}-answer-card.json').exists()
    html = (pub / f'{SLUG}.html').read_text(encoding='utf-8')
    assert TITLE in html
    assert f'{SLUG}.png' in html
    assert f'{SLUG}.csv' in html
    assert 'Educational operations guide only' in html
    banned = ['testimonial', 'guaranteed revenue', 'certifies compliance', 'approved client', 'diagnosis advice', 'treatment advice']
    assert not any(term in html.lower() for term in banned)


def test_morning_publication_manifest_index_sitemap_and_llms():
    pub = ROOT / 'publications' / DATE
    manifest = json.loads((pub / 'manifest.json').read_text(encoding='utf-8'))
    posts = manifest['posts']
    assert any(post['slot'] == 'morning' and post['slug'] == SLUG and post['title'] == TITLE for post in posts)
    index = (pub / 'index.html').read_text(encoding='utf-8')
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
    url = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
    assert url in index or f'{SLUG}.html' in index
    assert f'{SLUG}-answer-card.json' in index
    assert url in sitemap
    assert url in llms


def test_morning_answer_card_has_seven_checks_and_boundary():
    card = json.loads((ROOT / 'publications' / DATE / f'{SLUG}-answer-card.json').read_text(encoding='utf-8'))
    assert card['slot'] == 'morning'
    assert len(card['checks']) == 7
    assert 'not medical' in card['boundary']
    assert 'guaranteed-performance' in card['boundary']
