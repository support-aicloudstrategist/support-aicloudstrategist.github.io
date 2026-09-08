from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "publications" / "2026-09-08" / "ai-agent-cost-spike-triage.html"
MD = ROOT / "publications" / "2026-09-08" / "ai-agent-cost-spike-triage.md"


def test_ai_agent_cost_spike_publication_has_revenue_bridge_without_overclaiming():
    html = PAGE.read_text(encoding="utf-8")
    assert "id='cost-spike-diagnostic-bridge'" in html
    assert "When this should become a paid diagnostic" in html
    assert "bounded AI cost evidence review" in html
    assert "/pricing#fixed-scope-diagnostics" in html
    assert "/free-business-review/?package=ai-agent-cost-spike-triage&amp;source=publication-2026-09-08" in html
    assert "ai-agent-cost-spike-triage.csv" in html
    for boundary in [
        "no credentials",
        "customer data",
        "production changes",
        "savings promise",
        "ROI claim",
        "legal advice",
        "security certification",
        "vendor approval claim",
    ]:
        assert boundary in html


def test_ai_agent_cost_spike_markdown_crosspost_has_same_commercial_path():
    md = MD.read_text(encoding="utf-8")
    assert "When this should become a paid diagnostic" in md
    assert "https://aicloudstrategist.com/free-business-review/?package=ai-agent-cost-spike-triage&source=publication-2026-09-08" in md
    assert "https://aicloudstrategist.com/pricing#fixed-scope-diagnostics" in md
