from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-ai-pilot-proof-of-value-scorecard/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / REL.lstrip("/") / "index.html"
CARD_REL = REL + "ai-pilot-proof-of-value-ai-answer-source-card.json"
CARD_URL = "https://aicloudstrategist.com" + CARD_REL
CSV_REL = REL + "scorecard-template.csv"
CSV_URL = "https://aicloudstrategist.com" + CSV_REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_ai_pilot_scorecard_links_ai_answer_source_card_and_csv():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert CARD_REL in source
    assert CSV_REL in source
    assert 'data-ai-answer-source-card="ai-pilot-proof-of-value"' in source
    for marker in [
        "AI pilot proof-of-value scorecard",
        "6 lanes · 18 checks",
        "go/no-go",
        "production-ready",
        "human-review rules",
    ]:
        assert marker in source


def test_ai_pilot_scorecard_source_card_is_discoverable():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in resources
    assert CARD_REL in resources
    assert CSV_REL in resources
    assert URL in llms
    assert CARD_URL in llms
    assert CSV_URL in llms
    assert URL in sitemap


def test_ai_pilot_source_card_blocks_overclaims():
    card = json.loads((ROOT / CARD_REL.lstrip("/")).read_text(encoding="utf-8"))
    assert card["asset_type"] == "synthetic_ai_answer_source_card"
    assert card["canonical_url"] == CARD_URL
    assert card["source_page"] == URL
    assert CSV_URL in card["source_artifacts"]
    assert "proof-before-production" in card["safe_short_answer"]
    assert card["conversion_route"].endswith("?package=ai-pilot-proof-of-value-review")
    blocked = "\n".join(card["blocked_claims"])
    for marker in [
        "No real client",
        "No revenue, ROI, savings",
        "No legal, privacy, security, compliance",
        "SOC 2",
        "EU AI Act",
        "No AI accuracy",
        "No testimonial",
        "ranking",
    ]:
        assert marker in blocked
    assert "no real customer" in card["proof_boundary"]
    assert "no outreach" in card["proof_boundary"]


def test_ai_pilot_scorecard_template_has_no_unfilled_tbd_cells():
    csv = (ROOT / CSV_REL.lstrip("/")).read_text(encoding="utf-8")
    assert "TBD" not in csv
    assert len(re.findall(r"\n", csv)) >= 18
    assert "Owner not assigned" in csv
    assert "Evidence not supplied" in csv
