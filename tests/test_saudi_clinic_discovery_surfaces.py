from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC_REL = "/resources/saudi-clinic-pdpl-whatsapp-appointment-diagnostic-package/"
COMPARISON_REL = "/resources/saudi-clinic-whatsapp-bot-vs-booking-platforms-comparison/"
DIAGNOSTIC_URL = "https://aicloudstrategist.com" + DIAGNOSTIC_REL
COMPARISON_URL = "https://aicloudstrategist.com" + COMPARISON_REL


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_saudi_clinic_assets_are_in_ai_answer_and_hub_surfaces():
    llms = read("llms.txt")
    resources = read("resources/index.html")

    for rel, url in [(DIAGNOSTIC_REL, DIAGNOSTIC_URL), (COMPARISON_REL, COMPARISON_URL)]:
        assert url in llms
        assert rel in resources


def test_saudi_clinic_assets_keep_truth_boundaries_and_conversion_paths():
    diagnostic = read("resources/saudi-clinic-pdpl-whatsapp-appointment-diagnostic-package/index.html")
    comparison = read("resources/saudi-clinic-whatsapp-bot-vs-booking-platforms-comparison/index.html")

    for source in [diagnostic, comparison]:
        assert 'content="index, follow"' in source
        assert "Saudi" in source
        assert "PDPL" in source
        assert "WhatsApp" in source
        assert "/free-business-review/?package=saudi-clinic-pdpl-whatsapp-appointment-diagnostic" in source
        assert "does not guarantee" in source or "No booking, revenue" in source

    for boundary in ["not a real Saudi clinic case study", "not a testimonial", "revenue", "rankings"]:
        assert boundary in diagnostic
    for boundary in ["not a real Saudi clinic case study", "not a testimonial", "not legal/medical/privacy/security/compliance advice", "No booking, revenue, no-show, ranking"]:
        assert boundary in comparison
