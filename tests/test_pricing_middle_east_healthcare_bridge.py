from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing" / "index.html"


def test_middle_east_bridge_is_visible_and_bounded():
    html = PRICING.read_text(encoding="utf-8")
    assert 'data-revenue-bridge="middle-east-healthcare-growthos-cloud-trust-readiness-map"' in html
    assert "Middle East healthcare AI and cloud trust readiness" in html
    assert "/resources/middle-east-healthcare-growthos-cloud-trust-readiness-map/" in html
    assert "/request-fit-review/" in html
    assert "no patient data, health data, personal data, production access" in html
    assert "compliance proof, ranking, demand, lead, patient outcome, savings, revenue, ROI" in html