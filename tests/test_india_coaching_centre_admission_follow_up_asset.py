import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-coaching-centre-admission-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


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


def test_page_contains_india_coaching_buyer_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    for phrase in [
        "India coaching centre admission follow up checklist",
        "Coaching centre admission enquiries not converting",
        "tuition centre WhatsApp enquiry follow up",
        "coaching class demo booking no show follow up",
        "student admission counselling CRM owner dashboard",
        "AI assistant for coaching centre enquiries with human review",
        "AI output is draft support, not an official representation",
        "counsellor ownership and parent follow-up evidence",
    ]:
        assert phrase in html
    for boundary in [
        "not a real customer case study",
        "not a testimonial",
        "not customer proof",
        "no real coaching centre, school, institute, student, parent, teacher, counsellor, prospect, lead",
        "not legal advice",
        "not privacy advice",
        "not education advice",
        "not academic advice",
        "not a compliance claim",
        "It does not claim DPDP compliance, child-data compliance",
        "admission growth, revenue result, ROI result, ranking result, ad-performance result or AI-accuracy result",
    ]:
        assert boundary in html


def test_asset_is_linked_for_discovery():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
