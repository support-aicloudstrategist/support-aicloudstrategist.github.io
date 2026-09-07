import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "search-console-indexing-readiness"
REL = f"/resources/{SLUG}/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "search-console-indexing-readiness-boundary.csv"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_indexing_boundary_page_is_indexable_and_buyer_safe():
    source = html()
    assert '<meta name="robots" content="index, follow, max-image-preview:large" />' in source
    assert f'<link rel="canonical" href="{URL}" />' in source
    assert source.count("<h1>") == 1
    assert source.count("data-aics-navigation-mount") == 1
    for marker in [
        "website is not showing in Google",
        "Search Console indexing readiness",
        "No-login SEO trust boundary",
        "Request a no-login discovery review",
        "Download boundary CSV",
        "proof-before-SEO-spend",
    ]:
        assert marker in source


def test_schema_and_dataset_are_machine_readable():
    docs = json_ld_documents(html())
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "Dataset", "FAQPage"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-07"
    assert "Search Console indexing readiness" in article["about"]
    dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
    assert dataset["url"] == URL + "search-console-indexing-readiness-boundary.csv"


def test_csv_separates_public_checks_from_unverified_metrics():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 8
    assert set(rows[0]) == {
        "check_area",
        "owner_question",
        "public_no_login_evidence",
        "requires_owner_telemetry",
        "claim_boundary",
        "next_owner_action",
    }
    text = CSV.read_text(encoding="utf-8")
    for marker in [
        "Synthetic readiness only; not proof of Google indexing",
        "Do not claim indexing impressions clicks CTR average position or query coverage without owner telemetry",
        "Do not claim traffic lead customer revenue savings or ROI impact without analytics/CRM evidence",
    ]:
        assert marker in text


def test_claim_boundaries_and_discovery_surfaces_are_wired():
    source = html()
    for forbidden in [
        "guaranteed ranking",
        "ranking #1",
        "proven traffic growth",
        "increased leads",
        "revenue results",
    ]:
        assert forbidden not in source.lower()
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert REL in resources
    assert URL in llms
    assert "search-console-indexing-readiness-boundary.csv" in llms
    assert f'"{REL}"' in sitemap_script
    assert REL in (ROOT / "resources" / "website-not-showing-google-indexing-checklist" / "index.html").read_text(encoding="utf-8")
