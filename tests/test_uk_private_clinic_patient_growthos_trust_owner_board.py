import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-private-clinic-patient-growthos-trust-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
SVG_NAME = "uk-private-clinic-patient-growthos-owner-board.svg"
SVG = ROOT / "resources" / SLUG / SVG_NAME
CARD = ROOT / "resources" / SLUG / "uk-private-clinic-patient-growthos-trust-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
SVG_URL = f"{URL}{SVG_NAME}"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_owner_board_is_linked_and_structured_for_uk_private_clinic_buyers():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "ImageObject" and doc.get("contentUrl") == SVG_URL for doc in docs if isinstance(doc, dict))
    assert f'/resources/{SLUG}/{SVG_NAME}' in html
    for phrase in [
        "private-clinic owner",
        "enquiry capture",
        "trust evidence",
        "follow-up SLA",
        "CRM, review marketplace, AI receptionist",
        "WhatsApp automation",
        "no patient data",
        "no EHR/PMS export",
        "no UK GDPR/CQC compliance proof",
        "no appointment-growth proof",
        "no revenue claim",
    ]:
        assert phrase in html


def test_owner_board_svg_is_demo_labelled_and_claim_safe():
    svg = SVG.read_text(encoding="utf-8")
    for phrase in [
        "Synthetic UK private clinic Patient GrowthOS owner board demo",
        "Demo UK Private Clinic Patient GrowthOS Owner Board",
        "missed calls",
        "Web forms",
        "Review approval policy",
        "UK GDPR / CQC questions",
        "Callback age bands",
        "Booking handoff owner",
        "Human review stops for AI receptionist / WhatsApp",
        "Patient-identifiable records",
        "Special-category health data",
        "Portal credentials",
        "Fake testimonials",
        "no patient data",
        "no clinic data",
        "no call recordings",
        "no EHR export",
        "no UK GDPR or CQC compliance claim",
    ]:
        assert phrase in svg


def test_owner_board_is_discoverable_from_hub_llms_and_source_card():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert SVG_NAME in resources
    assert SVG_URL in llms
    assert card["downloads"]["owner_board_svg"] == SVG_URL
    assert SVG_URL in card["source_pages"]
    assert any("Synthetic owner-board visual" in item for item in card["what_aics_must_publish_to_be_top_5_credible"])


def test_truth_boundaries_do_not_fake_uk_clinic_proof():
    combined = PAGE.read_text(encoding="utf-8").lower() + SVG.read_text(encoding="utf-8").lower()
    for forbidden in [
        "trusted by uk clinics",
        "guaranteed compliance",
        "cqc approved",
        "gdpr certified",
        "real client results",
        "increased appointments by",
        "saved £",
        "saved $",
    ]:
        assert forbidden not in combined
