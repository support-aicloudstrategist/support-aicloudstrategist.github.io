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


def test_middle_east_readiness_map_has_bounded_commercial_next_step():
    html = (ROOT / "resources" / "middle-east-healthcare-growthos-cloud-trust-readiness-map" / "index.html").read_text(encoding="utf-8")
    assert 'data-revenue-bridge="middle-east-healthcare-readiness-fit-review"' in html
    assert "Want a bounded next step?" in html
    assert "/pricing/" in html
    assert "/request-fit-review/" in html
    assert "without patient data, health data, personal data or production access" in html


def test_manual_work_publication_uses_directory_index_fallback():
    root = ROOT / "publications" / "2026-11-20"
    page = root / "manual-work-automation-readiness-map-live.html" / "index.html"
    assert page.exists()
    assert "Too Much Manual Work? A 5-Check Automation Readiness Map" in page.read_text(encoding="utf-8")
    assert "manual-work-automation-readiness-map-live.html/" in (root / "manual-work-automation-readiness-map-answer-card.json").read_text(encoding="utf-8")
