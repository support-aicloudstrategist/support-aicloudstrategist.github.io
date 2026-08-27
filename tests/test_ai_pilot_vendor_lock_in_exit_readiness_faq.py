from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-pilot-vendor-lock-in-exit-readiness-faq"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_blocks(html: str):
    pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
    return [json.loads(match.group(1)) for match in pattern.finditer(html)]


def test_ai_pilot_vendor_lock_in_page_has_search_intent_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI pilot vendor lock-in FAQ" in html
    assert "data export" in html
    assert "model portability" in html
    assert "prompt" in html
    assert "fallback" in html
    assert "production approval" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert "switching guarantee" in html
    assert URL in html


def test_ai_pilot_vendor_lock_in_structured_data_and_discovery():
    html = PAGE.read_text(encoding="utf-8")
    blocks = json_ld_blocks(html)
    assert any(block.get("@type") == "BreadcrumbList" for block in blocks)
    graph = next(block["@graph"] for block in blocks if "@graph" in block)
    article = next(item for item in graph if item.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert any("AI pilot vendor lock-in" in topic for topic in article["about"])
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert URL in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
    assert URL in sitemap


def test_ai_pilot_vendor_lock_in_internal_links_are_existing_targets():
    html = PAGE.read_text(encoding="utf-8")
    for href in [
        "/resources/global-ai-pilot-data-residency-subprocessor-evidence-checklist/",
        "/resources/global-ai-vendor-security-questionnaire-answer-source-map/",
        "/resources/global-ai-pilot-production-go-no-go-decision-record-template/",
        "/resources/global-ai-pilot-rollback-readiness-checklist/",
        "/resources/global-ai-pilot-external-claim-approval-log-template/",
        "/services/cloud-security/",
    ]:
        assert href in html
        target = ROOT / href.strip("/") / "index.html"
        assert target.exists(), href
