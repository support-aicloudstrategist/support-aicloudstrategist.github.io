from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "cloud-finops" / "index.html"


def test_cloud_finops_service_surfaces_public_revenue_entry_paths():
    html = PAGE.read_text(encoding="utf-8")
    section = html.split('id="engagement"', 1)[1].split('id="procurement"', 1)[0]

    assert 'data-finops-revenue-bridge="cloud-finops-public-entry-paths"' in section
    assert "Azure bill too high owner-action diagnostic" in section
    assert "/resources/azure-bill-too-high-owner-action-checklist/" in section
    assert "/free-business-review/?package=azure-bill-too-high-owner-action-checklist&amp;source=cloud-finops-service" in section
    assert "AI cost anomaly approval diagnostic" in section
    assert "/resources/global-enterprise-ai-cost-anomaly-approval-runbook/" in section
    assert "/free-business-review/?package=global-enterprise-ai-cost-anomaly-approval-runbook&amp;source=cloud-finops-service" in section


def test_cloud_finops_public_entry_paths_keep_claim_boundaries_clear():
    html = PAGE.read_text(encoding="utf-8")
    section = html.split('data-finops-revenue-bridge="cloud-finops-public-entry-paths"', 1)[1].split('id="procurement"', 1)[0]

    for boundary in [
        "no Azure credentials",
        "billing-console access",
        "invoices",
        "production logs",
        "tenant access",
        "customer data",
        "cloud secrets",
        "not savings evidence",
        "ROI evidence",
        "ranking evidence",
        "Microsoft partnership proof",
        "vendor partnership proof",
        "cost-reduction claim",
    ]:
        assert boundary in section
