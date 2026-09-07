from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-07'
SLUG = 'cloud-bill-owner-triage'
TITLE = 'Cloud Bill Owner Triage: 6 Checks Before You Cut Costs'
BOUNDARY_TERMS = [
    'Educational operations guide only',
    'not legal, compliance, medical, financial, security, certification, savings',
]


def test_evening_publication_assets_exist_and_are_linked():
    pub = ROOT / 'publications' / DATE
    page = pub / f'{SLUG}.html'
    assert page.exists()
    html = page.read_text(encoding='utf-8')
    assert TITLE in html
    assert f'{SLUG}.png' in html
    assert f'{SLUG}.csv' in html
    assert 'Spike date is known' in html
    assert 'Usage driver is separated' in html
    for term in BOUNDARY_TERMS:
        assert term in html
    for ext in ['svg', 'png', 'csv', 'md']:
        asset = pub / f'{SLUG}.{ext}'
        assert asset.exists()
        assert asset.stat().st_size > 100


def test_evening_publication_manifest_log_and_discovery_links():
    pub = ROOT / 'publications' / DATE
    manifest = json.loads((pub / 'manifest.json').read_text(encoding='utf-8'))
    evening = [m for m in manifest if m.get('slot') == 'evening']
    assert len(evening) == 1
    assert evening[0]['slug'] == SLUG
    assert evening[0]['url'] == f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
    assert evening[0]['png'].endswith(f'/{SLUG}.png')
    index_html = (pub / 'index.html').read_text(encoding='utf-8')
    log = (pub / 'publish-log.md').read_text(encoding='utf-8')
    homepage = (ROOT / 'index.html').read_text(encoding='utf-8')
    llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
    evidence = ROOT / 'docs' / 'publication-evidence' / f'{DATE}-evening-{SLUG}.md'
    assert f'{SLUG}.html' in index_html
    assert f'{SLUG}.html' in log
    assert f'/publications/{DATE}/{SLUG}.html' in homepage
    assert f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html' in llms
    assert evidence.exists()
