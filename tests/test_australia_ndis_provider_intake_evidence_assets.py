import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "australia-ndis-provider-missed-calls-participant-intake-checklist"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "australia-ndis-intake-owner-evidence.csv"
SVG = ROOT / "resources" / SLUG / "australia-ndis-intake-owner-dashboard.svg"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_australia_ndis_intake_asset_has_downloadable_owner_evidence():
    html = PAGE.read_text(encoding="utf-8")
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    svg = SVG.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert "NDIS provider missed calls" in html
    assert "participant enquiry follow-up" in html
    assert "australia-ndis-intake-owner-evidence.csv" in html
    assert "australia-ndis-intake-owner-dashboard.svg" in html
    assert len(rows) == 6
    assert set(rows[0]) == {
        "intake_signal",
        "buyer_question",
        "redacted_evidence_to_collect",
        "accountable_owner",
        "safe_next_step",
        "unsafe_claim_boundary",
    }
    assert all("Synthetic row only" in row["unsafe_claim_boundary"] for row in rows)
    assert "DEMO / SYNTHETIC ONLY" in svg
    assert "no participant data" in svg
    assert "No NDIS compliance conclusion" in svg


def test_australia_ndis_asset_schema_discovery_and_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    docs = json_ld_documents(html)
    types = {doc.get("@type") for doc in docs if isinstance(doc, dict)}
    assert {"Article", "FAQPage", "Dataset", "ImageObject"}.issubset(types)
    article = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert article["dateModified"] == "2026-09-03"
    dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset")
    image = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "ImageObject")
    assert dataset["url"] == f"{URL}australia-ndis-intake-owner-evidence.csv"
    assert image["contentUrl"] == f"{URL}australia-ndis-intake-owner-dashboard.svg"
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert f"{URL}australia-ndis-intake-owner-evidence.csv" in llms
    assert f"{URL}australia-ndis-intake-owner-dashboard.svg" in llms
    assert URL in sitemap
    assert f"/resources/{SLUG}/" in resources
    for phrase in [
        "not a real customer case study",
        "not proof of participant outcomes",
        "NDIS quality/safeguarding compliance",
        "No real Australian NDIS provider",
        "No outreach was sent",
    ]:
        assert phrase in html
    forbidden = ["guaranteed revenue", "trusted by", "certified partner", "100% conversion", "real client results"]
    assert all(term not in html.lower() for term in forbidden)
