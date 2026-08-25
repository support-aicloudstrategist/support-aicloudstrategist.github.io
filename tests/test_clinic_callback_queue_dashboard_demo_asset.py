from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "resources" / "clinic-callback-queue-dashboard-demo" / "index.html"
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
    assert "not proof of search performance" in page
    assert f'link rel="canonical" href="{url}"' in page
    assert href in resources
    assert url in sitemap
    assert url in llms
