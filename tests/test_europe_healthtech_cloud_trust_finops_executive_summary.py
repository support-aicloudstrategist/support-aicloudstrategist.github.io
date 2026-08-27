import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-executive-summary"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_europe_executive_summary_has_indexable_schema_and_single_h1():
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
        "Europe healthtech cloud cost optimisation",
        "AI spend governance executive summary",
        "GDPR evidence owner handoff",
        "DPIA adviser-question readiness",
        "EU AI Act healthtech evidence questions",
        "security questionnaire evidence room",
        "vendor-risk trust centre readiness",
        "data residency and subprocessor evidence",
        "human-review boundary for healthtech AI",
        "proof-before-platform",
    ]:
        assert marker in article["about"]


def test_europe_executive_summary_contains_buyer_language_competitors_and_cluster_links():
    source = html()
    for marker in [
        "Europe / UK-EU",
        "healthtech cloud cost optimisation GDPR evidence",
        "AI cloud FinOps",
        "LLM cost governance",
        "GDPR evidence",
        "DPIA questions",
        "EU AI Act evidence",
        "NHS DSPT",
        "DTAC evidence questions",
        "security questionnaire evidence",
        "vendor risk management",
        "trust centre evidence",
        "data residency",
        "subprocessor register",
        "Apptio Cloudability",
        "CloudHealth",
        "CloudZero",
        "Vantage",
        "Datadog Cloud Cost Management",
        "Vanta",
        "Drata",
        "Secureframe",
        "OneTrust",
        "TrustArc",
        "/resources/europe-healthtech-cloud-trust-finops-evidence-room/",
        "/resources/europe-healthtech-cloud-trust-finops-no-credentials-intake-policy/",
        "/resources/europe-healthtech-cloud-trust-finops-evidence-room/sample.csv",
        "/resources/europe-healthtech-cloud-trust-finops-evidence-room/owner-dashboard.csv",
        "/resources/europe-healthtech-cloud-trust-finops-evidence-room/owner-dashboard.svg",
        "/free-business-review/?package=europe-healthtech-cloud-trust-finops-executive-summary",
    ]:
        assert marker in source


def test_europe_executive_summary_boundaries_block_unverified_claims():
    source = html()
    for marker in [
        "not production data",
        "not patient data",
        "not personal data",
        "not health data",
        "not customer data",
        "not a real European healthtech case study",
        "not a testimonial",
        "not a certification",
        "not GDPR compliance proof",
        "not EU AI Act compliance proof",
        "not NHS DSPT proof",
        "not DTAC proof",
        "not ISO 27001 proof",
        "not SOC 2 proof",
        "not legal advice",
        "not privacy advice",
        "not DPO advice",
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
    for forbidden in ["trusted by", "guaranteed compliance", "gdpr certified", "real client results", "saved ", "increased revenue"]:
        assert forbidden not in source.lower()


def test_europe_executive_summary_discovery_surfaces_are_wired():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
