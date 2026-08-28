import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-saas-customer-onboarding-implementation-delay-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / f"{SLUG}.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def json_ld_documents(html):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_onboarding_delay_page_has_downloadable_dataset_and_structured_data():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert html.count("<h1>") == 1
    assert f"/{SLUG}.csv" in html
    docs = json_ld_documents(html)
    assert any(doc.get("@type") == "Article" and doc.get("mainEntityOfPage") == URL for doc in docs)
    assert any(doc.get("@type") == "Dataset" and doc.get("url", "").endswith(f"/{SLUG}.csv") for doc in docs)
    assert any(doc.get("@type") == "FAQPage" for doc in docs)


def test_onboarding_delay_csv_is_redaction_first_and_claim_safe():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) >= 8
    assert rows[0].keys() == {
        "implementation_stage",
        "delay_signal",
        "blocker_type",
        "accountable_owner",
        "redacted_evidence",
        "next_action",
        "unsafe_claim_boundary",
    }
    csv_text = CSV.read_text(encoding="utf-8")
    for phrase in [
        "Do not request or store passwords, tokens or production secrets",
        "Do not claim onboarding accelerated, retention improved or revenue protected",
        "Do not claim churn reduction, renewal saved, ROI or customer outcome proof",
    ]:
        assert phrase in csv_text


def test_onboarding_delay_discovery_surfaces_are_wired():
    assert PATH in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{PATH}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
