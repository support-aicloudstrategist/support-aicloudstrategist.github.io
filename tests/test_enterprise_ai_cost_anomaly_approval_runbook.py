from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-enterprise-ai-cost-anomaly-approval-runbook/"
URL = "https://aicloudstrategist.com" + REL
SLUG = "global-enterprise-ai-cost-anomaly-approval-runbook"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_PATH = ROOT / "resources" / SLUG / "ai-cost-anomaly-approval-log-template.csv"
SVG_PATH = ROOT / "resources" / SLUG / "ai-cost-anomaly-approval-flow.svg"
CSV_URL = URL + "ai-cost-anomaly-approval-log-template.csv"
SVG_URL = URL + "ai-cost-anomaly-approval-flow.svg"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_ai_cost_anomaly_runbook_has_seo_schema_and_buyer_language():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 3
    for marker in [
        "AI cost anomaly",
        "LLM spend spike",
        "GPU waste",
        "inference cost overage",
        "cloud budget alert",
        "FinOps approval",
        "cost owner dashboard",
        "CFO/CTO approval record",
        "production-risk changes",
    ]:
        assert marker in source


def test_ai_cost_anomaly_runbook_has_truth_boundaries_and_safe_positioning():
    source = html()
    for marker in [
        "not a real client case study",
        "not production workload data",
        "not a testimonial",
        "not a certification",
        "not proof of savings",
        "not ROI evidence",
        "not ranking evidence",
        "not a guarantee of lower AI or cloud cost",
        "No outreach was sent",
        "not security/legal/procurement/accounting/tax advice",
        "/free-business-review/?package=ai-cost-anomaly-runbook",
        "/services/cloud-finops/",
        "/resources/global-enterprise-ai-agent-change-approval-evidence-checklist/",
        "ai-cost-anomaly-approval-log-template.csv",
        "ai-cost-anomaly-approval-flow.svg",
        "Downloadable approval evidence",
    ]:
        assert marker in source


def test_ai_cost_anomaly_runbook_downloads_are_structured_and_labelled():
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 4
    assert rows[0].keys() >= {
        "anomaly_id",
        "trigger_phrase",
        "evidence_source",
        "baseline_window",
        "affected_workload",
        "owner",
        "proposed_action",
        "production_risk",
        "approval_gate",
        "claim_boundary",
        "next_review",
    }
    joined = "\n".join(" ".join(row.values()) for row in rows)
    assert "LLM spend spike" in joined
    assert "GPU waste" in joined
    assert "Do not claim savings" in joined
    svg = SVG_PATH.read_text(encoding="utf-8")
    assert "DEMO / SYNTHETIC" in svg
    assert "no savings, ROI, ranking or guarantee claim" in svg


def test_ai_cost_anomaly_runbook_schema_mentions_dataset_and_image():
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html())
    parsed = [json.loads(block) for block in blocks]
    flat = json.dumps(parsed)
    assert CSV_URL in flat
    assert SVG_URL in flat
    assert "Dataset" in flat
    assert "ImageObject" in flat


def test_ai_cost_anomaly_runbook_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
