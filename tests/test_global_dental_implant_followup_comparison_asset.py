from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-dental-implant-follow-up-vs-crm-ai-receptionist-comparison"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
CSV = (ROOT / "resources" / SLUG / "dental-implant-follow-up-comparison-matrix.csv").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_dental_implant_comparison_is_indexable_and_buyer_safe():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "Dental Implant Follow-up vs CRM and AI Receptionist Comparison" in PAGE
    assert "dental implant leads not converting" in PAGE
    assert "synthetic buyer-education comparison" in PAGE
    assert "vendor ranking" in PAGE
    assert "No outreach was sent" in PAGE
    assert "rankings, AI-answer inclusion, impressions, clicks, demand, leads, customers and revenue remain unverified" in PAGE
    assert url in SITEMAP


def test_dental_implant_comparison_csv_and_discovery_links_exist():
    href = f"/resources/{SLUG}/"
    csv_href = f"/resources/{SLUG}/dental-implant-follow-up-comparison-matrix.csv"
    assert href in RESOURCES
    assert "CRM, AI receptionist, call centre and agency" in RESOURCES
    assert f"https://aicloudstrategist.com{href}" in LLMS
    assert f"https://aicloudstrategist.com{csv_href}" in LLMS
    assert "route,best_fit,risk_if_used_too_early,owner_evidence_needed,claim_boundary" in CSV
    assert "AICS owner-evidence review" in CSV
    assert "No conversion revenue or treatment acceptance claim" in CSV
