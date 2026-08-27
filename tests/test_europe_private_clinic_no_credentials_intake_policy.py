from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-private-clinic-no-credentials-intake-policy"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / "europe-private-clinic-patient-growthos-intake-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_policy_page_exists_with_seo_and_schema():
    html = text(PAGE)
    assert "Europe Private Clinic No-Credentials Intake Policy" in html
    assert f'<link rel="canonical" href="{URL}"' in html
    assert '"@type":"Article"' in html
    assert '"@type":"FAQPage"' in html
    for phrase in [
        "no live credentials",
        "redacted evidence",
        "GDPR appointment reminder evidence",
        "AI receptionist human handoff",
        "Patient GrowthOS reviews",
    ]:
        assert phrase in html


def test_research_competitor_language_and_top_consideration_gap_are_present():
    html = text(PAGE)
    for competitor in ["Accurx", "Pabau", "Semble", "Cliniko", "Doctolib"]:
        assert competitor in html
    for phrase in [
        "What AICS must publish/build next for top-3/top-5 consideration",
        "Downloadable redaction templates",
        "Trust-room structure",
        "Comparison backlinks",
        "Demo evidence",
    ]:
        assert phrase in html


def test_no_credentials_policy_blocks_sensitive_default_intake_and_fake_claims():
    html = text(PAGE)
    required_boundaries = [
        "not a real clinic case study",
        "not patient data",
        "not production access proof",
        "not legal advice",
        "not privacy advice",
        "not clinical advice",
        "not GDPR/UK GDPR/RGPD compliance proof",
        "not certification",
        "not revenue evidence",
        "No customer outreach was sent",
        "Admin login to CMS, booking platform, EHR or practice-management software",
        "Patient names, phone numbers, symptoms, diagnoses, recordings or raw mailbox exports",
    ]
    for phrase in required_boundaries:
        assert phrase in html
    forbidden = [
        "trusted by European clinics",
        "guaranteed appointments",
        "guaranteed no-show reduction",
        "GDPR certified",
        "real clinic results",
    ]
    lower = html.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lower


def test_csv_template_is_redaction_first_and_linked_from_llms_resources_sitemap():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    fields = {row["field"] for row in rows}
    assert {"source_channel", "adviser_question_flag", "ai_human_boundary_flag", "evidence_link_or_screenshot_id"}.issubset(fields)
    redaction = "\n".join(row["redaction_rule"] for row in rows)
    assert "Do not include patient name" in redaction
    assert "Do not include symptom text" in redaction
    assert f"/resources/{SLUG}/" in text(ROOT / "resources" / "index.html")
    assert URL in text(ROOT / "llms.txt")
    assert f"/resources/{SLUG}/" in text(ROOT / "scripts" / "build_sitemap.py")


def test_existing_europe_patient_growthos_comparison_links_to_policy():
    comparison = text(ROOT / "resources" / "europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison" / "index.html")
    assert f"/resources/{SLUG}/" in comparison
