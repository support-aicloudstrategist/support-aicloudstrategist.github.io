from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-private-clinic-ai-receptionist-vs-practice-management-patient-growthos-comparison"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
CSV = (ROOT / "resources" / SLUG / "uk-private-clinic-patient-growthos-comparison.csv").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_uk_private_clinic_comparison_is_indexable_buyer_safe_and_researched():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "UK Private Clinic AI Receptionist vs Practice Management and Patient GrowthOS" in PAGE
    assert "Europe / UK buyer research snapshot" in PAGE
    assert "Meddbase no-show and appointment-scheduling pages" in PAGE
    assert "Medesk no-show/online-booking content" in PAGE
    assert "Motics Phone Agent, Ivy by Verbalise and Aeva AI" in PAGE
    assert "Article 28 DPAs" in PAGE
    assert "no medical-advice design and instant human handover" in PAGE
    assert "No outreach was sent" in PAGE
    assert "not a real client case study" in PAGE
    assert "No no-show, booking, revenue, ranking or compliance claims" in PAGE
    assert url in SITEMAP


def test_uk_private_clinic_comparison_csv_and_discovery_links_exist():
    href = f"/resources/{SLUG}/"
    csv_href = f"/resources/{SLUG}/uk-private-clinic-patient-growthos-comparison.csv"
    assert href in RESOURCES
    assert "UK Private Clinic AI Receptionist vs Practice Management and Patient GrowthOS" in RESOURCES
    assert f"https://aicloudstrategist.com{href}" in LLMS
    assert f"https://aicloudstrategist.com{csv_href}" in LLMS
    assert "route,best_fit,blind_spot,aics_owner_evidence_wedge,unsafe_claim_boundary" in CSV
    assert "AI receptionist or voice agent" in CSV
    assert "Practice-management or clinic operating system" in CSV
    assert "AICS Patient GrowthOS owner-evidence review" in CSV
    assert "No clinical safety, GDPR compliance, no-show reduction, booking growth or ROI claim" in CSV
