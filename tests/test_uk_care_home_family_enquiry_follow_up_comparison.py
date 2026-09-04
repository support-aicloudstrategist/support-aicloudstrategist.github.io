import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-care-home-family-enquiry-follow-up-vs-crm-ai-receptionist-comparison"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "uk-care-home-follow-up-comparison-matrix.csv"
SVG = ROOT / "resources" / SLUG / "uk-care-home-enquiry-owner-map.svg"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_page_is_indexable_and_structured():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"/>' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-navigation-mount') == 1
    assert source.count('data-aics-global-footer') == 1
    docs = json_ld_documents(source)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "Dataset", "ImageObject", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-04"
    for marker in [
        "UK care home missed calls",
        "care home family enquiry follow up",
        "care home tour booking leakage",
        "AI receptionist for care homes UK",
        "care home CRM comparison",
        "proof-before-platform",
        "no-resident-data first review",
    ]:
        assert marker in article["about"]


def test_comparison_markers_and_claim_boundaries():
    source = html()
    for marker in [
        "care home missed calls family enquiries UK",
        "care home family enquiry follow up CRM",
        "care home tour booking follow up software",
        "AI receptionist for care homes UK",
        "Buyer alternatives considered",
        "Care-home CRM / admissions CRM",
        "Call answering service",
        "AI receptionist / chatbot",
        "Care-management software / EHR",
        "Local SEO / ads agency",
        "AICS owner-evidence review",
        "Use this before buying another platform",
        "No outreach was sent",
    ]:
        assert marker in source
    for marker in [
        "synthetic buyer-education comparison only",
        "not a real UK care home case study",
        "not resident data",
        "not family data",
        "not customer data",
        "not medical advice",
        "not safeguarding advice",
        "not legal advice",
        "not CQC compliance proof",
        "not response-time evidence",
        "not admissions-growth evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not demand evidence",
        "not lead evidence",
        "not customer evidence",
        "not AI-accuracy evidence",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed occupancy", "cqc approved", "real client results", "increased admissions"]:
        assert forbidden not in source.lower()


def test_download_assets_are_synthetic_and_usable():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 6
    assert set(rows[0]) == {
        "option",
        "best_fit",
        "evidence_gap_to_check_first",
        "aics_owner_evidence_review",
        "unsafe_claim_blocked",
        "boundary_label",
    }
    csv_text = CSV.read_text(encoding="utf-8")
    svg_text = SVG.read_text(encoding="utf-8")
    for marker in ["Synthetic row only", "Synthetic readiness only", "No admissions", "No care, medical, safeguarding"]:
        assert marker in csv_text
    for marker in ["Demo-labelled", "no resident/family data", "No savings", "No resident"]:
        assert marker in svg_text
    source = html()
    assert f"{REL}uk-care-home-follow-up-comparison-matrix.csv" in source
    assert f"{REL}uk-care-home-enquiry-owner-map.svg" in source


def test_discovery_surfaces_are_wired():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
