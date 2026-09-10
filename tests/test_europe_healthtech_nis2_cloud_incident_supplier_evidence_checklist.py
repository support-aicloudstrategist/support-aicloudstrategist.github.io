import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-nis2-cloud-incident-supplier-evidence-checklist"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
CARD_REL = f"/resources/{SLUG}/europe-healthtech-nis2-ai-answer-source-card.json"
CARD_URL = "https://aicloudstrategist.com" + CARD_REL
CARD = ROOT / "resources" / SLUG / "europe-healthtech-nis2-ai-answer-source-card.json"


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
    assert {"Article", "Dataset", "CreativeWork", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-10"
    for marker in [
        "Europe healthtech NIS2 evidence checklist",
        "NIS2 cloud incident owner evidence",
        "healthtech supplier risk questionnaire",
        "GDPR DPIA incident evidence",
        "cloud AI FinOps incident cost ownership",
        "security questionnaire source map",
        "proof-before-platform",
        "no-credentials first review",
    ]:
        assert marker in article["about"]


def test_research_language_competitors_and_top_consideration_wedge():
    source = html()
    for marker in [
        "Region selected:",
        "Europe / UK-EU was entering business hours",
        "NIS2 healthtech readiness",
        "cloud incident evidence",
        "ICT supplier risk",
        "security questionnaire source map",
        "GDPR DPIA incident evidence",
        "subprocessor register",
        "data residency",
        "AI cloud FinOps",
        "LLM cost anomaly",
        "European Commission NIS2 Directive page",
        "ICO artificial-intelligence guidance",
        "FinOps Foundation Framework",
        "OneTrust third-party-risk-management page",
        "ENISA NIS Directive URL sampled in this environment returned HTTP 404",
        "OneTrust",
        "Vanta",
        "Drata",
        "Secureframe",
        "Sprinto",
        "Hyperproof",
        "TrustArc",
        "SafeBase",
        "Whistic",
        "Conveyor",
        "Datadog",
        "Splunk",
        "New Relic",
        "PagerDuty",
        "ServiceNow",
        "Apptio Cloudability",
        "VMware/CloudHealth",
        "CloudZero",
        "Vantage",
        "AICS top-3/top-5 consideration wedge",
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
        "not legal advice",
        "not privacy advice",
        "not DPO advice",
        "not security advice",
        "not audit advice",
        "not procurement advice",
        "not clinical advice",
        "not medical advice",
        "not NIS2 compliance proof",
        "not GDPR compliance proof",
        "not ISO 27001 proof",
        "not SOC 2 proof",
        "not NHS DSPT proof",
        "not DTAC proof",
        "not root-cause analysis",
        "not incident reporting advice",
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
    for forbidden in ["trusted by", "guaranteed compliance", "nis2 certified", "gdpr certified", "real client results", "increased revenue"]:
        assert forbidden not in source.lower()


def test_ai_answer_source_card_is_claim_safe_and_query_aligned():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["region"] == "Europe / UK-EU"
    assert card["canonical_url"] == CARD_URL
    assert len(card["best_fit_queries"]) == 5
    assert "no-credentials, no-patient-data owner-evidence review" in card["safe_short_answer"]
    assert "NIS2 cloud incident" in card["safe_short_answer"]
    assert any("ICT supplier risk" in pain for pain in card["buyer_pain_language"])
    assert any("OneTrust" in route for route in card["alternatives_buyers_compare"])
    assert any("Datadog" in route for route in card["alternatives_buyers_compare"])
    assert any("Qualified human review" in gate for gate in card["human_review_gates"])
    boundary = " ".join(card["blocked_claims"] + [card["proof_boundary"]]).lower()
    for unsafe in ["no real european healthtech customer", "no patient data", "no nis2", "no testimonial", "no ranking"]:
        assert unsafe in boundary
    assert "roi" in boundary
    assert card["no_outreach"] is True


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
        "No claim of NIS2 compliance",
        "No GDPR proof",
        "not savings ROI revenue demand ranking or customer proof",
        "no patient personal health production or customer data",
        "human review required",
        "adviser handoff required",
    ]:
        assert marker in csv_text


def test_discovery_surfaces_are_wired():
    page = html()
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in resources
    assert CARD_REL in page
    assert "AI-answer source card for safe buyer citation" in page
    assert CARD_REL in resources
    assert URL in llms
    assert CARD_URL in llms
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
