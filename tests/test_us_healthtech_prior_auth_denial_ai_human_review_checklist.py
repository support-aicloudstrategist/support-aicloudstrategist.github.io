import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthtech-prior-auth-denial-ai-human-review-checklist"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_page_indexable_canonical_schema_and_boundaries():
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
    assert article["dateModified"] == "2026-09-04"
    for marker in [
        "US healthtech prior authorization AI human review checklist",
        "prior authorization denial follow up evidence",
        "AI appeal drafting healthcare human review",
        "HIPAA AI vendor risk evidence",
        "patient access denial workflow",
        "healthcare GrowthOS owner evidence",
        "RCM automation evidence boundary",
        "cloud LLM cost ownership healthcare",
        "no PHI first review",
        "proof-before-platform",
    ]:
        assert marker in article["about"]


def test_research_snapshot_competitors_and_wedge():
    source = html()
    for marker in [
        "Region selected:",
        "North America / United States",
        "06:37 US Eastern",
        "prior authorization delay",
        "denial follow-up",
        "AI appeal drafting healthcare",
        "HIPAA AI vendor risk",
        "healthtech security questionnaire",
        "patient engagement platform comparison",
        "cloud cost owner dashboard",
        "LLM cost allocation",
        "Phreesia",
        "Luma Health",
        "Artera",
        "Vanta",
        "Drata",
        "OneTrust",
        "CloudZero",
        "Apptio Cloudability",
        "CloudHealth",
        "Flexera",
        "Harness",
        "AICS top-3/top-5 consideration wedge",
        "no-credentials, no-PHI evidence packet",
        "ONC health IT privacy/security resources",
        "returned HTTP 200",
        "returned HTTP 403",
        "returned HTTP 404",
    ]:
        assert marker in source


def test_claim_boundaries_block_fake_proof():
    source = html()
    for marker in [
        "synthetic buyer-education checklist only",
        "not a real US healthtech",
        "not PHI/ePHI",
        "not claims data",
        "not payer data",
        "not patient data",
        "not customer data",
        "not production data",
        "not a testimonial",
        "not certification",
        "not HIPAA compliance proof",
        "not SOC 2 proof",
        "not HITRUST proof",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not medical advice",
        "not billing advice",
        "not coding advice",
        "not payer advice",
        "not denial-reduction evidence",
        "not recovered-revenue evidence",
        "not savings evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not demand evidence",
        "not lead evidence",
        "not revenue evidence",
        "No customer outreach was sent",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed compliance", "hipaa certified", "real client results", "increased revenue"]:
        assert forbidden not in source.lower()


def test_csv_is_synthetic_no_phi_and_owner_usable():
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
        "no PHI/ePHI or claims data",
        "adviser handoff required",
        "human review required",
        "No HIPAA SOC 2 HITRUST procurement approval or certification claim",
        "No savings, ROI, cost-reduction, ranking, demand, lead, customer or revenue claim",
    ]:
        assert marker in csv_text


def test_discovery_surfaces_are_wired():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
