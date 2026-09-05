from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-05"
SLUG = "ai-reply-readiness-checkpoints"
URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html"
CSV_URL = f"https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv"
PATH = f"/publications/{DATE}/{SLUG}.html"
CSV_PATH = f"/publications/{DATE}/{SLUG}.csv"
PNG_PATH = f"/publications/{DATE}/{SLUG}.png"


def test_resources_hub_surfaces_ai_reply_readiness_publication():
    html = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert 'data-featured-publication="ai-reply-readiness-checkpoints"' in html
    assert PATH in html
    assert CSV_PATH in html
    assert PNG_PATH in html
    assert "AI Reply Readiness: 7 Checkpoints Before a Bot Answers" in html
    assert "narrow, sourced, reversible and ready for customer-facing use" in html


def test_ai_reply_readiness_publication_assets_are_discoverable_and_claim_safe():
    page = (ROOT / "publications" / DATE / f"{SLUG}.html").read_text(encoding="utf-8")
    csv = (ROOT / "publications" / DATE / f"{SLUG}.csv").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert f"<link rel='canonical' href='{URL}'>" in page
    assert "customer-result, approval, or guaranteed-performance advice" in page
    assert "checkpoint,owner_question,safe_output" in csv
    assert URL in llms
    assert CSV_URL in llms
    assert f"<loc>{URL}</loc>" in sitemap
    for forbidden in ["trusted by", "increased revenue", "guaranteed compliance"]:
        assert forbidden not in page.lower()
