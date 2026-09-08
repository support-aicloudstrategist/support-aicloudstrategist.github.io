from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-08'
SLUG = 'ai-agent-cost-spike-triage'
TITLE = 'AI Agent Cost Spike Triage: 7 Checks Before You Scale or Switch Tools'
BOUNDARY = 'Educational operations guide only'


def test_evening_publication_files_exist_and_are_safe():
    pub = ROOT / 'publications' / DATE
    for ext in ['html', 'png', 'svg', 'csv', 'md']:
        assert (pub / f'{SLUG}.{ext}').exists(), ext
    html = (pub / f'{SLUG}.html').read_text(encoding='utf-8')
    assert TITLE in html
    assert f'{SLUG}.png' in html
    assert BOUNDARY in html
    for forbidden in ['testimonial', 'guaranteed savings', 'certified result', 'client logo']:
        assert forbidden not in html.lower()


def test_evening_publication_is_discoverable():
    for rel in ['index.html', 'llms.txt', 'sitemap.xml', f'publications/{DATE}/index.html', f'publications/{DATE}/manifest.json']:
        text = (ROOT / rel).read_text(encoding='utf-8')
        assert SLUG in text
    evidence = ROOT / 'docs' / 'publication-evidence' / f'{DATE}-evening-{SLUG}.md'
    assert evidence.exists()
    assert SLUG in evidence.read_text(encoding='utf-8')
