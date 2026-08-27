import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "north-america-healthtech-ai-procurement-questionnaire-owner-handoff"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "procurement-questionnaire-owner-handoff.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_owner_handoff_has_seo_schema_and_single_h1():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-navigation-mount') == 1
    assert source.count('data-aics-global-footer') == 1
    docs = json_ld_documents(source)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert "Article" in types
    assert "Dataset" in types
    assert "FAQPage" in types
    assert "BreadcrumbList" in types
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-08-27"
    for marker in [
        "North America healthtech AI procurement questionnaire",
        "HIPAA-style questionnaire owner handoff",
        "PHI ePHI AI data-use evidence",
        "human review escalation owner",
        "proof-before-platform",
    ]:
        assert marker in article["about"]


def test_owner_handoff_contains_buyer_language_and_cta_path():
    source = html()
    for marker in [
        "North America / US + Canada",
        "procurement questionnaires often stall because answer owners",
        "HIPAA-style AI vendor risk questionnaire answers",
        "PHI/ePHI boundary wording",
        "BAA/subprocessor evidence",
        "SOC 2 or HITRUST status",
        "security-questionnaire evidence rooms",
        "LLM spend governance",
        "patient-engagement, GRC, trust-center, vendor-risk and FinOps tools",
        "/free-business-review/?package=north-america-healthtech-ai-procurement-questionnaire-owner-handoff",
        "/resources/north-america-healthtech-ai-procurement-questionnaire-owner-handoff/procurement-questionnaire-owner-handoff.csv",
        "/resources/north-america-healthtech-ai-cloud-first-review-checklist/",
        "/resources/north-america-healthtech-ai-cloud-finops-trust-evidence-room/",
        "/resources/us-healthtech-hipaa-ai-procurement-evidence-source-map/",
    ]:
        assert marker in source


def test_owner_handoff_boundaries_block_unverified_claims():
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


def test_owner_handoff_csv_and_discovery_surfaces_are_wired():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 8
    assert set(rows[0]) == {"question_area", "buyer_question", "source_evidence_to_prepare", "answer_owner", "review_gate", "unsafe_claim_to_block", "boundary_label"}
    csv_text = CSV.read_text(encoding="utf-8")
    for marker in [
        "Template row only; not HIPAA advice or compliance proof",
        "Template row only; not legal advice or contract approval",
        "Template row only; not certification evidence",
        "Template row only; not savings ROI or revenue proof",
        "Template row only; not medical clinical billing or legal advice",
        "Template row only; not customer testimonial ranking outcome or revenue proof",
    ]:
        assert marker in csv_text
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
