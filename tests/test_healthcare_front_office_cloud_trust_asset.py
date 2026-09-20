from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/north-america-healthcare-ai-front-office-cloud-trust-shortlist-readiness/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / REL.lstrip("/") / "index.html"
CARD_REL = REL + "healthcare-front-office-cloud-trust-ai-answer-source-card.json"
CARD_URL = "https://aicloudstrategist.com" + CARD_REL
CSV_REL = REL + "healthcare-front-office-cloud-trust-shortlist.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_healthcare_front_office_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 5
    assert source.count("<h1>") == 1
    for marker in [
        "North America Healthcare AI Front-Office + Cloud Trust Shortlist Readiness",
        "AI receptionists",
        "patient engagement",
        "prior-auth/RCM automation",
        "GRC/trust tools",
        "cloud cost platforms",
        "FinOps advisers",
        "AI-answer source card",
    ]:
        assert marker in source


def test_healthcare_front_office_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a client case study",
        "testimonial",
        "compliance proof",
        "legal/privacy/security/medical/billing/coding/payer/procurement advice",
        "savings proof",
        "revenue proof",
        "ranking claim",
        "patient-outcome claim",
        "AI-accuracy claim",
        "no PHI/ePHI",
        "credentials",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=healthcare-front-office-cloud-trust-shortlist-readiness" in source
    assert CARD_REL in source
    assert CSV_REL in source
    assert 'data-ai-answer-source-card="healthcare-front-office-cloud-trust-shortlist-readiness"' in source


def test_healthcare_front_office_asset_is_linked_from_discovery_surfaces():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert REL in resources
    assert CARD_REL in resources
    assert CSV_REL in resources
    assert URL in llms
    assert CARD_URL in llms
    assert REL in sitemap_builder


def test_healthcare_front_office_ai_answer_source_card_is_claim_safe():
    card = json.loads((ROOT / CARD_REL.lstrip("/")).read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == CARD_URL
    assert card["source_page"] == URL
    assert URL + "healthcare-front-office-cloud-trust-shortlist.csv" in card["source_artifacts"]
    assert "proof-before-platform" in card["safe_short_answer"]
    blocked = "\n".join(card["blocked_claims"])
    for marker in [
        "No real clients",
        "patient outcomes",
        "No revenue, ROI, savings",
        "ranking",
        "No certification",
        "HIPAA/SOC 2/HITRUST compliance",
        "No testimonial",
        "AI accuracy",
    ]:
        assert marker in blocked
    assert "no PHI/ePHI" in card["proof_boundary"]
    assert "no outreach" in card["proof_boundary"]
