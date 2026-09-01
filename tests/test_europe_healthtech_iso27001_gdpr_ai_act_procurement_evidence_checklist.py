import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-iso27001-gdpr-ai-act-procurement-evidence-checklist"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthtech-iso27001-gdpr-ai-act-procurement-evidence-checklist.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_page_is_indexable_canonical_schema_and_single_h1():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"/>' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-navigation-mount') == 1
    assert source.count('data-aics-global-footer') == 1
    docs = json_ld_documents(source)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "Dataset", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-01"
    for marker in [
        "Europe healthtech ISO 27001 procurement evidence",
        "GDPR DPIA AI procurement questionnaire",
        "EU AI Act healthtech evidence checklist",
        "cloud AI FinOps owner evidence",
        "security questionnaire trust centre evidence",
        "proof-before-platform",
    ]:
        assert marker in article["about"]


def test_research_language_competitors_and_top_consideration_wedge():
    source = html()
    for marker in [
        "Region selected:",
        "Europe / UK-EU business day",
        "healthtech ISO 27001 procurement questionnaire",
        "GDPR DPIA evidence for AI",
        "EU AI Act evidence questions",
        "NHS DSPT / DTAC evidence",
        "trust centre evidence",
        "vendor risk management",
        "security questionnaire answer source map",
        "DPA blocker",
        "data residency",
        "subprocessor register",
        "AI cloud FinOps",
        "LLM cost governance",
        "European Commission AI Act overview returned HTTP 200",
        "ICO AI guidance hub returned HTTP 200",
        "FinOps Foundation Framework returned HTTP 200",
        "NHS DTAC returned HTTP 403",
        "Vanta",
        "Drata",
        "Secureframe",
        "Sprinto",
        "Hyperproof",
        "OneTrust",
        "TrustArc",
        "Conveyor",
        "SafeBase",
        "Whistic",
        "Apptio Cloudability",
        "VMware/CloudHealth",
        "CloudZero",
        "Vantage",
        "Datadog Cloud Cost Management",
        "AWS Cost Explorer",
        "Azure Cost Management",
        "AICS top-3/top-5 consideration wedge",
        "what evidence supports the answer, who owns it, what is missing",
        "Use this before buying another platform",
    ]:
        assert marker in source


def test_claim_boundaries_block_fake_proof():
    source = html()
    for marker in [
        "synthetic buyer-education checklist only",
        "not a real European healthtech case study",
        "not a testimonial",
        "not production data",
        "not patient data",
        "not personal data",
        "not health data",
        "not customer data",
        "not a certification",
        "not ISO 27001 proof",
        "not SOC 2 proof",
        "not GDPR compliance proof",
        "not EU AI Act compliance proof",
        "not NHS DSPT proof",
        "not DTAC proof",
        "not legal advice",
        "not privacy advice",
        "not DPO advice",
        "not security advice",
        "not audit advice",
        "not procurement advice",
        "not clinical advice",
        "not medical advice",
        "not savings evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not demand evidence",
        "not lead evidence",
        "not customer evidence",
        "not revenue evidence",
        "No customer outreach was sent",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed compliance", "gdpr certified", "iso 27001 certified", "real client results", "saved ", "increased revenue"]:
        assert forbidden not in source.lower()


def test_csv_is_synthetic_and_usable():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 6
    assert set(rows[0]) == {
        "buyer_question_pain_language",
        "evidence_buyer_expects",
        "aics_evidence_packet_item",
        "owner_or_adviser_handoff",
        "unsafe_claim_blocked",
        "boundary_label",
    }
    csv_text = CSV.read_text(encoding="utf-8")
    for marker in [
        "Synthetic row only",
        "not certification proof",
        "not GDPR proof",
        "not EU AI Act proof",
        "no patient personal health production or customer data",
        "not savings ROI revenue demand ranking or customer proof",
        "human review required",
    ]:
        assert marker in csv_text


def test_discovery_surfaces_are_wired():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
