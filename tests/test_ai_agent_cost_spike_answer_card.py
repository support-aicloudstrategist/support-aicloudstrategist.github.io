import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "publications" / "2026-09-08" / "ai-agent-cost-spike-answer-card.json"
PAGE = ROOT / "publications" / "2026-09-08" / "ai-agent-cost-spike-triage.html"
DAY_INDEX = ROOT / "publications" / "2026-09-08" / "index.html"
MD = ROOT / "publications" / "2026-09-08" / "ai-agent-cost-spike-triage.md"
LLMS = ROOT / "llms.txt"


def test_ai_agent_cost_spike_answer_card_is_buyer_safe_and_routeable():
    data = json.loads(CARD.read_text(encoding="utf-8"))
    assert data["primary_buyer_question"].startswith("What should we check")
    assert "no-credentials" in data["safe_answer"]
    assert data["route_to"].endswith("source=answer-card")
    assert data["pricing_context"] == "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics"
    assert data["downloadable_worksheet"].endswith("ai-agent-cost-spike-triage.csv")
    boundaries = " ".join(data["claim_boundaries"])
    for phrase in [
        "No credentials",
        "customer data",
        "No savings",
        "ROI",
        "Not a customer case study",
    ]:
        assert phrase in boundaries


def test_ai_agent_cost_spike_answer_card_is_discoverable():
    rel = "ai-agent-cost-spike-answer-card.json"
    abs_url = "https://aicloudstrategist.com/publications/2026-09-08/" + rel
    assert rel in PAGE.read_text(encoding="utf-8")
    assert rel in DAY_INDEX.read_text(encoding="utf-8")
    assert abs_url in (ROOT / "publications" / "2026-09-08" / "manifest.json").read_text(encoding="utf-8")
    assert abs_url in MD.read_text(encoding="utf-8")
    assert abs_url in LLMS.read_text(encoding="utf-8")
