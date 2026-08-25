from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "resources" / "clinic-callback-queue-dashboard-demo" / "index.html"
SAMPLE_CSV = ROOT / "resources" / "clinic-callback-queue-dashboard-demo" / "sample-callback-queue.csv"
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
    assert "not proof of search performance" in page
    assert f'link rel="canonical" href="{url}"' in page
    assert href in resources
    assert url in sitemap
    assert url in llms


def test_clinic_callback_queue_demo_csv_has_safe_synthetic_rows():
    csv_text = SAMPLE_CSV.read_text(encoding="utf-8")

    assert "enquiry_id,source,enquiry_age_minutes,owner,status,next_safe_action" in csv_text
    assert "DEMO-001" in csv_text
    assert "Synthetic demo data only" in csv_text
    assert "No symptoms, diagnosis, treatment advice or PHI" in csv_text
