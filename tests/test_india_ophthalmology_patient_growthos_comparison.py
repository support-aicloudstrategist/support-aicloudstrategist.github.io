from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/india-ophthalmology-patient-growthos-vs-clinic-software-whatsapp-crm-ai-receptionist-comparison/"
URL = "https://aicloudstrategist.com" + REL
CSV = URL + "india-ophthalmology-patient-growthos-comparison.csv"


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def test_ophthalmology_comparison_page_is_buyer_safe_and_indexable():
    html = text("resources/india-ophthalmology-patient-growthos-vs-clinic-software-whatsapp-crm-ai-receptionist-comparison/index.html")
    assert f'<link rel="canonical" href="{URL}"' in html
    assert "India Ophthalmology Patient GrowthOS vs Clinic Software" in html
    assert "cataract counselling" in html
    assert "LASIK enquiries" in html
    assert "retina-review" in html
    assert "optical pickup" in html
    assert "FAQPage" in html
    assert "redaction-first" in html
    for forbidden in ["trusted by", "guaranteed", "#1 eye clinic", "certified partner", "real client result"]:
        assert forbidden not in html.lower()
    for boundary in ["not patient data", "not a testimonial", "not DPDP compliance proof", "not a vendor ranking", "not evidence of appointment uplift"]:
        assert boundary in html


def test_ophthalmology_comparison_csv_and_discovery_routes_are_present():
    csv = text("resources/india-ophthalmology-patient-growthos-vs-clinic-software-whatsapp-crm-ai-receptionist-comparison/india-ophthalmology-patient-growthos-comparison.csv")
    assert "route_buyer_may_consider" in csv
    assert "AI receptionist or call-answering tool" in csv
    assert "No autonomous clinical triage claim" in csv
    assert REL in text("resources/index.html")
    assert URL in text("llms.txt")
    assert CSV in text("llms.txt")
    assert f'"{REL}"' in text("scripts/build_sitemap.py")
