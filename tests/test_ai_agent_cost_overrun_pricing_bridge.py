import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_FILES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "/resources/global-ai-agent-cost-overrun-owner-evidence-checklist/"
CSV = RESOURCE + "ai-agent-cost-overrun-owner-evidence.csv"
CONTACT = "/contact.html?service=enterprise-ai&amp;stage=diagnostic&amp;source=pricing-ai-agent-cost-overrun"


def _fixed_scope_section(html: str) -> str:
    start = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1]
    if '<section class="section pricing-showcase">' in start:
        return start.split('<section class="section pricing-showcase">', 1)[0]
    return start.split('<section class="section"><div class="container faq">', 1)[0]


def test_ai_agent_cost_overrun_bridge_visible_on_both_pricing_routes():
    for path in PRICING_FILES:
        section = _fixed_scope_section(path.read_text(encoding="utf-8"))
        assert 'data-revenue-bridge="global-ai-agent-cost-overrun-owner-evidence"' in section
        assert "AI agent cost overrun owner-evidence diagnostic bridge" in section
        assert "Scope before LLM budget increases, agent-platform expansion" in section
        assert "budget owner" in section
        assert "pause rules" in section
        assert RESOURCE in section
        assert CSV in section
        assert CONTACT in section


def test_ai_agent_cost_overrun_bridge_keeps_truth_boundaries_and_schema_count():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    section = _fixed_scope_section(html)
    card = section.split('data-revenue-bridge="global-ai-agent-cost-overrun-owner-evidence"', 1)[1].split("</aside>", 1)[0]
    for boundary in [
        "no real customer",
        "model provider",
        "invoice",
        "token log",
        "prompt",
        "credential",
        "production access",
        "savings, ROI, cost reduction",
        "demand, lead, customer, revenue",
        "AI-accuracy claim",
    ]:
        assert boundary in card

    match = re.search(
        r'<script type="application/ld\+json">({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})</script>',
        html,
    )
    assert match, "pricing fixed-scope ItemList JSON-LD missing"
    data = json.loads(match.group(1))
    assert data["numberOfItems"] == len(data["itemListElement"])
    assert any(item["url"].endswith(RESOURCE) for item in data["itemListElement"])
