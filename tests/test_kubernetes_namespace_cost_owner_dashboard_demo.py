from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/kubernetes-namespace-cost-owner-dashboard-demo/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "kubernetes-namespace-cost-owner-dashboard-demo" / "index.html"
CSV = PAGE.parent / "kubernetes-namespace-cost-owner-dashboard-demo.csv"
SVG = PAGE.parent / "kubernetes-namespace-cost-owner-dashboard-demo.svg"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_kubernetes_namespace_dashboard_demo_has_seo_schema_and_assets():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 3
    for marker in [
        "Kubernetes namespace cost allocation dashboard",
        "namespace chargeback owner dashboard",
        "pod rightsizing approval",
        "idle cluster review",
        "GPU waste FinOps dashboard",
        "cloud cost owner dashboard",
        "proof-before-platform",
        "kubernetes-namespace-cost-owner-dashboard-demo.csv",
        "kubernetes-namespace-cost-owner-dashboard-demo.svg",
        '"@type":"Dataset"',
    ]:
        assert marker in source
    assert CSV.is_file()
    assert SVG.is_file()


def test_kubernetes_namespace_dashboard_demo_has_truth_boundaries():
    source = html()
    for marker in [
        "synthetic demo",
        "not a real client case study",
        "not production workload data",
        "not cloud account data",
        "not a testimonial",
        "not a certification",
        "not proof of savings",
        "not ROI evidence",
        "not ranking evidence",
        "not a guarantee of lower Kubernetes cost",
        "No outreach was sent",
        "no readable aicloudstrategist.com result marker",
    ]:
        assert marker in source


def test_kubernetes_namespace_dashboard_demo_csv_is_safe_and_useful():
    rows = list(csv.DictReader(CSV.read_text(encoding="utf-8").splitlines()))
    assert len(rows) >= 5
    expected = {
        "cluster",
        "namespace",
        "environment",
        "business_owner",
        "monthly_cost_band",
        "cost_trend",
        "utilization_signal",
        "recommended_action",
        "approval_owner",
        "risk_boundary",
        "next_review_date",
        "proof_boundary",
    }
    assert expected.issubset(rows[0].keys())
    assert all(row["proof_boundary"] == "Synthetic demo row only" for row in rows)


def test_kubernetes_namespace_dashboard_demo_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
