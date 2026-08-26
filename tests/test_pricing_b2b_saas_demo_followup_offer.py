from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
PAGE = ROOT / "resources" / "global-b2b-saas-demo-security-questionnaire-follow-up-evidence-checklist" / "index.html"
ROUTE = "/resources/global-b2b-saas-demo-security-questionnaire-follow-up-evidence-checklist/"
URL = f"https://aicloudstrategist.com{ROUTE}"


def _fixed_scope_section(html: str) -> str:
    return html.split('id="fixed-scope-diagnostics"', 1)[1].split('<section class="section pricing-showcase"', 1)[0]


def test_pricing_page_surfaces_b2b_saas_demo_followup_as_sellable_offer():
    html = PRICING.read_text(encoding="utf-8")
    section = _fixed_scope_section(html)

    assert "Thirteen concrete first offers buyers can understand before a custom build." in section
    assert "B2B SaaS demo-to-security-questionnaire follow-up diagnostic" in section
    assert ROUTE in section
    assert "stalled demo, pilot, expansion, procurement, vendor-risk" in section
    assert "DPA/MSA, security-questionnaire, AI-use, trust-centre" in section
    assert "deal-desk blocker queues" in section
    assert "no legal, privacy, security, compliance, procurement, ranking, revenue or ROI claims" in section


def test_fixed_scope_diagnostic_count_matches_public_heading():
    html = PRICING.read_text(encoding="utf-8")
    section = _fixed_scope_section(html)
    cards = re.findall(r'<article class="card">', section)

    assert len(cards) == 13


def test_fixed_scope_diagnostics_have_discovery_itemlist_schema():
    html = PRICING.read_text(encoding="utf-8")
    schema_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)
    itemlists = [json.loads(block) for block in schema_blocks if 'pricing#fixed-scope-diagnostics' in block]

    assert len(itemlists) == 1
    itemlist = itemlists[0]
    assert itemlist["@type"] == "ItemList"
    assert itemlist["@id"] == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    assert itemlist["numberOfItems"] == 13
    assert len(itemlist["itemListElement"]) == 13
    first = itemlist["itemListElement"][0]
    assert first["position"] == 1
    assert first["url"] == URL
    assert first["item"]["@type"] == "Service"
    assert first["item"]["offers"]["priceSpecification"]["description"] == "Scope before quote; pass-through costs and implementation work are confirmed separately."


def test_b2b_saas_demo_followup_page_is_public_buyer_safe_and_linked():
    page = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    build_sitemap = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    assert URL in page
    assert "Claim boundaries" in page
    assert "not a real customer case study" in page
    assert "AICS owns the operational gap" in page
    assert "Request the diagnostic fit check" in page
    assert ROUTE in resources
    assert URL in llms
    assert URL in sitemap
    assert ROUTE in build_sitemap
