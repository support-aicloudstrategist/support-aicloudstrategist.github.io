import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-generated-marketing-creative-approval-checklist"
URL = "https://aicloudstrategist.com/resources/" + SLUG + "/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-generated-marketing-creative-approval-register.csv"
SVG = ROOT / "resources" / SLUG / "ai-creative-approval-board.svg"


def html():
    return PAGE.read_text(encoding="utf-8")


def docs(source):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_page_indexable_schema_and_search_markers():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"/>' in source
    assert source.count("<h1>") == 1
    assert source.count('data-aics-navigation-mount') == 1
    assert source.count('data-aics-global-footer') == 1
    types = {d.get("@type") for d in docs(source) if isinstance(d, dict)}
    assert {"Article", "Dataset", "ImageObject", "FAQPage", "BreadcrumbList"}.issubset(types)
    article = next(d for d in docs(source) if isinstance(d, dict) and d.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-04"
    for marker in [
        "AI generated ad creative approval checklist",
        "AI marketing content brand safety review",
        "AI advertisement claims approval workflow",
        "proof-before-publication marketing assets",
    ]:
        assert marker in article["about"]


def test_asset_links_and_top_five_wedge():
    source = html()
    for marker in [
        "AICS top-3/top-5 wedge",
        "brand-safe outputs",
        "claim boundaries",
        "AI Creative Studio",
        "ai-generated-marketing-creative-approval-register.csv",
        "ai-creative-approval-board.svg",
    ]:
        assert marker in source


def test_claim_boundaries_block_fake_campaign_proof():
    source = html().lower()
    for marker in [
        "synthetic buyer-education checklist only",
        "not a real client campaign",
        "not customer data",
        "not ad-account data",
        "not a platform approval",
        "not legal advice",
        "not advertising advice",
        "not ip advice",
        "not compliance advice",
        "not a guarantee of ad approval",
        "not a performance claim",
        "no outreach, dms, cold emails or contact-form submissions were sent",
    ]:
        assert marker in source
    for forbidden in ["trusted by", "guaranteed leads", "real client results", "increased conversion"]:
        assert forbidden not in source


def test_csv_and_svg_are_synthetic_owner_usable():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 6
    assert set(rows[0]) == {
        "asset_or_campaign",
        "buyer_pain_question",
        "evidence_to_collect_before_publish",
        "human_owner_or_reviewer",
        "next_safe_action",
        "blocked_claim",
        "boundary_label",
    }
    text = CSV.read_text(encoding="utf-8")
    for marker in [
        "Synthetic row only",
        "no customer ad-account personal production or platform data",
        "No guaranteed sales leads revenue ROI platform approval or compliance",
        "No legal advertising compliance medical financial or security advice",
    ]:
        assert marker in text
    svg = SVG.read_text(encoding="utf-8")
    assert "Demo AI creative approval board" in svg
    assert "No customer data" in svg
