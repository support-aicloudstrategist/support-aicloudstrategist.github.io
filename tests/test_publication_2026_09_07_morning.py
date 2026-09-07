from pathlib import Path
import csv

REPO = Path(__file__).resolve().parents[1]
DATE = '2026-09-07'
SLUG = 'manual-work-automation-triage'
TITLE = 'Manual Work Automation Triage: 6 Checks Before You Automate'
BOUNDARY_FRAGMENT = 'Educational operations guide only'


def test_morning_publication_page_assets_and_safety_boundary():
    pub_dir = REPO / 'publications' / DATE
    page = pub_dir / f'{SLUG}.html'
    png = pub_dir / f'{SLUG}.png'
    svg = pub_dir / f'{SLUG}.svg'
    md = pub_dir / f'{SLUG}.md'
    csv_path = pub_dir / f'{SLUG}.csv'

    assert page.exists()
    assert png.exists() and png.stat().st_size > 10_000
    assert svg.exists() and svg.stat().st_size > 5_000
    assert md.exists()
    assert csv_path.exists()

    html = page.read_text(encoding='utf-8')
    assert TITLE in html
    assert f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html' in html
    assert f'{SLUG}.png' in html
    assert BOUNDARY_FRAGMENT in html
    for boundary_phrase in ['customer-result', 'guaranteed-performance advice']:
        assert boundary_phrase in html.lower()


def test_morning_publication_csv_has_six_operational_checks():
    csv_path = REPO / 'publications' / DATE / f'{SLUG}.csv'
    rows = list(csv.DictReader(csv_path.open(encoding='utf-8')))
    assert len(rows) == 6
    assert rows[0]['check'] == 'Frequency is visible'
    assert rows[-1]['check'] == 'Customer impact is reversible'
    assert all(row['owner_question'] and row['safe_action'] for row in rows)


def test_morning_publication_is_discoverable_from_home_llms_and_sitemap():
    home = (REPO / 'index.html').read_text(encoding='utf-8')
    llms = (REPO / 'llms.txt').read_text(encoding='utf-8')
    sitemap = (REPO / 'sitemap.xml').read_text(encoding='utf-8')
    path = f'/publications/{DATE}/{SLUG}.html'
    url = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
    assert path in home
    assert url in llms
    assert url in sitemap
