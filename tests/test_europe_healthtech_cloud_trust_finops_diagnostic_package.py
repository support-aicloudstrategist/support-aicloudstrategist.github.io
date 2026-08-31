from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthtech-cloud-trust-finops-diagnostic-package"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_europe_healthtech_cloud_trust_finops_diagnostic_is_indexable_and_buyer_safe():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "Europe Healthtech Cloud Trust + FinOps Diagnostic Package" in PAGE
    assert "fixed-scope evidence package" in PAGE
    assert "GDPR/DPIA adviser-question" in PAGE
    assert "cloud/AI spend owners" in PAGE
    assert "vendor-risk blockers" in PAGE
    assert "human-review boundaries" in PAGE
    assert "no patient data" in PAGE.lower()
    assert "No outreach was sent" in PAGE
    for forbidden in ("testimonial", "guarantee", "savings claim", "ROI claim", "compliance opinion"):
        assert forbidden in PAGE
    assert url in SITEMAP


def test_europe_healthtech_cloud_trust_finops_diagnostic_is_discoverable_and_sellable():
    href = f"/resources/{SLUG}/"
    assert href in RESOURCES
    assert "Europe Healthtech Cloud Trust + FinOps Diagnostic Package" in RESOURCES
    assert href in PRICING
    assert "Twenty concrete first offers" in PRICING
    assert 'numberOfItems":20' in PRICING
    assert "Scope before quote" in PRICING
    assert "europe-healthtech-cloud-trust-finops-diagnostic" in PRICING
