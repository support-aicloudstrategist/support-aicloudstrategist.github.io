import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-clinic-google-ads-not-converting-appointment-evidence-checklist"
URL = "https://aicloudstrategist.com/resources/" + SLUG + "/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / (SLUG + ".csv")
SVG = ROOT / "resources" / SLUG / "india-clinic-ad-to-appointment-owner-board.svg"

def html():
    return PAGE.read_text(encoding="utf-8")

def docs(source):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I|re.S)]

def test_page_indexable_schema_and_search_markers():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"/>' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-navigation-mount') == 1
    assert source.count('data-aics-global-footer') == 1
    types = {d.get("@type") for d in docs(source) if isinstance(d, dict)}
    assert {"Article", "Dataset", "ImageObject", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(d for d in docs(source) if isinstance(d, dict) and d.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-04"
    for marker in ["India clinic Google Ads not converting patients", "Practo leads not converting clinic", "proof-before-more-ad-spend", "no-patient-data first review"]:
        assert marker in article["about"]

def test_visibility_references_and_wedge():
    source = html()
    for marker in ["Bing returned HTTP 200", "did not show a readable AICS marker", "Google Ads India", "Practo for doctors", "Lybrate", "HubSpot CRM", "Zoho CRM", "Zocdoc returned HTTP 403", "AICS top-3/top-5 consideration wedge", "source-to-owner evidence before more ads"]:
        assert marker in source

def test_claim_boundaries_block_fake_proof():
    source = html().lower()
    for marker in ["synthetic buyer-education checklist only", "not a real india clinic case study", "not patient data", "not health data", "not personal data", "not a google ads performance report", "not dpdp compliance proof", "not legal advice", "not medical advice", "not a ranking claim", "not demand evidence", "not lead evidence", "not patient evidence", "not appointment-growth evidence", "not revenue evidence", "not roi evidence", "no customer outreach was sent"]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed revenue", "real client results", "increased appointments"]:
        assert forbidden not in source

def test_csv_and_svg_are_synthetic_owner_usable():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 6
    assert set(rows[0]) == {"channel_or_lead_source", "buyer_pain_question", "evidence_to_collect_without_patient_data", "owner_or_handoff", "next_safe_action", "blocked_claim", "boundary_label"}
    text = CSV.read_text(encoding="utf-8")
    for marker in ["Synthetic row only", "no patient health personal production or customer data", "No guaranteed patients appointments revenue ROI or ad performance", "No DPDP compliance proof legal advice or medical advice"]:
        assert marker in text
    svg = SVG.read_text(encoding="utf-8")
    assert "Demo India clinic ad-to-appointment owner board" in svg
    assert "no patient data" in svg
