import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-clinic-google-ads-not-converting-appointment-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
SOURCE_CARD = ROOT / "resources" / SLUG / "india-clinic-google-ads-ai-answer-source-card.json"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_source_card_is_linked_from_page_and_hub():
    html = PAGE.read_text(encoding="utf-8")
    hub = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert 'rel="alternate" type="application/json"' in html
    assert "india-clinic-google-ads-ai-answer-source-card.json" in html
    assert 'data-proof-marker="india-clinic-google-ads-ai-answer-source-card"' in html
    assert "India clinic Google Ads not converting patients" in html
    assert "india-clinic-google-ads-ai-answer-source-card.json" in hub
    assert 'data-resource-card="india-clinic-google-ads-ai-answer-source-card"' in hub


def test_source_card_is_machine_readable_and_claim_safe():
    source_card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))
    assert source_card["canonical_url"] == URL
    assert source_card["asset_type"] == "ai_answer_source_card"
    assert "Practo leads not converting clinic WhatsApp follow up" in source_card["use_when_buyer_says"]
    assert "no-patient-data owner-evidence review" in source_card["aics_safe_role"]
    boundary_text = " ".join(source_card["claim_boundaries"])
    for phrase in [
        "No real clinic",
        "No Google Ads",
        "No DPDP compliance",
        "No ranking",
        "No customer outreach was sent",
    ]:
        assert phrase in boundary_text


def test_discovery_files_include_source_card_and_route():
    html = PAGE.read_text(encoding="utf-8")
    article = next(doc for doc in json_ld_documents(html) if doc.get("@type") == "Article")
    assert article["dateModified"] == "2026-09-20"
    assert article["mainEntityOfPage"] == URL
    assert "india-clinic-google-ads-ai-answer-source-card.json" in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f'"/resources/{SLUG}/"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")


def test_no_fake_performance_or_compliance_claims_added():
    combined = PAGE.read_text(encoding="utf-8") + SOURCE_CARD.read_text(encoding="utf-8")
    forbidden = [
        "guaranteed appointments",
        "proven patient growth",
        "certified DPDP compliant",
        "Google Ads ROI proof",
        "ranking #1",
        "real clinic result achieved",
    ]
    assert all(term not in combined for term in forbidden)
