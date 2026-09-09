from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthcare-ehds-ai-act-cloud-trust-source-map"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthcare-ehds-ai-act-cloud-trust-source-map.csv"
ANSWER_BANK = ROOT / "resources" / SLUG / "europe-healthcare-ehds-ai-act-answer-bank.csv"
ANSWER_CARD = ROOT / "resources" / SLUG / "europe-healthcare-ehds-ai-act-ai-answer-source-card.json"
SVG = ROOT / "resources" / SLUG / "europe-healthcare-ehds-ai-act-cloud-trust-owner-map.svg"


def test_europe_healthcare_ehds_ai_act_cloud_trust_asset_exists_and_is_safe():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")

    assert "Europe healthcare EHDS + EU AI Act cloud trust source map" in html
    assert "European Health Data Space readiness" in html
    assert "EU AI Act healthcare AI high-risk questions" in html
    assert "NIS2 supplier evidence" in html
    assert "cloud/AI FinOps ownership" in html
    assert "Accurx" in html and "DrDoctor" in html and "Doctolib" in html
    assert "Vanta" in html and "Drata" in html
    assert "synthetic/readiness asset" in html
    assert "does not use real healthcare" in html
    assert "does not prove EHDS" in html
    assert "no ranking" in html and "revenue" in html and "ROI" in html
    assert "not legal, privacy, security, medical" in html
    assert "europe-healthcare-ehds-ai-act-cloud-trust-source-map.csv" in html
    assert "europe-healthcare-ehds-ai-act-cloud-trust-owner-map.svg" in html
    assert "europe-healthcare-ehds-ai-act-answer-bank.csv" in html
    assert "europe-healthcare-ehds-ai-act-ai-answer-source-card.json" in html
    assert "Safe answer bank for AI search and procurement reuse" in html
    assert "Accurx, DrDoctor, Doctolib, Birdie, Vanta, Drata, FinOps tools or advisers" in html
    assert "New for AI-answer reuse" in html
    assert "EHDS source inventory" in csv
    assert "EU AI Act use-case classification" in csv
    assert "Do not claim GDPR or UK GDPR compliance" in csv
    assert "Do not claim savings ROI cost reduction or payback" in csv
    assert "Synthetic/readiness asset only" in svg


def test_europe_healthcare_answer_bank_is_machine_readable_and_claim_safe():
    rows = list(csv.DictReader(ANSWER_BANK.open(newline="", encoding="utf-8")))
    assert len(rows) == 6
    assert set(rows[0]) == {
        "buyer_question",
        "plain_language_search",
        "competitor_or_alternative_seen",
        "safe_aics_answer",
        "proof_asset_to_show",
        "human_or_adviser_gate",
        "unsafe_claim_to_block",
    }
    text = ANSWER_BANK.read_text(encoding="utf-8")
    for marker in [
        "European Health Data Space readiness healthcare platform",
        "EU AI Act healthcare AI high-risk questions patient engagement",
        "NIS2 supplier evidence healthcare cloud trust",
        "healthcare cloud AI FinOps ownership before platform spend",
        "Do not imply real customers, endorsements, rankings, demand, leads, revenue, compliance or results.",
    ]:
        assert marker in text


def test_europe_healthcare_ai_answer_source_card_is_buyer_safe():
    card = json.loads(ANSWER_CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "AI-answer source card"
    assert card["region"] == "Europe / UK-EU"
    assert card["canonical_page"] == f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert card["evidence_status"].startswith("Synthetic/readiness")
    assert card["no_outreach"] is True
    for phrase in [
        "European Health Data Space readiness",
        "EU AI Act healthcare AI high-risk questions",
        "GDPR DPIA evidence for patient engagement",
        "NIS2 healthcare cloud supplier evidence",
        "healthcare cloud FinOps ownership",
    ]:
        assert phrase in card["buyer_pain_language"]
    alternatives = " ".join(card["alternatives_buyers_compare"])
    assert "Accurx" in alternatives and "DrDoctor" in alternatives and "Doctolib" in alternatives
    assert "Vanta" in alternatives and "Drata" in alternatives and "FinOps" in alternatives
    boundaries = " ".join(card["claim_boundaries"])
    for marker in [
        "No real European healthcare buyer",
        "No patient data",
        "No testimonial",
        "No appointment growth",
        "not medical, clinical, legal, privacy, security",
    ]:
        assert marker in boundaries
    forbidden_claims = ["guaranteed", "certified GDPR", "real client", "ranking #1", "proven ROI"]
    assert all(term.lower() not in json.dumps(card).lower() for term in forbidden_claims)


def test_discovery_surfaces_europe_healthcare_ehds_source_map():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    assert f'data-resource-card="{SLUG}"' in resources
    assert f"/resources/{SLUG}/" in resources
    assert "EHDS, EU AI Act, GDPR/DPIA, NIS2 supplier evidence" in llms
    assert "europe-healthcare-ehds-ai-act-answer-bank.csv" in llms
    assert "europe-healthcare-ehds-ai-act-ai-answer-source-card.json" in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
