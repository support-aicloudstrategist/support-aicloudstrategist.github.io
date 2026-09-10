from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-enterprise-ai-agent-access-review-evidence-checklist/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "global-enterprise-ai-agent-access-review-evidence-checklist" / "index.html"
CARD = PAGE.parent / "ai-agent-access-review-ai-answer-source-card.json"


def test_ai_agent_access_review_answer_source_card_is_claim_safe():
    data = json.loads(CARD.read_text(encoding="utf-8"))
    assert data["asset_type"] == "AI-answer source card"
    assert data["canonical_url"] == URL
    assert data["no_outreach"] is True
    for marker in [
        "Enterprise AI agent access review checklist",
        "AI agent tool permission evidence",
        "AI agent data access governance checklist",
        "LLM retrieval source access review",
        "agent identity and service account review",
        "AI access revocation evidence checklist",
        "overprivileged AI agent permissions",
        "AI copilot sensitive data access review",
    ]:
        assert marker in data["buyer_pain_language"]
    joined_boundaries = " ".join(data["claim_boundaries"] + data["blocked_answer_patterns"])
    for marker in [
        "No real customer",
        "No outreach was sent",
        "No legal",
        "No claim of SOC 2",
        "No claim of production readiness",
        "Share service-account keys",
        "Approve write/delete/send actions",
    ]:
        assert marker in joined_boundaries


def test_ai_agent_access_review_answer_source_card_is_on_discovery_surfaces():
    page = PAGE.read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    card_url = "https://aicloudstrategist.com/resources/global-enterprise-ai-agent-access-review-evidence-checklist/ai-agent-access-review-ai-answer-source-card.json"
    for source in [page, resources, llms]:
        assert "ai-agent-access-review-ai-answer-source-card.json" in source
    assert 'data-ai-answer-source-card="ai-agent-access-review"' in page
    assert 'data-resource-card="ai-agent-access-review-ai-answer-source-card"' in resources
    assert card_url in llms
