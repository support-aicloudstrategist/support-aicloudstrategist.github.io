import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"


class ScriptCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_json_ld = False
        self.scripts = []
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self.in_json_ld = True
            self._buf = []

    def handle_data(self, data):
        if self.in_json_ld:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json_ld:
            self.scripts.append("".join(self._buf))
            self.in_json_ld = False


def test_pricing_surfaces_healthtech_questionnaire_owner_handoff_offer():
    html = PRICING.read_text(encoding="utf-8")
    assert "Seventeen concrete first offers" in html
    assert "North America healthtech AI procurement questionnaire owner handoff" in html
    assert "/resources/north-america-healthtech-ai-procurement-questionnaire-owner-handoff/" in html
    assert "PHI/ePHI, BAA, SOC 2, HITRUST, AI data-use" in html
    assert "no compliance, audit, procurement, ranking, revenue or ROI claims" in html
    section = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1].split('<section class="section pricing-showcase">', 1)[0]
    assert len(re.findall(r'<article class="card"><h3>', section)) == 17


def test_pricing_json_ld_includes_15_fixed_scope_diagnostics():
    parser = ScriptCollector()
    parser.feed(PRICING.read_text(encoding="utf-8"))
    item_lists = [json.loads(script) for script in parser.scripts if 'pricing#fixed-scope-diagnostics' in script]
    assert len(item_lists) == 1
    item_list = item_lists[0]
    assert item_list["numberOfItems"] == 17
    assert len(item_list["itemListElement"]) == 17
    last = item_list["itemListElement"][-1]
    assert last["position"] == 17
    assert last["url"] == "https://aicloudstrategist.com/resources/north-america-healthtech-ai-procurement-questionnaire-owner-handoff/"
    assert last["item"]["name"] == "North America healthtech AI procurement questionnaire owner handoff"
