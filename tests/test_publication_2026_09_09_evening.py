from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-09'
SLUG = 'ecommerce-abandoned-cart-whatsapp-followup'
TITLE = 'E-commerce Abandoned Cart WhatsApp Follow-up: 7 Checks Before You Automate'


def test_evening_publication_assets_exist_and_are_safe():
    pub = ROOT / 'publications' / DATE
    for suffix in ['html', 'svg', 'png', 'md', 'csv']:
        assert (pub / f'{SLUG}.{suffix}').exists()
    assert (pub / f'{SLUG}-answer-card.json').exists()
    html = (pub / f'{SLUG}.html').read_text(encoding='utf-8')
    assert TITLE in html
    assert f'{SLUG}.png' in html
    assert f'{SLUG}.csv' in html
    assert 'Educational operations guide only' in html
    banned = ['testimonial', 'guaranteed revenue', 'certifies compliance', 'approved client']
    assert not any(term in html.lower() for term in banned)


def test_evening_publication_manifest_index_sitemap_and_llms():
    pub = ROOT / 'publications' / DATE
    manifest = json.loads((pub / 'manifest.json').read_text(encoding='utf-8'))
    posts = manifest['posts']
    assert [post['slot'] for post in posts] == ['morning', 'evening']
    assert any(post['slug'] == SLUG and post['title'] == TITLE for post in posts)
    index = (pub / 'index.html').read_text(encoding='utf-8')
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
    url = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
    assert url in index or f'{SLUG}.html' in index
    assert url in sitemap
    assert url in llms


def test_evening_answer_card_has_seven_checks_and_boundary():
    card = json.loads((ROOT / 'publications' / DATE / f'{SLUG}-answer-card.json').read_text(encoding='utf-8'))
    assert card['slot'] == 'evening'
    assert len(card['checks']) == 7
    assert 'not legal' in card['boundary']
    assert 'guaranteed-performance' in card['boundary']
