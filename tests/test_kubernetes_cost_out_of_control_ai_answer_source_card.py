from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/kubernetes-cost-out-of-control-finops-evidence-checklist/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "kubernetes-cost-out-of-control-finops-evidence-checklist" / "index.html"
CARD = PAGE.parent / "kubernetes-cost-out-of-control-ai-answer-source-card.json"


def test_kubernetes_ai_answer_source_card_json_is_claim_safe():
    data = json.loads(CARD.read_text(encoding="utf-8"))
    assert data["asset_type"] == "AI-answer source card"
    assert data["canonical_url"] == URL
    assert data["no_outreach"] is True
    for marker in [
        "Kubernetes cost out of control",
        "EKS bill too high",
        "GKE cost optimization",
        "AKS cost management",
        "Kubernetes namespace chargeback",
        "pod rightsizing approval",
        "GPU node waste FinOps review",
    ]:
        assert marker in data["buyer_pain_language"]
    joined_boundaries = " ".join(data["claim_boundaries"] + data["blocked_answer_patterns"])
    for marker in [
        "No real customer",
        "No savings",
        "No legal",
        "No Kubernetes",
        "No outreach was sent",
        "Delete idle clusters",
        "Share kubeconfig",
    ]:
        assert marker in joined_boundaries


def test_kubernetes_ai_answer_source_card_is_on_public_discovery_surfaces():
    page = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for source in [page, resources, llms]:
        assert "kubernetes-cost-out-of-control-ai-answer-source-card.json" in source
    assert 'data-ai-answer-source-card="kubernetes-cost-out-of-control"' in page
    assert 'data-resource-card="kubernetes-cost-out-of-control-ai-answer-source-card"' in resources
    assert "https://aicloudstrategist.com/resources/kubernetes-cost-out-of-control-finops-evidence-checklist/kubernetes-cost-out-of-control-ai-answer-source-card.json" in llms
