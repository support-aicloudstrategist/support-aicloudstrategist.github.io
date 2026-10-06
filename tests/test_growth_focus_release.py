from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]

def test_priority_pages_have_unique_metadata_and_one_h1():
    from bs4 import BeautifulSoup
    files=[ROOT/'index.html',ROOT/'pricing/index.html',ROOT/'free-business-review/index.html',ROOT/'services/production-ai-readiness/index.html',ROOT/'services/cloud-ai-economics/index.html']
    titles=[];descriptions=[];canonicals=[]
    for file in files:
        soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
        assert len(soup.find_all('h1'))==1,file
        description=soup.select_one('meta[name=description]');canonical=soup.select_one('link[rel=canonical]')
        assert soup.title and description and canonical
        titles.append(soup.title.get_text(strip=True));descriptions.append(description['content']);canonicals.append(canonical['href'])
    assert len(set(titles))==len(titles)
    assert len(set(descriptions))==len(descriptions)
    assert len(set(canonicals))==len(canonicals)

def test_sitemap_is_curated_canonical_host_only():
    tree=ET.parse(ROOT/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[node.text for node in tree.findall('s:url/s:loc',ns)]
    assert 10 <= len(urls) <= 600
    assert len(urls)==len(set(urls))
    assert all(url.startswith('https://aicloudstrategist.com/') for url in urls)
    assert not any('github.io' in url for url in urls)
    assert 'https://aicloudstrategist.com/services/production-ai-readiness/' in urls
    assert 'https://aicloudstrategist.com/services/cloud-ai-economics/' in urls
    assert not any('/ai-automation-agency-' in url for url in urls)

def test_analytics_collector_is_non_pii_allowlisted():
    source=(ROOT/'functions/api/events.ts').read_text(encoding='utf-8')
    for forbidden in ('email','phone','message','full_name','whatsapp_number'):
        assert f'"{forbidden}"' not in source
    assert 'non_pii_allowlist_v1' in source

def test_broken_linkedin_entity_url_removed_from_priority_pages():
    for path in ('index.html','about/index.html','terms','privacy'):
        assert 'linkedin.com/company/aicloudstrategist' not in (ROOT/path).read_text(encoding='utf-8')

def test_lead_endpoint_delivers_m365_notification_after_durable_storage():
    source=(ROOT/'functions/api/lead.ts').read_text(encoding='utf-8')
    assert source.index('await context.env.LEAD_LOG.put(leadId') < source.index('await sendLeadEmail(context.env, lead, textBody)')
    assert 'notification_status: "microsoft_365_sent"' not in source
    assert 'notificationStatus = "microsoft_365_sent"' in source
    assert 'notification_configured' in source
