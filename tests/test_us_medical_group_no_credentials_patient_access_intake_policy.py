import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-group-no-credentials-patient-access-intake-policy"
PAGE = ROOT / "resources" / SLUG / "index.html"
COMPARISON = ROOT / "resources" / "us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison" / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_policy_blocks_unsafe_first_review_inputs():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "No-credentials intake policy for no-show recovery and patient-access reviews",
        "Do not send in first review",
        "PHI/ePHI",
        "EHR/PMS, RCM, call-center, portal, analytics or AI receptionist logins",
        "Payer files, claims, eligibility, authorization or denial records containing individuals",
        "Call recordings, transcripts or voicemails",
        "Unsupported success claims",
        "Safe substitute",
    ]:
        assert phrase in html


def test_policy_truth_boundary_avoids_fake_healthcare_proof():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "not a customer case study",
        "no-show reduction result",
        "appointment-growth result",
        "HIPAA proof",
        "No outreach was sent",
        "No savings, revenue, appointment-growth, ranking, lead, customer, testimonial, certification or compliance-proof claim",
    ]:
        assert phrase in html
    forbidden = ["guaranteed HIPAA compliance", "reduced no-shows by", "Acme Medical Group", "customer testimonial"]
    assert all(term not in html for term in forbidden)


def test_policy_schema_and_discovery_links_are_present():
    html = PAGE.read_text(encoding="utf-8")
    article = next(doc for doc in json_ld_documents(html) if doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-08-31"
    assert "AI receptionist HIPAA boundary" in article["about"]
    assert f"/resources/{SLUG}/" in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f'"/resources/{SLUG}/"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in COMPARISON.read_text(encoding="utf-8")
