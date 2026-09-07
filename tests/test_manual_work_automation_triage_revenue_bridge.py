from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PUBLICATION_PATH = "/publications/2026-09-07/manual-work-automation-triage.html"
CSV_PATH = "/publications/2026-09-07/manual-work-automation-triage.csv"


def test_resources_hub_surfaces_manual_work_triage_asset_near_featured_publication():
    html = (REPO / "resources" / "index.html").read_text(encoding="utf-8")

    assert 'data-featured-publication="ai-reply-readiness-checkpoints"' in html
    assert 'data-resource-card="manual-work-automation-triage"' in html
    assert PUBLICATION_PATH in html
    assert CSV_PATH in html
    assert "/pricing#fixed-scope-diagnostics" in html
    assert "claim boundaries" in html


def test_pricing_has_manual_work_automation_triage_revenue_bridge_without_changing_existing_offer_count():
    html = (REPO / "pricing.html").read_text(encoding="utf-8")

    assert "Thirty-two concrete first offers" in html
    assert 'data-revenue-bridge="manual-work-automation-triage"' in html
    assert "Manual work automation triage diagnostic bridge" in html
    assert PUBLICATION_PATH in html
    assert CSV_PATH in html
    assert "manual-work-automation-triage-diagnostic" in html
    for boundary in [
        "no customer data",
        "credentials",
        "production access",
        "savings, revenue, ROI or automation-performance claim",
    ]:
        assert boundary in html
