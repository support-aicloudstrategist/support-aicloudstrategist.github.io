from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-enterprise-ai-cost-anomaly-approval-runbook/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "global-enterprise-ai-cost-anomaly-approval-runbook" / "index.html"


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
    ]:
        assert marker in source


def test_ai_cost_anomaly_runbook_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
