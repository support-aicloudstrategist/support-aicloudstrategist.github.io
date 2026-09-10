from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-10'
SLUG = 'support-ticket-ai-reply-boundary-card'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'


def test_night_publication_assets_exist_and_are_claim_safe():
    pub = ROOT / 'publications' / DATE
    page = (pub / f'{SLUG}.html').read_text(encoding='utf-8')
    card = json.loads((pub / f'{SLUG}-answer-card.json').read_text(encoding='utf-8'))
    rows = list(csv.DictReader((pub / f'{SLUG}.csv').open(encoding='utf-8')))

    assert (pub / f'{SLUG}.png').stat().st_size > 10000
    assert (pub / f'{SLUG}.svg').exists()
    assert len(rows) == 7
    assert "Download CSV worksheet" in page
    assert "When this should become a paid diagnostic" in page
    assert "No customer, SLA, revenue, savings, compliance, legal, refund, security, ranking or incident-resolution claims" in page
    assert card['url'] == URL
    assert card['date'] == DATE
    assert card['slot'] == 'night'
    assert 'support-SLA' in card['boundary']


def test_night_publication_is_discoverable_in_index_sitemap_llms_and_resources():
    index = (ROOT / 'publications' / DATE / 'index.html').read_text(encoding='utf-8')
    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
    resources = (ROOT / 'resources' / 'index.html').read_text(encoding='utf-8')

    assert f'{SLUG}.html' in index
    assert f'{SLUG}.png' in index
    assert f'{SLUG}.csv' in index
    assert f'{SLUG}-answer-card.json' in index
    assert URL in sitemap
    assert f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv' in sitemap
    assert f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}-answer-card.json' in sitemap
    assert URL in llms
    assert f'data-resource-card="{SLUG}"' in resources
    assert f'/publications/{DATE}/{SLUG}.csv' in resources
