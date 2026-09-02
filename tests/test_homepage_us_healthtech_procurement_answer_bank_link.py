from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "us-healthtech-ai-patient-access-procurement-answer-bank" / "index.html"


def test_homepage_surfaces_us_healthtech_procurement_answer_bank():
    homepage = HOME.read_text(encoding="utf-8")
    resource = RESOURCE.read_text(encoding="utf-8")

    href = "/resources/us-healthtech-ai-patient-access-procurement-answer-bank/"

    assert href in homepage
    assert "US Healthtech AI + Patient Access Procurement Answer Bank" in homepage
    assert "Open the patient-access procurement answer bank" in homepage
    assert "synthetic, no-PHI procurement answer bank" in homepage
    assert "patient-access, HIPAA/PHI, AI human-review, security-questionnaire and cloud/LLM FinOps" in homepage
    assert 'link rel="canonical" href="https://aicloudstrategist.com/resources/us-healthtech-ai-patient-access-procurement-answer-bank/"' in resource
