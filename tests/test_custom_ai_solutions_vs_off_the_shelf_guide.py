from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/custom-ai-solutions-vs-off-the-shelf-ai-tools-guide/index.html"
RESOURCE_HUB = ROOT / "resources/index.html"
AI_AUTOMATION_SERVICE = ROOT / "services/ai-automation/index.html"
SITEMAP_SCRIPT = ROOT / "scripts/build_sitemap.py"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"
ROADMAP = ROOT / "seo/MASTER_SEO_ROADMAP.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def json_ld_graph(source: str) -> list[dict]:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    assert blocks
    return json.loads(blocks[0])["@graph"]


def test_page_is_indexable_with_single_h1_and_canonical() -> None:
    html = read(PAGE)
    assert '<meta name="robots" content="index, follow' in html
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/custom-ai-solutions-vs-off-the-shelf-ai-tools-guide/"' in html
    assert len(re.findall(r"<h1\b", html, re.I)) == 1
    assert "Custom AI solutions vs off-the-shelf AI tools" in html


def test_structured_data_article_and_faq_are_parseable() -> None:
    graph = json_ld_graph(read(PAGE))
    types = {node.get("@type") for node in graph}
    assert {"Organization", "WebPage", "Article", "FAQPage"}.issubset(types)
    article = next(node for node in graph if node.get("@type") == "Article")
    assert article["mainEntityOfPage"] == "https://aicloudstrategist.com/resources/custom-ai-solutions-vs-off-the-shelf-ai-tools-guide/"
    faq = next(node for node in graph if node.get("@type") == "FAQPage")
    faq_text = " ".join(item["acceptedAnswer"]["text"] for item in faq["mainEntity"])
    assert "off-the-shelf AI tool" in faq_text
    assert "Custom AI" in faq_text
    assert "does not claim guaranteed ROI" in faq_text


def test_buyer_language_and_truth_boundary() -> None:
    html = read(PAGE).lower()
    for phrase in [
        "off-the-shelf ai tool",
        "integration-led automation",
        "custom ai solution with controls",
        "process redesign before ai",
        "approval gates",
        "not a customer case study or software ranking",
        "does not claim clients, revenue uplift, cost saving, model accuracy, compliance approval, vendor superiority or guaranteed roi",
    ]:
        assert phrase in html


def test_internal_discovery_wiring_and_tracker() -> None:
    url = "/resources/custom-ai-solutions-vs-off-the-shelf-ai-tools-guide/"
    full_url = f"https://aicloudstrategist.com{url}"
    assert url in read(RESOURCE_HUB)
    assert url in read(AI_AUTOMATION_SERVICE)
    assert f'"{url}"' in read(SITEMAP_SCRIPT)
    assert full_url in read(SITEMAP)
    assert full_url in read(LLMS)
    assert "[x] Custom AI solutions vs off-the-shelf AI tools guide." in read(ROADMAP)
