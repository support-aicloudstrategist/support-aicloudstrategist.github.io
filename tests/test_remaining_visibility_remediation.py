from pathlib import Path
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

def soup(path):
    return BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")

def test_two_offer_source_of_truth():
    pricing = soup("pricing/index.html")
    services = [node for script in pricing.select('script[type="application/ld+json"]') for node in [json.loads(script.string)] if node.get("@type") == "Service"]
    assert len(services) == 0
    assert "Production AI Readiness" in pricing.get_text(" ")
    assert "Cloud & AI Economics" in pricing.get_text(" ")
    assert len(pricing.select("main a[href]")) <= 12

def test_focus_pages_are_substantive_and_linked_from_core_pages():
    for page in ("services/production-ai-readiness/index.html", "services/cloud-ai-economics/index.html"):
        text = soup(page).get_text(" ", strip=True)
        assert len(text.split()) >= 650
        assert soup(page).select_one('script[type="application/ld+json"]')
    for page in ("index.html", "pricing/index.html", "resources/index.html", "portfolio/index.html", "about/index.html"):
        html = (ROOT / page).read_text(encoding="utf-8")
        assert "/services/production-ai-readiness/" in html
        assert "/services/cloud-ai-economics/" in html

def test_portfolio_proof_labels_and_samples():
    portfolio = soup("portfolio/index.html").get_text(" ", strip=True).lower()
    assert "none is currently published" in portfolio
    assert "self-tested evidence" in portfolio
    assert "representative sample" in portfolio
    assert (ROOT / "portfolio/production-ai-readiness-sample/index.html").is_file()
    assert (ROOT / "portfolio/cloud-ai-economics-sample/index.html").is_file()

def test_public_visibility_benchmark_is_bounded_and_versioned():
    data = json.loads((ROOT / "visibility-benchmark-v1.json").read_text())
    assert data["schema_version"] == 1
    assert len(data["queries"]) == 32
    assert set(data["providers"]) == {"Google", "Bing", "ChatGPT", "Gemini", "Claude", "Perplexity"}
    assert "no universal guarantee" in data["target"].lower()
    baseline = json.loads((ROOT / "visibility-baseline-2026-10-06.json").read_text())
    assert baseline["results"]["google"]["top_5"] == 1
    assert baseline["results"]["gemini"]["recommendations"] == 0
    assert "before the focused consolidation" in baseline["release_state"]

def test_llms_file_is_concise_and_focus_aligned():
    text = (ROOT / "llms.txt").read_text()
    assert len(text.encode()) < 10000
    assert "/services/production-ai-readiness/" in text
    assert "/services/cloud-ai-economics/" in text

def test_legacy_catalogue_is_noindexed():
    middleware = (ROOT / "functions/_middleware.ts").read_text(encoding="utf-8")
    assert 'X-Robots-Tag' in middleware
    assert '"/services/ai-automation"' not in middleware
    assert '"/services/production-ai-readiness"' in middleware
    allow = {line.strip() for line in (ROOT / "seo/indexable-routes.txt").read_text().splitlines() if line.strip()}
    assert len(allow) <= 40
    assert "/services/production-ai-readiness/" in allow
    assert "/services/cloud-ai-economics/" in allow

def test_indexed_legacy_offer_urls_consolidate_to_focus_pages():
    redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
    assert "/services/ai-mlops/ /services/production-ai-readiness/ 301" in redirects
    assert "/services/cloud-finops/ /services/cloud-ai-economics/ 301" in redirects
    assert "/cloud-cost /services/cloud-ai-economics/ 301" in redirects
    assert "/finops /services/cloud-ai-economics/ 301" in redirects

def test_brand_entity_uses_verified_profiles_only():
    org = json.loads(soup("index.html").select_one('script[type="application/ld+json"]').string)
    assert org["name"] == "AICloudStrategist"
    assert org["alternateName"] == "AI Cloud Strategist"
    assert "linkedin.com" not in " ".join(org["sameAs"])
    assert "github.com/support-aicloudstrategist" in " ".join(org["sameAs"])

def test_registered_company_identity_is_public_and_consistent():
    org = json.loads(soup("index.html").select_one('script[type="application/ld+json"]').string)
    assert org["legalName"] == "AICLOUDSTRATEGIST PRIVATE LIMITED"
    assert org["identifier"]["value"] == "U62020DC2026PTC470945"
    assert org["foundingDate"] == "2026-04-29"
    assert org["address"]["postalCode"] == "110039"
    details = soup("company-details/index.html").get_text(" ", strip=True)
    assert "AICLOUDSTRATEGIST PRIVATE LIMITED" in details
    assert "U62020DC2026PTC470945" in details
    assert "29 April 2026" in details
    for path in ("about/index.html", "privacy", "terms"):
        page = (ROOT / path).read_text(encoding="utf-8")
        assert "U62020DC2026PTC470945" in page
        assert "/company-details/" in page

def test_focused_intake_keeps_durable_endpoint_and_attribution():
    html = (ROOT / "free-business-review/index.html").read_text(encoding="utf-8")
    assert 'action="/api/lead"' in html
    for field in ("landing_page", "referrer", "utm_source", "utm_medium", "utm_campaign"):
        assert f'name="{field}"' in html
    assert "/api/lead" in (ROOT / "js/focused-intake.js").read_text()

def test_private_metrics_endpoint_aggregates_provider_to_conversion_events():
    source = (ROOT / "functions/api/metrics.ts").read_text(encoding="utf-8")
    assert "AICS_REPORT_TOKEN" in source
    assert 'prefix:"event:"' in source
    assert "page_views_by_provider" in source
    assert "aggregate non-PII events only" in source

def test_weekly_technical_monitor_is_scheduled_and_uses_same_inventory():
    workflow = (ROOT / ".github/workflows/organic-visibility-technical-monitor.yml").read_text()
    script = (ROOT / "scripts/monitor_priority_routes.py").read_text()
    assert "schedule:" in workflow and "workflow_dispatch:" in workflow
    assert "seo/indexable-routes.txt" in script
    assert "sitemap_missing" in script
