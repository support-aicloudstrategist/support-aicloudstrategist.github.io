from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-vendor-claim-reality-check-procurement-packet"
URL = "https://aicloudstrategist.com/resources/global-ai-vendor-claim-reality-check-procurement-packet/"

def test_procurement_packet_resource_and_files_exist():
    page = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
    assert "AI Vendor Claim Reality-Check Procurement Packet" in page
    assert "Request vendor-claim fit check" in page
    assert "no customer data, credentials" in page
    card = json.loads((ROOT / "resources" / SLUG / "ai-vendor-claim-reality-check-source-card.json").read_text(encoding="utf-8"))
    assert card["url"] == URL
    assert "no vendor ranking" in card["claim_boundaries"]
    csv = (ROOT / "resources" / SLUG / "ai-vendor-claim-reality-check-procurement-questions.csv").read_text(encoding="utf-8")
    assert "Outcome promise" in csv and "Portability" in csv

def test_resource_cta_routes_to_free_review():
    html = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
    assert f"/free-business-review/?package={SLUG}&amp;source=resource" in html
    assert f"/free-business-review/?package={SLUG}&amp;source=resource-bottom" in html

def test_resources_hub_and_sitemap_reference_packet():
    assert f'/resources/{SLUG}/' in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
