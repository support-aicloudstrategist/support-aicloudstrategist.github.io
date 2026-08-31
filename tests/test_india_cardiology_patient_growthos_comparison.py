from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-cardiology-patient-growthos-vs-clinic-software-whatsapp-crm-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_PATH = ROOT / "resources" / SLUG / "india-cardiology-patient-growthos-comparison.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_cardiology_comparison_page_has_seo_schema_and_buyer_language():
    html = text(PAGE)
    assert "India Cardiology Patient GrowthOS vs Clinic Software, LIS, WhatsApp CRM and AI Receptionists" in html
    assert f'<link rel="canonical" href="{URL}"' in html
    assert '"@type":"Article"' in html
    assert '"@type":"FAQPage"' in html
    for phrase in [
        "TMT appointment follow up",
        "Echo confirmation",
        "ECG/Holter report pickup",
        "TPA/pre-auth document chasing",
        "DPDP-safe intake",
        "top-3/top-5 shortlist credibility",
    ]:
        assert phrase in html


def test_cardiology_comparison_covers_shortlist_routes_without_ranking_claims():
    html = text(PAGE)
    for phrase in [
        "Clinic management software",
        "Practo Ray",
        "Eka Care",
        "Diagnostic LIS",
        "CrelioHealth",
        "MocDoc",
        "WhatsApp CRM",
        "AI receptionist",
        "Digital marketing agency",
    ]:
        assert phrase in html
    forbidden = [
        "best cardiology software",
        "ranked #1",
        "preferred partner",
        "we guarantee appointments",
        "we guarantee no-show reduction",
        "AICS is DPDP certified",
        "real clinic results prove",
    ]
    lower = html.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lower


def test_cardiology_comparison_truth_boundary_and_redaction_policy():
    html = text(PAGE)
    for phrase in [
        "buyer-education and proof-of-method comparison",
        "not a real cardiology clinic case study",
        "not patient data",
        "not production access proof",
        "not a testimonial",
        "not certification",
        "not DPDP compliance proof",
        "No customer outreach was sent",
        "Admin credentials, patient identifiers, reports, diagnoses and raw chat exports are not requested by default",
    ]:
        assert phrase in html


def test_cardiology_comparison_csv_and_discovery_links():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    assert len(rows) == 5
    assert {"route", "typical_strength", "gap_to_verify", "aics_patient_growthos_evidence", "redaction_boundary"}.issubset(rows[0])
    csv_text = CSV_PATH.read_text(encoding="utf-8")
    for phrase in ["Clinic management software", "Diagnostic LIS", "WhatsApp CRM", "AI receptionist", "Digital marketing"]:
        assert phrase in csv_text
    assert "No patient names" in csv_text
    assert f"/resources/{SLUG}/" in text(ROOT / "resources" / "index.html")
    assert URL in text(ROOT / "llms.txt")
    assert f"/resources/{SLUG}/" in text(ROOT / "scripts" / "build_sitemap.py")
