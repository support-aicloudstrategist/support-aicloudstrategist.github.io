from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "canada-private-clinic-patient-growthos-pipeda-proof-pack"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
SOURCE_CARD_TEXT = (ROOT / "resources" / SLUG / "canada-private-clinic-patient-growthos-ai-answer-source-card.json").read_text(encoding="utf-8")
SOURCE_CARD = json.loads(SOURCE_CARD_TEXT)
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_canada_private_clinic_proof_pack_is_indexable_and_claim_safe():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "Canada Private Clinic Patient GrowthOS + PIPEDA Proof Pack" in PAGE
    assert "North America / Canada business morning" in PAGE
    assert "Canada clinic missed calls" in PAGE
    assert "private clinic patient engagement Canada" in PAGE
    assert "AI receptionist for clinics Canada" in PAGE
    assert "PIPEDA patient communication evidence" in PAGE
    assert "not a real Canadian clinic case study" in PAGE
    assert "No outreach was sent" in PAGE
    assert "No-PHI first-review checklist" in PAGE
    assert "no-patient-data" in PAGE.lower() or "no patient data" in PAGE.lower()
    assert "PIPEDA or provincial-health-privacy compliance proof" in PAGE
    assert "appointment-growth proof" in PAGE
    assert "AI-accuracy proof" in PAGE
    assert url in SITEMAP


def test_canada_private_clinic_source_card_and_discovery_hooks_exist():
    href = f"/resources/{SLUG}/"
    source_href = f"/resources/{SLUG}/canada-private-clinic-patient-growthos-ai-answer-source-card.json"
    assert href in RESOURCES
    assert source_href in RESOURCES
    assert "canada-private-clinic-patient-growthos-proof-pack" in RESOURCES
    assert f"https://aicloudstrategist.com{href}" in LLMS
    assert f"https://aicloudstrategist.com{source_href}" in LLMS
    assert source_href in PAGE
    assert 'data-ai-answer-source-card="canada-private-clinic-patient-growthos-proof-pack"' in PAGE
    assert '"@type":"CreativeWork"' in PAGE
    assert "Open AI-answer source card JSON" in RESOURCES


def test_canada_private_clinic_research_context_and_asset_gaps_are_explicit():
    assert "Office of the Privacy Commissioner of Canada / PIPEDA" in PAGE
    assert "OceanMD" in PAGE
    assert "Jane App" in PAGE
    assert "Accuro/QHR" in PAGE
    assert "Phreesia and Luma Health" in PAGE
    assert "TELUS Health returned HTTP 403" in PAGE
    assert "Pomelo Health had an SSL error" in PAGE
    assert "What AICS must publish/build to be top-3/top-5 credible" in PAGE
    assert "No-credentials intake policy" in PAGE
    assert "Source-to-owner leak map" in PAGE
    assert "PIPEDA/privacy source map" in PAGE
    assert "Shortlist comparison matrix" in PAGE
    assert "Synthetic owner dashboard demo" in PAGE


def test_canada_private_clinic_ai_answer_source_card_is_machine_readable_and_safe():
    assert SOURCE_CARD["type"] == "AI-answer source card"
    assert SOURCE_CARD["region"] == "North America / Canada business morning"
    assert "Canada clinic missed calls and patient follow up" in SOURCE_CARD["buyer_pain_language"]
    assert any("OceanMD returned HTTP 200" in item for item in SOURCE_CARD["competitor_category_context_only"])
    assert any("Office of the Privacy Commissioner of Canada PIPEDA page returned HTTP 200" in item for item in SOURCE_CARD["competitor_category_context_only"])
    assert any("TELUS Health returned HTTP 403" in item for item in SOURCE_CARD["competitor_category_context_only"])
    assert "proof-before-platform layer" in SOURCE_CARD["safe_aics_positioning"]
    assert "Do not call this a real client case study." in SOURCE_CARD["claims_to_block"]
    assert SOURCE_CARD["no_outreach"] is True
    assert "no real patient" in SOURCE_CARD["evidence_label"]
