import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "industries" / "manufacturing-exporters" / "index.html"
URL = "https://aicloudstrategist.com/industries/manufacturing-exporters/"
REL = "/industries/manufacturing-exporters/"


def json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_has_indexable_canonical_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert '<link rel="canonical" href="https://aicloudstrategist.com/industries/manufacturing-exporters/">' in html
    assert "noindex" not in html.lower()
    docs = json_ld_documents(html)
    graph = docs[0]["@graph"]
    assert any(node.get("@type") == "WebPage" and node.get("url") == URL for node in graph)
    assert any(node.get("@type") == "Service" and "Manufacturing" in node.get("name", "") for node in graph)


def test_page_maps_revenue_ready_services_and_resources():
    html = PAGE.read_text(encoding="utf-8")
    required_links = [
        "/services/workflow-automation/",
        "/services/crm-automation/",
        "/services/website-digital-presence/",
        "/services/ai-automation/",
        "/resources/global-manufacturing-production-follow-up-excel-evidence-checklist/",
        "/resources/customer-problem-search/factory-manual-work-reduce/",
    ]
    for link in required_links:
        assert link in html
    assert "No fake factory case studies" in html
    assert "does not claim client results" in html


def test_discoverability_links_are_updated():
    assert REL in (ROOT / "industries" / "index.html").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
