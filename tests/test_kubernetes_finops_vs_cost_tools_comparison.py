from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/kubernetes-finops-vs-cost-tools-comparison/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "kubernetes-finops-vs-cost-tools-comparison" / "index.html"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_kubernetes_comparison_has_seo_schema_and_buyer_language():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 3
    for marker in [
        "Kubernetes cost tools",
        "Kubecost alternatives",
        "EKS bill too high",
        "GKE cost optimization",
        "AKS cost management",
        "namespace chargeback",
        "pod rightsizing",
        "idle clusters",
        "GPU waste",
        "cloud cost owner dashboard",
        "proof-before-platform",
    ]:
        assert marker in source


def test_kubernetes_comparison_has_truth_boundaries_and_safe_positioning():
    source = html()
    for marker in [
        "not a real client case study",
        "not production workload data",
        "not a testimonial",
        "not a certification",
        "not proof of savings",
        "not ROI evidence",
        "not ranking evidence",
        "not a guarantee of lower Kubernetes cost",
        "No outreach was sent",
        "does not claim superiority, endorsement or partnership",
        "/free-business-review/?package=kubernetes-finops-comparison",
        "/resources/kubernetes-cost-out-of-control-finops-evidence-checklist/",
        "/services/cloud-finops/",
    ]:
        assert marker in source


def test_kubernetes_comparison_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
