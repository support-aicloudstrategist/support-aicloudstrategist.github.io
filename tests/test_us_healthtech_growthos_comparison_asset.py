from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/us-healthtech-growthos-vs-patient-engagement-grc-finops-comparison/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "us-healthtech-growthos-vs-patient-engagement-grc-finops-comparison" / "index.html"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_us_healthtech_growthos_comparison_has_seo_schema_and_single_h1():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-global-footer') == 1
    docs = json_ld_documents(source)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert "Article" in types
    assert "FAQPage" in types
    assert "BreadcrumbList" in types
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert "Healthcare GrowthOS comparison" in article["about"]
    assert "proof-before-platform" in article["about"]
    assert "synthetic owner dashboard demo" in article["about"]


def test_us_healthtech_growthos_comparison_contains_region_research_and_competitors():
    source = html()
    for marker in [
        "Region selected:",
        "North America / United States",
        "Healthcare GrowthOS",
        "Patient GrowthOS",
        "HIPAA AI questionnaire",
        "healthtech AI vendor risk",
        "patient engagement platform comparison",
        "AI receptionist for medical office",
        "prior authorization workflow",
        "LLM cost allocation",
        "Phreesia",
        "NexHealth",
        "Luma Health",
        "Artera",
        "Hyro",
        "Notable",
        "CloudZero",
        "Vantage",
        "IBM Cloudability",
        "Vanta",
        "Drata",
        "OneTrust",
    ]:
        assert marker in source


def test_us_healthtech_growthos_comparison_has_top_consideration_gaps_and_boundaries():
    source = html()
    for marker in [
        "Top-3/top-5 credibility gaps AICS has now started to close",
        "Public demo evidence room",
        "Downloadable GitHub trust artifact",
        "Adviser boundary workflow",
        "Founder/CFO/CTO dashboard mockup",
        "/resources/north-america-healthtech-ai-cloud-owner-dashboard-demo/",
        "/resources/north-america-healthtech-redacted-cloud-ai-intake-template/redacted-cloud-ai-intake-template.csv",
        "/resources/north-america-healthtech-cloud-trust-finops-no-credentials-intake-policy/",
        "synthetic SVG dashboard",
        "not a real client case study",
        "not production healthtech data",
        "not patient data",
        "not PHI",
        "not a testimonial",
        "not a certification",
        "not a HIPAA compliance attestation",
        "not SOC 2 or HITRUST proof",
        "not legal/privacy/security/medical/billing advice",
        "not proof of savings",
        "not ROI evidence",
        "not ranking evidence",
        "No outreach was sent",
        "/free-business-review/?package=us-healthtech-growthos-comparison",
        "/resources/us-healthtech-ai-vendor-risk-cloud-cost-evidence-checklist/",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed savings", "hipaa certified", "real patient results", "revenue lift"]:
        assert forbidden not in source.lower()


def test_us_healthtech_growthos_comparison_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
