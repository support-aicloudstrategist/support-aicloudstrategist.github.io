import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "saudi-healthtech-cloud-trust-nphies-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "saudi-healthtech-cloud-trust-nphies-owner-evidence-checklist.csv"
CARD = ROOT / "resources" / SLUG / "saudi-healthtech-nphies-cloud-trust-ai-answer-source-card.json"


def test_saudi_healthtech_nphies_page_exists_with_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "Saudi Healthtech Cloud Trust + NPHIES Owner Evidence Checklist" in html
    assert "Buyer pain-language targeted" in html
    assert "NPHIES-adjacent workflow evidence" in html
    assert "What a top-5 credible answer must publish" in html
    assert "not a real Saudi hospital" in html
    assert "not NPHIES implementation evidence" in html
    assert "No outreach was sent" in html
    assert "not savings evidence" in html
    assert "not ranking evidence" in html


def test_saudi_healthtech_nphies_downloads_are_synthetic_and_safe():
    csv = CSV.read_text(encoding="utf-8")
    assert "NPHIES-adjacent workflow" in csv
    assert "No credentials tokens or production exports" in csv
    assert "Not NPHIES certification or implementation evidence" in csv
    data = json.loads(CARD.read_text(encoding="utf-8"))
    assert data["synthetic_only"] is True
    assert data["not_real_client_evidence"] is True
    assert data["no_outreach_sent"] is True
    assert "No claim of Saudi clients" in " ".join(data["positioning_boundaries"])


def test_saudi_healthtech_nphies_discoverability_wiring():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert f'/resources/{SLUG}/' in resources
    assert f'https://aicloudstrategist.com/resources/{SLUG}/' in sitemap
    assert f'https://aicloudstrategist.com/resources/{SLUG}/' in llms
    assert "saudi-healthtech-nphies-cloud-trust-ai-answer-source-card.json" in llms
