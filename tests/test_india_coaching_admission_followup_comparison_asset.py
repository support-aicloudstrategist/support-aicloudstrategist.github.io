from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "india-coaching-centre-admission-follow-up-vs-crm-whatsapp-ai-comparison" / "index.html"
CSV = ROOT / "resources" / "india-coaching-centre-admission-follow-up-vs-crm-whatsapp-ai-comparison" / "india-coaching-admission-follow-up-comparison.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
CHECKLIST = ROOT / "resources" / "india-coaching-centre-admission-follow-up-checklist" / "index.html"


def test_comparison_page_is_indexable_and_buyer_safe():
    html = PAGE.read_text(encoding="utf-8")
    assert "coaching centre admission enquiries not converting" in html
    assert "CRM, WhatsApp automation and AI chatbots" in html
    assert "synthetic buyer-education comparison only" in html
    assert "not a real coaching-centre case study" in html
    assert "does not claim DPDP compliance" in html
    assert "Dataset" in html
    assert "Request diagnostic fit check" in html


def test_synthetic_csv_matrix_exists_with_expected_routes():
    csv = CSV.read_text(encoding="utf-8")
    for route in ["CRM or education ERP", "WhatsApp automation", "AI chatbot or AI receptionist", "Call centre or agency", "AICS owner-evidence review"]:
        assert route in csv
    assert "No automated fee, scholarship, admission or result promise" in csv


def test_resource_hub_llms_and_existing_checklist_link_asset():
    slug = "/resources/india-coaching-centre-admission-follow-up-vs-crm-whatsapp-ai-comparison/"
    assert slug in RESOURCES.read_text(encoding="utf-8")
    assert slug in LLMS.read_text(encoding="utf-8")
    assert slug in CHECKLIST.read_text(encoding="utf-8")
