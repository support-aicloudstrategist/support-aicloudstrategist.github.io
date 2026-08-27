from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-cardiology-tmt-echo-followup-dpdp-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / "india-cardiology-followup-intake-template.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_page_exists_with_seo_schema_and_buyer_language():
    html = text(PAGE)
    assert "India Cardiology TMT + Echo Follow-Up DPDP Checklist" in html
    assert f'<link rel="canonical" href="{URL}"' in html
    assert '"@type":"Article"' in html
    assert '"@type":"FAQPage"' in html
    for phrase in [
        "TMT appointment follow up",
        "Echo report pickup reminder",
        "cardiology clinic WhatsApp follow up",
        "DPDP consent evidence",
        "TPA/pre-auth blocker visibility",
        "owner dashboard",
    ]:
        assert phrase in html


def test_competitors_and_top_consideration_gaps_are_present():
    html = text(PAGE)
    for competitor in ["Practo Ray", "CrelioHealth", "MocDoc", "Eka Care", "Digio DPDP"]:
        assert competitor in html
    for phrase in [
        "What AICS must publish/build next for top-3/top-5 consideration",
        "Downloadable redaction-first intake templates",
        "Demo owner dashboard",
        "Comparison backlinks",
        "Proof boundary policy",
        "Trust-room structure",
    ]:
        assert phrase in html


def test_boundaries_block_fake_healthcare_claims_and_sensitive_default_intake():
    html = text(PAGE)
    required = [
        "not a real cardiology clinic case study",
        "not patient data",
        "not production access proof",
        "not a testimonial",
        "not certification",
        "not DPDP compliance proof",
        "No customer outreach was sent",
        "Admin credentials, patient identifiers, reports, diagnoses and raw chat exports are not requested by default",
    ]
    for phrase in required:
        assert phrase in html
    forbidden = [
        "trusted by cardiology clinics",
        "guaranteed appointments",
        "guaranteed no-show reduction",
        "DPDP certified",
        "real cardiology results",
        "booked appointment uplift proof",
    ]
    lower = html.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lower


def test_csv_template_is_redaction_first_and_linked():
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    fields = {row["field"] for row in rows}
    assert {"source_channel", "diagnostic_or_service_type", "whatsapp_opt_in_evidence", "human_review_flag", "unsupported_claim_risk"}.issubset(fields)
    redaction_text = "\n".join(row["redaction_rule"] for row in rows)
    assert "Do not include patient name" in redaction_text
    assert "do not include symptoms diagnosis report findings" in redaction_text
    assert f"/resources/{SLUG}/" in text(ROOT / "resources" / "index.html")
    assert URL in text(ROOT / "llms.txt")
    assert f"/resources/{SLUG}/" in text(ROOT / "scripts" / "build_sitemap.py")
