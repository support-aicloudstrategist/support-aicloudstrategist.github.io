from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "47-cloud-cost-checks-before-finops-consultant" / "index.html"


def page_text():
    return PAGE.read_text(encoding="utf-8")


def test_cloud_cost_checklist_has_fixed_scope_revenue_bridge():
    text = page_text()
    assert 'data-revenue-bridge="cloud-cost-checklist-fixed-scope-diagnostic"' in text
    assert "/free-business-review/?package=cloud-cost-checklist-owner-review" in text
    assert "/pricing.html#fixed-scope-diagnostics" in text
    assert "/services/cloud-finops/" in text
    assert "fixed-scope diagnostic" in text
    assert "FinOps consultant, platform, commitment or migration spend" in text


def test_cloud_cost_checklist_bridge_preserves_safety_boundaries():
    text = page_text()
    required = [
        "no-credentials diagnostic",
        "read-only, redacted review",
        "no production changes",
        "credentials",
        "savings promises",
        "compliance proof",
        "architecture advice",
        "No guaranteed savings claim before review",
    ]
    for marker in required:
        assert marker in text


def test_cloud_cost_owner_artifacts_remain_linked():
    text = page_text()
    assert "cloud-cost-owner-review-checklist.csv" in text
    assert "cloud-cost-owner-board.svg" in text
    assert (PAGE.parent / "cloud-cost-owner-review-checklist.csv").exists()
    assert (PAGE.parent / "cloud-cost-owner-board.svg").exists()
