import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-dental-clinic-missed-calls-whatsapp-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_FILE = ROOT / "resources" / SLUG / "india-dental-follow-up-owner-evidence.csv"
ANSWER_BANK = ROOT / "resources" / SLUG / "india-dental-ai-answer-bank.csv"
SVG_FILE = ROOT / "resources" / SLUG / "india-dental-follow-up-owner-board.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"
PRICING = ROOT / "pricing.html"
FREE_REVIEW = ROOT / "free-business-review" / "index.html"
FREE_REVIEW_LEGACY = ROOT / "free-business-review.html"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_india_dental_page_has_buyer_language_and_truth_boundary():
    html = PAGE.read_text(encoding="utf-8")
    assert "dental clinic missed calls India" in html
    assert "dental WhatsApp follow up" in html
    assert "implant enquiry not converting" in html
    assert "AI receptionist for dental clinic India" in html
    assert "DPDP adviser questions" in html
    assert "No real dental clinic" in html
    assert "not evidence of appointments, patients, revenue" in html
    assert "dateModified\":\"2026-09-08" in html
    assert "AI-answer bank for dental follow-up searches" in html
    assert "Download synthetic AI-answer bank CSV" in html


def test_india_dental_json_ld_has_article_dataset_image_faq():
    docs = _json_ld_documents(PAGE.read_text(encoding="utf-8"))
    types = {doc.get("@type") for doc in docs}
    assert {"Article", "Dataset", "ImageObject", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(doc for doc in docs if doc.get("@type") == "Article")
    dataset = next(doc for doc in docs if doc.get("@type") == "Dataset")
    datasets = [doc for doc in docs if doc.get("@type") == "Dataset"]
    faq = next(doc for doc in docs if doc.get("@type") == "FAQPage")
    assert article["mainEntityOfPage"].endswith(f"/resources/{SLUG}/")
    assert article["image"].endswith("india-dental-follow-up-owner-board.svg")
    assert "Synthetic no-patient-data" in dataset["description"]
    assert dataset["url"].endswith("india-dental-follow-up-owner-evidence.csv")
    assert any(doc.get("url", "").endswith("india-dental-ai-answer-bank.csv") for doc in datasets)
    assert len(faq["mainEntity"]) == 3


def test_india_dental_csv_and_svg_are_synthetic_and_no_patient_data():
    rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8")))
    assert len(rows) == 5
    assert rows[0]["field"] == "missed_call_queue"
    assert all(row["human_review_gate"].strip() for row in rows)
    assert any("DPDP compliance" in row["unsafe_claim_to_block"] for row in rows)
    svg = SVG_FILE.read_text(encoding="utf-8")
    assert "Synthetic India dental missed-call and WhatsApp owner board" in svg
    assert "no patient names" in svg
    assert "Safety gate" in svg


def test_india_dental_ai_answer_bank_blocks_unsafe_claims():
    rows = list(csv.DictReader(ANSWER_BANK.open(encoding="utf-8")))
    assert len(rows) == 5
    questions = "\n".join(row["buyer_question"] for row in rows)
    unsafe = "\n".join(row["unsafe_claim_to_block"] for row in rows)
    gates = "\n".join(row["human_review_gate"] for row in rows)
    assert "Why are dental clinic calls and WhatsApp enquiries not converting into appointments?" in questions
    assert "Should an Indian dental clinic buy an AI receptionist before fixing follow-up?" in questions
    assert "Do not request credentials, PHI/sensitive personal data" in unsafe
    assert "Do not claim appointments, patients, treatment acceptance, revenue, savings, ROI" in unsafe
    assert "Clinical, privacy/legal adviser and clinic leadership" in gates


def test_india_dental_pack_is_discoverable_from_hub_llms_and_sitemap():
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
    assert "india-dental-follow-up-owner-evidence.csv" in resources
    assert "india-dental-ai-answer-bank.csv" in resources
    assert "india-dental-follow-up-owner-board.svg" in resources
    assert "india-dental-follow-up-owner-evidence.csv" in llms
    assert "india-dental-ai-answer-bank.csv" in llms


def test_india_dental_revenue_bridge_is_wired_to_pricing_and_free_review():
    pricing = PRICING.read_text(encoding="utf-8")
    assert "Thirty-seven concrete first offers" in pricing
    assert '"numberOfItems":37' in pricing
    assert 'data-revenue-bridge="india-dental-missed-calls-whatsapp-follow-up"' in pricing
    assert "Scope before dental CRM, call-centre, ad-agency, WhatsApp automation or AI receptionist spend" in pricing
    assert "/free-business-review/?package=india-dental-missed-calls-whatsapp-follow-up&amp;source=pricing-fixed-scope" in pricing
    assert "no real dental clinic" in pricing
    assert "booked appointment, patient growth, revenue, savings, ROI" in pricing

    for path in (FREE_REVIEW, FREE_REVIEW_LEGACY):
        html = path.read_text(encoding="utf-8")
        assert 'data-review-route="india-dental-missed-calls-whatsapp-follow-up"' in html
        assert "Dental missed-call + WhatsApp follow-up fit check" in html
        assert f"/resources/{SLUG}/" in html
        assert "india-dental-follow-up-owner-evidence.csv" in html
        assert "india-dental-follow-up-owner-board.svg" in html
