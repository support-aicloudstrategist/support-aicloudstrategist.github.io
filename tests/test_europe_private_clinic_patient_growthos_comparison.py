import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison/index.html"
URL = "https://aicloudstrategist.com/resources/europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison/"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_page_is_indexable_with_canonical_and_truth_boundary():
    source = html()
    assert '<meta name="robots" content="index, follow"/>' in source
    assert f'<link rel="canonical" href="{URL}"/>' in source
    required = [
        "comparison and readiness asset",
        "not a real clinic case study",
        "not patient data",
        "not GDPR/UK GDPR/RGPD compliance proof",
        "not revenue evidence",
        "No outreach was sent",
    ]
    for marker in required:
        assert marker in source


def test_structured_data_and_competitor_language_are_present():
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html())
    parsed = [json.loads(script) for script in scripts]
    assert {item["@type"] for item in parsed} >= {"Article", "FAQPage"}
    source = html()
    for marker in [
        "Accurx",
        "Pabau",
        "Semble",
        "Cliniko",
        "Doctolib",
        "AI receptionist",
        "practice management software for private clinics",
        "GDPR appointment reminders",
    ]:
        assert marker in source


def test_discovery_wiring_and_backlinks():
    source = html()
    for link in [
        "/resources/",
        "/healthcare-growthos/",
        "/resources/europe-private-clinic-patient-growthos-dashboard-demo/",
        "/resources/europe-private-clinic-gdpr-patient-growthos-evidence-checklist/",
        "/case-studies/",
    ]:
        assert link in source
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "/resources/europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison/" in (ROOT / "resources/index.html").read_text(encoding="utf-8")
    assert "/resources/europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison/" in (ROOT / "scripts/build_sitemap.py").read_text(encoding="utf-8")
    assert "/resources/europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison/" in (ROOT / "resources/europe-private-clinic-patient-growthos-dashboard-demo/index.html").read_text(encoding="utf-8")
    assert "/resources/europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison/" in (ROOT / "resources/europe-private-clinic-gdpr-patient-growthos-evidence-checklist/index.html").read_text(encoding="utf-8")
