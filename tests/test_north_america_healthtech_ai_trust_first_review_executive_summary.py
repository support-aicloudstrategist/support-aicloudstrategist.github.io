import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-healthtech-ai-trust-first-review-executive-summary"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_executive_summary_has_indexable_schema_and_single_h1():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-navigation-mount') == 1
    assert source.count('data-aics-global-footer') == 1
    docs = json_ld_documents(source)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-08-27"
    for marker in [
        "North America healthtech executive summary",
        "Healthcare GrowthOS board summary",
        "Patient GrowthOS executive one-pager",
        "HIPAA-style AI receptionist evidence summary",
        "PHI/ePHI no-credentials review boundary",
        "cloud and LLM FinOps owner evidence",
        "healthtech vendor-risk questionnaire readiness",
        "proof-before-platform",
    ]:
        assert marker in article["about"]


def test_executive_summary_contains_buyer_language_competitors_and_cluster_links():
    source = html()
    for marker in [
        "North America / US + Canada",
        "Healthcare GrowthOS",
        "Patient GrowthOS",
        "AI medical receptionist",
        "AI receptionist human handoff",
        "HIPAA-style questionnaire evidence",
        "PHI/ePHI boundary wording",
        "BAA/subprocessor evidence",
        "SOC 2/HITRUST status",
        "cloud cost optimization",
        "AI spend governance",
        "LLM spend owner dashboard",
        "Assort Health",
        "Hyro",
        "Notable",
        "Luma Health",
        "Artera",
        "Phreesia",
        "Vanta",
        "Drata",
        "Apptio Cloudability",
        "CloudZero",
        "/resources/north-america-healthtech-ai-trust-first-review/",
        "/resources/north-america-healthtech-cloud-trust-finops-no-credentials-intake-policy/",
        "/resources/north-america-healthtech-redacted-cloud-ai-intake-template/",
        "/resources/north-america-healthtech-ai-cloud-owner-dashboard-demo/",
        "/resources/north-america-healthtech-ai-cloud-first-review-checklist/healthtech-ai-cloud-first-review-checklist.csv",
        "/resources/north-america-healthtech-ai-procurement-questionnaire-owner-handoff/",
        "/resources/north-america-healthtech-ai-human-review-escalation-policy-template/",
        "/free-business-review/?package=north-america-healthtech-ai-trust-first-review-executive-summary",
    ]:
        assert marker in source


def test_executive_summary_boundaries_block_unverified_claims():
    source = html()
    for marker in [
        "not production data",
        "not patient data",
        "not PHI/ePHI",
        "not customer data",
        "not a real healthtech case study",
        "not a testimonial",
        "not a certification",
        "not HIPAA compliance proof",
        "not SOC 2 proof",
        "not HITRUST certification evidence",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not audit advice",
        "not procurement advice",
        "not clinical advice",
        "not medical advice",
        "not billing advice",
        "not savings evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not demand evidence",
        "not lead evidence",
        "not customer evidence",
        "not revenue evidence",
        "No outreach was sent",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "saved ", "increased revenue"]:
        assert forbidden not in source.lower()


def test_executive_summary_discovery_surfaces_are_wired():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
