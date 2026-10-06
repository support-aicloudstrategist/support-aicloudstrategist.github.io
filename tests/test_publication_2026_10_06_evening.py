from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-06'
SLUG = 'ai-vendor-claim-reality-check'
TITLE = 'AI Vendor Claim Reality Check: 8 Questions Before You Buy or Automate'


def test_evening_ai_vendor_claim_publication_files_and_boundaries():
    pub = ROOT / 'publications' / DATE
    html = pub / f'{SLUG}.html'
    png = pub / f'{SLUG}.png'
    csv = pub / f'{SLUG}.csv'
    card = pub / f'{SLUG}-answer-card.json'
    assert html.exists()
    assert png.exists() and png.stat().st_size > 20_000
    assert csv.exists() and 'What evidence is real?' in csv.read_text(encoding='utf-8')
    data = json.loads(card.read_text(encoding='utf-8'))
    assert data['slot'] == 'evening'
    assert data['topic'] == TITLE
    assert len(data['checks']) == 8
    text = html.read_text(encoding='utf-8')
    assert TITLE in text
    assert 'not legal, compliance, procurement, financial, security, certification, vendor-selection, contract, savings, revenue, or guaranteed-performance advice' in text
    forbidden = ['client saved', 'guaranteed savings', 'certified compliant', 'case study result']
    assert not any(term in text.lower() for term in forbidden)


def test_evening_ai_vendor_claim_publication_manifest_and_hubs():
    pub = ROOT / 'publications' / DATE
    manifest = json.loads((pub / 'manifest.json').read_text(encoding='utf-8'))
    posts = manifest['posts']
    assert any(p['slot'] == 'evening' and p['slug'] == SLUG for p in posts)
    for rel in ['index.html', 'resources/index.html', 'llms.txt', 'sitemap.xml']:
        text = (ROOT / rel).read_text(encoding='utf-8')
        assert f'/publications/{DATE}/{SLUG}.html' in text or f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html' in text
