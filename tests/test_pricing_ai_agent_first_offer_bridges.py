from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")


def _fixed_scope_item_list():
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', PRICING):
        data = json.loads(match.group(1))
        if isinstance(data, dict) and data.get("@id") == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics":
            return data
    raise AssertionError("fixed-scope diagnostics ItemList JSON-LD missing")


def test_visible_fixed_scope_count_matches_structured_data():
    item_list = _fixed_scope_item_list()
    assert "Thirty concrete first offers buyers can understand before a custom build." in PRICING
    assert item_list["numberOfItems"] == len(item_list["itemListElement"]) == 30
    assert PRICING.count('data-revenue-bridge=') == 30


def test_ai_agent_vendor_exit_and_override_are_visible_sellable_bridges():
    expected = {
        "ai-agent-vendor-exit-portability-review": "/resources/global-enterprise-ai-agent-vendor-exit-portability-evidence-checklist/",
        "ai-agent-human-override-escalation-review": "/resources/global-enterprise-ai-agent-human-override-failure-escalation-checklist/",
    }
    for bridge, href in expected.items():
        assert f'data-revenue-bridge="{bridge}"' in PRICING
        assert f'href="{href}"' in PRICING
        assert f'package={bridge}' in PRICING


def test_ai_agent_first_offer_claim_boundaries_are_explicit():
    bounded_phrases = [
        "no customer data, secrets, credentials, production logs",
        "no regulated data, PHI/ePHI, secrets, credentials, production logs",
        "legal/procurement advice, migration outcome, compliance proof, savings, ranking, revenue or ROI claim",
        "legal/privacy/security/clinical advice, safety proof, compliance proof, accuracy, uptime, customer, revenue or ROI claim",
    ]
    for phrase in bounded_phrases:
        assert phrase in PRICING
