from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def test_law_firm_industry_page_is_indexable_and_safety_bounded():
    html = (ROOT / "industries" / "law-firms" / "index.html").read_text(encoding="utf-8")

    assert '<link rel="canonical" href="https://aicloudstrategist.com/industries/law-firms/">' in html
    assert re.search(r"<h1>[^<]*law firms", html, re.I)
    assert "No attorney-client relationship by bot" in html
    assert "This page does not claim legal outcomes, clients or attorney approval" in html
    assert "/services/us-law-firm-ai-intake-answering-service/" in html
    assert "/resources/global-law-firm-missed-call-client-intake-follow-up-checklist/" in html
    assert "/resources/us-law-firm-ai-intake-answering-service-faq/" in html

    for payload in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        json.loads(payload)


def test_law_firm_industry_page_is_discoverable_from_hub_and_sitemap():
    hub = (ROOT / "industries" / "index.html").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert "/industries/law-firms/" in hub
    assert "https://aicloudstrategist.com/industries/law-firms/" in sitemap
