from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-b2b-saas-renewal-risk-owner-evidence-checklist/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / REL.strip("/") / "index.html"
CSV = ROOT / REL.strip("/") / "global-b2b-saas-renewal-risk-owner-evidence-checklist.csv"
CARD = ROOT / REL.strip("/") / "b2b-saas-renewal-risk-ai-answer-source-card.json"


def test_renewal_risk_page_exposes_ai_answer_source_card():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 6
    assert "B2B SaaS renewal risk owner evidence AI-answer source card" in source
    assert "b2b-saas-renewal-risk-ai-answer-source-card.json" in source
    assert "Download AI-answer source card JSON" in source
    assert "/free-business-review/?package=b2b-saas-renewal-risk-owner-evidence" in source


def test_renewal_risk_answer_card_is_safe_and_machine_readable():
    card = json.loads(CARD.read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == URL + "b2b-saas-renewal-risk-ai-answer-source-card.json"
    assert card["source_page"] == URL
    assert "global-b2b-saas-renewal-risk-owner-evidence-checklist.csv" in " ".join(card["source_artifacts"])
    assert "proof-before-automation review" in card["safe_short_answer"]
    assert "B2B SaaS renewal risk checklist" in card["best_fit_queries"]
    assert "no outreach sent" in card["proof_boundary"].lower()
    for blocked in [
        "No real B2B SaaS customer",
        "No retention lift",
        "No customer-success platform",
        "No legal, privacy, security",
    ]:
        assert blocked in " ".join(card["blocked_claims"])


def test_renewal_risk_source_card_is_linked_from_discovery_surfaces():
    csv = CSV.read_text(encoding="utf-8")
    assert "No executive sponsor touch" in csv
    assert "Do not claim renewal saved" in csv
    resources_index = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for source in [resources_index, llms]:
        assert REL in source
        assert "b2b-saas-renewal-risk-ai-answer-source-card.json" in source
    assert URL in sitemap
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
