from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/crm-automation-examples-guide/index.html"
RESOURCE_HUB = ROOT / "resources/index.html"
CRM_SERVICE = ROOT / "services/crm-automation/index.html"
SITEMAP_SCRIPT = ROOT / "scripts/build_sitemap.py"
SITEMAP = ROOT / "sitemap.xml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def json_ld_blocks(source: str) -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    return [json.loads(block) for block in blocks]


def test_page_is_indexable_with_single_h1_and_canonical() -> None:
    html = read(PAGE)
    assert '<meta name="robots" content="index, follow' in html
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/crm-automation-examples-guide/"' in html
    assert len(re.findall(r"<h1\b", html, re.I)) == 1
    assert "CRM automation examples for service businesses" in html


def test_structured_data_article_and_faq_are_parseable() -> None:
    graph = json_ld_blocks(read(PAGE))[0]["@graph"]
    types = {node.get("@type") for node in graph}
    assert {"Organization", "WebPage", "Article", "FAQPage"}.issubset(types)
    article = next(node for node in graph if node.get("@type") == "Article")
    assert article["mainEntityOfPage"] == "https://aicloudstrategist.com/resources/crm-automation-examples-guide/"
    faq = next(node for node in graph if node.get("@type") == "FAQPage")
    assert "guaranteed revenue" in faq["mainEntity"][1]["acceptedAnswer"]["text"]


def test_buyer_language_and_truth_boundary() -> None:
    html = read(PAGE).lower()
    for phrase in [
        "missed-call to callback queue",
        "whatsapp enquiry capture",
        "appointment no-show recovery",
        "quote follow-up pipeline",
        "human-review flag",
        "not a customer case study",
        "does not claim clients, revenue uplift, conversion improvement, compliance approval, software ranking or guaranteed roi",
    ]:
        assert phrase in html


def test_internal_discovery_wiring() -> None:
    url = "/resources/crm-automation-examples-guide/"
    assert url in read(RESOURCE_HUB)
    assert url in read(CRM_SERVICE)
    assert '"/resources/crm-automation-examples-guide/"' in read(SITEMAP_SCRIPT)
    assert "https://aicloudstrategist.com/resources/crm-automation-examples-guide/" in read(SITEMAP)
