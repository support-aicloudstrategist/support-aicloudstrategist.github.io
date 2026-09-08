from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-agent-cost-overrun-owner-evidence-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-agent-cost-overrun-owner-evidence.csv"


def test_ai_agent_cost_overrun_asset_has_discovery_and_schema():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert source.count('<script type="application/ld+json">') >= 4
    for marker in [
        "AI Agent Cost Overrun Owner Evidence Checklist",
        "AI agent cost overrun",
        "LLM spend spikes",
        "token budget ownership",
        "approval gates",
        "pause rules",
        "Comparison matrix before spend",
        "AICS owner-evidence review",
        "Request AI cost diagnostic scope",
        "Download synthetic evidence CSV",
        "Truth boundary",
    ]:
        assert marker in source


def test_ai_agent_cost_overrun_asset_keeps_claim_boundaries_clear():
    source = PAGE.read_text(encoding="utf-8")
    for boundary in [
        "synthetic buyer-education checklist",
        "not a real client case study",
        "not customer usage data",
        "not cloud account data",
        "not LLM provider data",
        "not invoice data",
        "not production log data",
        "not security advice",
        "not legal advice",
        "not procurement advice",
        "not savings evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real customer, prospect, buyer, model provider, platform partner, invoice, token log, prompt, credential, architecture, testimonial, certification, partnership, customer outcome, ranking, demand, lead, customer, revenue, savings, ROI, cost reduction, uptime or AI-accuracy claim is made",
    ]:
        assert boundary in source


def test_ai_agent_cost_overrun_asset_is_routed_to_index_llms_and_sitemap():
    csv = CSV.read_text(encoding="utf-8")
    assert "Workflow purpose" in csv
    assert "No customer result revenue savings ROI or productivity claim" in csv
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "ai-agent-cost-overrun-owner-evidence.csv" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "ai-agent-cost-overrun-owner-evidence.csv" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{REL}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
