from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
SLUG = "global-b2b-saas-customer-onboarding-implementation-delay-checklist"
RESOURCE = ROOT / "resources" / SLUG / "index.html"


def test_homepage_surfaces_b2b_saas_onboarding_delay_owner_dashboard_asset():
    home = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")
    href = f"/resources/{SLUG}/"

    assert 'data-homepage-resource="b2b-saas-onboarding-delay-owner-dashboard"' in home
    assert href in home
    assert "B2B SaaS Customer Onboarding Implementation Delay Checklist" in home
    assert "sales-to-CS handoffs, kickoff, data migration, integrations, security review" in home
    assert "before more CS platform or AI follow-up spend" in home

    assert "no real SaaS client" in resource
    assert "not customer proof" in resource
    assert "faster onboarding" in resource
    assert "Request the diagnostic fit check" in resource
