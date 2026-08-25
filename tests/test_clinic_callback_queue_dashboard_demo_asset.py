from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "resources" / "clinic-callback-queue-dashboard-demo" / "index.html"
SAMPLE_CSV = ROOT / "resources" / "clinic-callback-queue-dashboard-demo" / "sample-callback-queue.csv"
DASHBOARD_SVG = ROOT / "resources" / "clinic-callback-queue-dashboard-demo" / "demo-dashboard.svg"
EVIDENCE_CHECKLIST = ROOT / "resources" / "clinic-callback-queue-dashboard-demo" / "evidence-checklist.html"
RESOURCES_INDEX = ROOT / "resources" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"


def test_clinic_callback_queue_dashboard_demo_is_publicly_discoverable():
    page = RESOURCE.read_text(encoding="utf-8")
    resources = RESOURCES_INDEX.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    url = "https://aicloudstrategist.com/resources/clinic-callback-queue-dashboard-demo/"
    href = "/resources/clinic-callback-queue-dashboard-demo/"

    assert "Clinic callback queue dashboard demo" in page
    assert "clinic missed patient calls" in page
    assert "missed call callback dashboard for clinics" in page
    assert "All example fields and metrics are demo-labelled and synthetic" in page
    assert "sample-callback-queue.csv" in page
    assert "demo-dashboard.svg" in page
    assert "Download the synthetic dashboard SVG" in page
    assert "not a real clinic result" in page
    assert "not proof of search performance" in page
    assert f'link rel="canonical" href="{url}"' in page
    assert href in resources
    assert url in sitemap
    assert url in llms


def test_clinic_callback_queue_evidence_checklist_is_safe_and_discoverable():
    page = EVIDENCE_CHECKLIST.read_text(encoding="utf-8")
    demo_page = RESOURCE.read_text(encoding="utf-8")
    resources = RESOURCES_INDEX.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    url = "https://aicloudstrategist.com/resources/clinic-callback-queue-dashboard-demo/evidence-checklist.html"
    href = "/resources/clinic-callback-queue-dashboard-demo/evidence-checklist.html"

    assert "Clinic callback queue evidence checklist" in page
    assert "clinic missed patient calls" in page
    assert "AI receptionist checklist" in page
    assert "One-page buying evidence checklist" in page
    assert "No real clinic, patient, PHI, customer result" in page
    assert "not evidence of search traffic" in page
    assert f'link rel="canonical" href="{url}"' in page
    assert href in demo_page
    assert href in resources
    assert url in sitemap
    assert url in llms


def test_clinic_callback_queue_demo_csv_has_safe_synthetic_rows():
    csv_text = SAMPLE_CSV.read_text(encoding="utf-8")

    assert "enquiry_id,source,enquiry_age_minutes,owner,status,next_safe_action" in csv_text
    assert "DEMO-001" in csv_text
    assert "Synthetic demo data only" in csv_text
    assert "No symptoms, diagnosis, treatment advice or PHI" in csv_text


def test_clinic_callback_queue_dashboard_svg_is_safe_and_synthetic():
    svg_text = DASHBOARD_SVG.read_text(encoding="utf-8")

    assert "Synthetic clinic callback queue dashboard snapshot" in svg_text
    assert "Synthetic demo data only" in svg_text
    assert "no real clinic, patient, PHI, booking, revenue or compliance claim" in svg_text
    assert "DEMO-004" in svg_text
    assert "Automation boundary" in svg_text
