import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-outpatient-specialty-referral-prior-auth-growthos-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "us-outpatient-referral-prior-auth-growthos-evidence-register.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"
CSV_URL = URL + "us-outpatient-referral-prior-auth-growthos-evidence-register.csv"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_page_is_indexable_canonical_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_page_contains_us_outpatient_buyer_language_and_competitors():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "US outpatient specialty referral + prior-auth GrowthOS evidence checklist",
        "US outpatient referral leakage",
        "prior authorization workflow software",
        "referral tracking for specialty clinics",
        "patient access automation",
        "Healthcare GrowthOS",
        "Patient GrowthOS",
        "HIPAA AI receptionist questions",
        "Phreesia",
        "Luma Health",
        "Notable",
        "Waystar",
        "Infinx",
        "AKASA",
        "Experian Health",
        "proof-before-platform wedge",
        "Download synthetic CSV",
    ]:
        assert phrase in html


def test_page_has_strict_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for boundary in [
        "synthetic, buyer-education checklist",
        "not a real customer case study",
        "not a testimonial",
        "not customer proof",
        "not patient data",
        "not PHI",
        "not legal/privacy/security/medical/billing/coding advice",
        "not a HIPAA compliance attestation",
        "not SOC 2/HITRUST/ONC/CMS certification proof",
        "not a prior-authorization approval claim",
        "No customer outreach was sent",
    ]:
        assert boundary in html


def test_csv_and_discovery_links_exist():
    html = PAGE.read_text(encoding="utf-8")
    assert "us-outpatient-referral-prior-auth-growthos-evidence-register.csv" in html
    csv = CSV.read_text(encoding="utf-8")
    for phrase in ["synthetic_scenario", "adviser_route", "public_claim_allowed", "no patient data", "no payer approval claim"]:
        assert phrase in csv
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert CSV_URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
