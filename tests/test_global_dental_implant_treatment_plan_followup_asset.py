from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-dental-implant-treatment-plan-follow-up-evidence-checklist"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
CSV = (ROOT / "resources" / SLUG / "dental-implant-treatment-plan-follow-up-synthetic.csv").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_dental_implant_asset_is_indexable_buyer_safe_and_commercial():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "Dental Implant Treatment Plan Follow-up Evidence Checklist" in PAGE
    assert "implant leads not converting" in PAGE
    assert "AI receptionist for dental clinic" in PAGE
    assert "simulated proof-of-method" in PAGE
    assert "not a real client case study" in PAGE
    assert "No outreach was sent" in PAGE
    assert "No real clinic, patient, dentist" in PAGE
    assert "No conversion revenue or treatment acceptance claim" in CSV
    assert url in SITEMAP


def test_dental_implant_csv_and_discovery_links_exist():
    href = f"/resources/{SLUG}/"
    csv_href = f"/resources/{SLUG}/dental-implant-treatment-plan-follow-up-synthetic.csv"
    assert href in RESOURCES
    assert "implant consults, treatment-plan estimates" in RESOURCES
    assert f"https://aicloudstrategist.com{href}" in LLMS
    assert f"https://aicloudstrategist.com{csv_href}" in LLMS
    assert "buyer_pain_phrase,lead_or_followup_stage,owner_evidence_needed" in CSV
    assert "finance handoff" in CSV
    assert "No clinical suitability claim" in CSV
    assert CSV.count("\n") >= 14
