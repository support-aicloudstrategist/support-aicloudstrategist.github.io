from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/global-manufacturing-production-follow-up-excel-evidence-checklist/index.html"


def page_text():
    return PAGE.read_text(encoding="utf-8")


def test_manufacturing_asset_is_indexable_and_canonical():
    html = page_text()
    assert '<meta name="robots" content="index, follow"' in html
    assert 'https://aicloudstrategist.com/resources/global-manufacturing-production-follow-up-excel-evidence-checklist/' in html
    assert html.count('<h1>') == 1
    assert html.count('application/ld+json') >= 4


def test_manufacturing_asset_has_buyer_language_and_boundaries():
    html = page_text().lower()
    required = [
        'factory production follow up excel owner dashboard',
        'manufacturing order tracking whatsapp quotation follow up',
        'erp',
        'mrp',
        'crm',
        'whatsapp-to-system',
        'dispatch promise evidence',
        'human-review boundaries',
        'not a real manufacturer case study',
        'not proof of faster production',
        'no real manufacturer',
        'no outreach',
    ]
    missing = [item for item in required if item not in html]
    assert missing == []


def test_manufacturing_asset_is_linked_from_discovery_surfaces():
    route = '/resources/global-manufacturing-production-follow-up-excel-evidence-checklist/'
    assert route in (ROOT / 'resources/index.html').read_text(encoding='utf-8')
    assert route in (ROOT / 'llms.txt').read_text(encoding='utf-8')
    assert f'https://aicloudstrategist.com{route}' in (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
