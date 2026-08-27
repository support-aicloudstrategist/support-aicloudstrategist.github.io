import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-healthtech-ai-human-review-escalation-policy-template"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "human-review-escalation-policy-template.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_policy_template_has_seo_schema_and_single_h1():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-navigation-mount') == 1
    assert source.count('data-aics-global-footer') == 1
    docs = json_ld_documents(source)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "Dataset", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-08-27"
    for marker in [
        "North America healthtech AI human review escalation policy",
        "HIPAA-style AI receptionist human handoff",
        "PHI/ePHI AI data-use boundary",
        "patient workflow unsafe automation stop list",
        "healthtech vendor-risk questionnaire evidence",
        "LLM spend governance owner escalation",
        "proof-before-platform",
    ]:
        assert marker in article["about"]


def test_policy_template_contains_buyer_language_and_cluster_links():
    source = html()
    for marker in [
        "North America / US + Canada",
        "AI receptionist human handoff",
        "HIPAA compliant AI workflow",
        "PHI/ePHI boundary wording",
        "patient engagement escalation rules",
        "BAA/subprocessor evidence",
        "SOC 2 or HITRUST status",
        "LLM spend governance",
        "unsafe automation stop list",
        "patient-engagement or front-office vendors",
        "GRC and FinOps tools",
        "/free-business-review/?package=north-america-healthtech-ai-human-review-escalation-policy-template",
        "/resources/north-america-healthtech-ai-human-review-escalation-policy-template/human-review-escalation-policy-template.csv",
        "/resources/north-america-healthtech-ai-cloud-finops-trust-evidence-room/",
        "/resources/north-america-healthtech-cloud-trust-finops-no-credentials-intake-policy/",
        "/resources/north-america-healthtech-ai-procurement-questionnaire-owner-handoff/",
        "/resources/us-healthtech-hipaa-ai-procurement-evidence-source-map/",
    ]:
        assert marker in source


def test_policy_template_boundaries_block_unverified_claims():
    source = html()
    for marker in [
        "not production data",
        "not patient data",
        "not PHI/ePHI",
        "not customer data",
        "not a real healthtech case study",
        "not a testimonial",
        "not procurement-win evidence",
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
        "not revenue evidence",
        "No outreach was sent",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "saved ", "increased revenue"]:
        assert forbidden not in source.lower()


def test_policy_template_csv_and_discovery_surfaces_are_wired():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 8
    assert set(rows[0]) == {"policy_area", "buyer_question", "evidence_to_prepare", "default_owner", "human_review_trigger", "unsafe_automation_to_block", "boundary_label"}
    csv_text = CSV.read_text(encoding="utf-8")
    for marker in [
        "Template row only; not medical advice, clinical approval or HIPAA compliance proof",
        "Template row only; not privacy legal security or HIPAA advice",
        "Template row only; not certification audit legal or procurement advice",
        "Template row only; not savings ROI revenue or FinOps outcome proof",
        "Template row only; not customer testimonial ranking outcome or revenue proof",
    ]:
        assert marker in csv_text
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
