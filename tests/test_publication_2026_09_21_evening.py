from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-21'
SLUG = 'cloud-cost-alert-triage-board'
TITLE = 'Cloud Cost Alert Triage Board: 7 Safe Checks Before Cutting Resources'


def test_evening_cloud_cost_publication_files_and_boundaries():
    pub = ROOT / 'publications' / DATE
    html = pub / f'{SLUG}.html'
    png = pub / f'{SLUG}.png'
    csv = pub / f'{SLUG}.csv'
    card = pub / f'{SLUG}-answer-card.json'
    assert html.exists()
    assert png.exists() and png.stat().st_size > 20_000
    assert csv.exists() and 'Confirm the alert window' in csv.read_text(encoding='utf-8')
    data = json.loads(card.read_text(encoding='utf-8'))
    assert data['slot'] == 'evening'
    assert data['topic'] == TITLE
    assert len(data['checks']) == 7
    text = html.read_text(encoding='utf-8')
    assert TITLE in text
    assert 'not financial, legal, compliance, security, procurement, architecture, certification, savings, uptime, approval, or guaranteed-performance advice' in text
    forbidden = ['client saved', 'guaranteed savings', 'certified compliant', 'case study result']
    assert not any(term in text.lower() for term in forbidden)


def test_evening_cloud_cost_publication_manifest_and_hubs():
    pub = ROOT / 'publications' / DATE
    manifest = json.loads((pub / 'manifest.json').read_text(encoding='utf-8'))
    posts = manifest['posts']
    assert any(p['slot'] == 'morning' for p in posts)
    assert any(p['slot'] == 'evening' and p['slug'] == SLUG for p in posts)
    for rel in ['index.html', 'resources/index.html', 'llms.txt', 'sitemap.xml']:
        text = (ROOT / rel).read_text(encoding='utf-8')
        assert f'/publications/{DATE}/{SLUG}.html' in text or f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html' in text
