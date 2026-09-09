import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_FILES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/"
CSV = RESOURCE + "clinic-after-hours-missed-call-ai-answer-bank.csv"
CONTACT = "/free-business-review/?package=clinic-after-hours-missed-call-evidence&amp;source=pricing-fixed-scope"


def _fixed_scope_section(html: str) -> str:
    start = html.split('<section class="section" id="fixed-scope-diagnostics">', 1)[1]
    return start.split('<section class="section"><div class="container faq">', 1)[0]


def test_clinic_after_hours_bridge_visible_on_both_pricing_routes():
    for path in PRICING_FILES:
        section = _fixed_scope_section(path.read_text(encoding="utf-8"))
        assert 'data-revenue-bridge="global-clinic-after-hours-missed-call-follow-up"' in section
        assert "Clinic after-hours missed-call follow-up diagnostic bridge" in section
        assert "Scope before clinic AI receptionist, call-centre, WhatsApp follow-up" in section
        assert "callback queue" in section
        assert "owner dashboard" in section
        assert RESOURCE in section
        assert CSV in section
        assert CONTACT in section


def test_clinic_after_hours_bridge_keeps_truth_boundaries_and_schema_count():
    html = (ROOT / "pricing.html").read_text(encoding="utf-8")
    section = _fixed_scope_section(html)
    card = section.split('data-revenue-bridge="global-clinic-after-hours-missed-call-follow-up"', 1)[1].split("</aside>", 1)[0]
    for boundary in [
        "no real clinic",
        "patient data",
        "call recording",
        "WhatsApp transcript",
        "credential",
        "production access",
        "legal/privacy/security/medical advice",
        "ranking, demand, lead",
        "booked appointment",
        "revenue, savings, ROI",
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
