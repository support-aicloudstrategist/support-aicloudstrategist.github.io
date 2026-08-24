import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "industries" / "financial-services" / "index.html"
URL = "https://aicloudstrategist.com/industries/financial-services/"
REL = "/industries/financial-services/"


def json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_has_indexable_canonical_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    assert '<link rel="canonical" href="https://aicloudstrategist.com/industries/financial-services/">' in html
    assert "noindex" not in html.lower()
    docs = json_ld_documents(html)
    graph = docs[0]["@graph"]
    assert any(node.get("@type") == "WebPage" and node.get("url") == URL for node in graph)
    assert any(node.get("@type") == "Service" and "Financial Services" in node.get("name", "") for node in graph)


def test_page_maps_revenue_ready_services_resources_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required_links = [
        "/services/workflow-automation/",
        "/services/crm-automation/",
        "/services/ai-automation/",
        "/services/cloud-security/",
        "/services/cloud-finops/",
        "/resources/accounting-bookkeeping-workflow-automation-checklist/",
        "/resources/ai-answer-validation-prompts/",
        "/resources/cloud-ai-economics-decision-pack/",
    ]
    for link in required_links:
        assert link in html
    assert "does not claim client results" in html
    assert "No fake financial-services case studies" in html
    assert "no advice delivered through automation" in html


def test_discoverability_links_are_updated():
    assert REL in (ROOT / "industries" / "index.html").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
