import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-healthtech-patient-access-procurement-diagnostic-scope-memo"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_scope_memo_is_indexable_and_structured():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Service" and doc.get("offers", {}).get("url", "").endswith("stage=scoping") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)
    assert any(doc.get("@type") == "BreadcrumbList" for doc in docs)


def test_scope_memo_is_buyer_sendable_and_revenue_ready_without_payment_claim():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "Buyer-sendable scope memo",
        "No PHI/ePHI",
        "No payment before proposal",
        "Request proposal-ready scope",
        "Patient-access operating evidence",
        "Referral leakage and owner handoff points",
        "Eligibility status ownership",
        "Prior-authorization blocker visibility",
        "HIPAA/PHI/BAA answer-source ownership",
        "Security-questionnaire, SOC 2/HITRUST and subprocessor evidence gaps",
        "Cloud/LLM FinOps owner map",
        "Unsupported sales claims",
        "Evidence source map",
        "Owner handoff matrix",
        "Unsupported-claim stop list",
        "Proposal-ready next step",
        "AICS scopes the diagnostic before quote, payment or implementation",
    ]:
        assert phrase in html


def test_scope_memo_truth_boundaries_block_fake_healthtech_proof():
    html = PAGE.read_text(encoding="utf-8")
    for boundary in [
        "not a customer result",
        "not a real healthtech case study",
        "not patient data",
        "not PHI/ePHI",
        "not production cloud data",
        "not a testimonial",
        "not certification",
        "not HIPAA compliance attestation",
        "not SOC 2 or HITRUST proof",
        "not legal/privacy/security/medical/billing/coding/payer/procurement advice",
        "not platform endorsement",
        "not partnership proof",
        "not ranking evidence",
        "not procurement approval",
        "not questionnaire approval",
        "not savings evidence",
        "not ROI evidence",
        "not revenue evidence",
        "not proof of booked appointments, no-show reduction, authorization speed, denial reduction, patient outcomes or AI accuracy",
        "No outreach was sent",
    ]:
        assert boundary in html
    forbidden = ["HIPAA compliant", "SOC 2 certified", "HITRUST certified", "guaranteed savings", "guaranteed revenue"]
    assert all(term not in html for term in forbidden)


def test_scope_memo_is_linked_from_discovery_and_revenue_surfaces():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert PATH in (ROOT / "pricing.html").read_text(encoding="utf-8")
    assert PATH in (ROOT / "resources" / "us-healthtech-ai-patient-access-procurement-answer-bank" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
