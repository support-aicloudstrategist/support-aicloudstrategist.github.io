import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing" / "index.html"
PRICING_FLAT = ROOT / "pricing.html"
PUBLICATION = "/publications/2026-09-09/saas-security-questionnaire-evidence-pack.html"
CSV = "/publications/2026-09-09/saas-security-questionnaire-evidence-pack.csv"
CONTACT = "/free-business-review/?package=saas-security-questionnaire-evidence-pack&amp;source=pricing-fixed-scope"


def _fixed_scope_section(html: str) -> str:
    return html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split(
        '<section class="section"><div class="container faq">', 1
    )[0]


def _item_list(html: str) -> dict:
    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing fixed-scope ItemList JSON-LD missing"
    return json.loads(match.group(1))


def test_pricing_and_pricing_index_are_synced_for_latest_saas_security_offer():
    html = PRICING.read_text(encoding="utf-8")
    flat = PRICING_FLAT.read_text(encoding="utf-8")
    assert html == flat

    section = _fixed_scope_section(html)
    assert 'data-revenue-bridge="saas-security-questionnaire-evidence-pack"' in section
    assert "SaaS security questionnaire evidence pack diagnostic bridge" in section
    assert "Scope before AI questionnaire-answering software, GRC trust-centre tooling" in section
    assert "approved answer sources, proof links, owner review" in section
    assert PUBLICATION in section
    assert CSV in section
    assert CONTACT in section
    assert "no SaaS customer, prospect data, security questionnaire export" in section
    assert "win-rate, revenue, savings, ROI or AI-accuracy claim" in section
    assert "trusted by" not in section.lower()


def test_pricing_jsonld_exposes_saas_security_evidence_pack_without_outcome_claims():
    data = _item_list(PRICING.read_text(encoding="utf-8"))
    items = data["itemListElement"]
    assert data["numberOfItems"] == len(items)
    offer = next(item for item in items if item["url"].endswith("saas-security-questionnaire-evidence-pack.html"))
    text = json.dumps(offer, ensure_ascii=False)
    assert "SaaS security questionnaire evidence pack diagnostic" in text
    assert "sales-engineering backlog" in text
    assert "no SaaS customer" in text
    assert "faster deal" in text
    assert "AI-accuracy claim" in text
