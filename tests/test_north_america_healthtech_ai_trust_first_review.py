import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-healthtech-ai-trust-first-review"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_trust_first_review_has_seo_schema_and_single_h1():
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
        "North America healthtech AI trust first review",
        "healthtech AI cloud trust diagnostic package",
        "HIPAA-style AI receptionist evidence review",
        "PHI/ePHI no-credentials intake",
        "patient workflow human-review readiness",
        "cloud and LLM spend owner evidence",
        "proof-before-platform",
    ]:
        assert marker in article["about"]


def test_trust_first_review_contains_buyer_language_cluster_and_cta():
    source = html()
    for marker in [
        "North America / US + Canada",
        "AI receptionist human handoff evidence",
        "healthtech AI cloud trust first review",
        "HIPAA-style questionnaire evidence before AI scale",
        "PHI/ePHI no-credentials intake boundary",
        "cloud and LLM spend owner dashboard",
        "SOC 2 / HITRUST status question preparation",
        "/free-business-review/?package=north-america-healthtech-ai-trust-first-review",
        "/resources/north-america-healthtech-ai-cloud-finops-trust-evidence-room/",
        "/resources/north-america-healthtech-cloud-trust-finops-no-credentials-intake-policy/",
        "/resources/north-america-healthtech-redacted-cloud-ai-intake-template/",
        "/resources/north-america-healthtech-ai-cloud-owner-dashboard-demo/",
        "/resources/north-america-healthtech-ai-cloud-first-review-checklist/",
        "/resources/north-america-healthtech-ai-procurement-questionnaire-owner-handoff/",
        "/resources/north-america-healthtech-ai-human-review-escalation-policy-template/",
    ]:
        assert marker in source


def test_trust_first_review_boundaries_block_unverified_claims():
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
        "not buyer approval evidence",
        "not lead evidence",
        "not customer evidence",
        "not revenue evidence",
        "No outreach was sent",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "saved ", "increased revenue"]:
        assert forbidden not in source.lower()
