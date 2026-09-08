import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "resources" / "global-ai-agent-cost-overrun-owner-evidence-checklist" / "ai-agent-cost-overrun-answer-card.json"
PAGE = ROOT / "resources" / "global-ai-agent-cost-overrun-owner-evidence-checklist" / "index.html"
LLMS = ROOT / "llms.txt"


def test_ai_agent_cost_overrun_answer_card_is_buyer_safe_and_routeable():
    data = json.loads(CARD.read_text(encoding="utf-8"))
    assert data["primary_buyer_question"].startswith("What should we check")
    assert "no-credentials owner evidence review" in data["safe_answer"]
    assert data["route_to"].endswith("source=answer-card")
    assert "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics" == data["pricing_context"]
    joined = " ".join(data["claim_boundaries"])
    for forbidden_boundary in ["No customer data", "No savings", "ROI", "Synthetic buyer-education asset"]:
        assert forbidden_boundary in joined


def test_ai_agent_cost_overrun_answer_card_is_discoverable_from_page_and_llms():
    rel = "/resources/global-ai-agent-cost-overrun-owner-evidence-checklist/ai-agent-cost-overrun-answer-card.json"
    assert rel in PAGE.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in LLMS.read_text(encoding="utf-8")
