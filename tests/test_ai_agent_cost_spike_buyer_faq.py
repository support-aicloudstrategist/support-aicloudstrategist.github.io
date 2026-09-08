from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "publications" / "2026-09-08" / "ai-agent-cost-spike-triage.html"
MD = ROOT / "publications" / "2026-09-08" / "ai-agent-cost-spike-triage.md"


def test_ai_agent_cost_spike_publication_has_buyer_objection_faq():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI agent cost spike buyer FAQ" in html
    assert "FAQPage" in html
    for phrase in [
        "Do I need to share credentials or customer data?",
        "No. The first review can start from bills, run counts, change notes",
        "Does this promise savings or ROI?",
        "No. It creates an evidence-led decision record",
        "When should we ask AICS for help?",
        "before you scale, switch vendors, raise limits or expose production access",
    ]:
        assert phrase in html


def test_ai_agent_cost_spike_markdown_crosspost_has_same_faq():
    md = MD.read_text(encoding="utf-8")
    assert "## AI agent cost spike buyer FAQ" in md
    assert "Do I need to share credentials or customer data?" in md
    assert "Does this promise savings or ROI?" in md
    assert "When should we ask AICS for help?" in md
