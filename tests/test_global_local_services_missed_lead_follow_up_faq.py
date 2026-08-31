from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-local-services-missed-lead-follow-up-faq"
PAGE = ROOT / "resources" / SLUG / "index.html"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def test_local_services_missed_lead_faq_is_buyer_safe_and_routable():
    html = PAGE.read_text(encoding="utf-8")
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/global-local-services-missed-lead-follow-up-faq/"' in html
    assert "Local services missed lead follow-up FAQ" in html
    assert "missed calls" in html
    assert "WhatsApp enquiries" in html
    assert "Request a missed-lead review" in html
    assert "/free-business-review/?package=whatsapp-lead-follow-up-owner-evidence-review" in html
    assert "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/" in html
    assert "not a real customer case study" in html
    assert "conversion-rate claim" in html
    assert "revenue claim or ROI proof" in html
    assert '"@type":"FAQPage"' in html


def test_local_services_missed_lead_faq_is_discoverable():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert PATH in resources
    assert URL in llms
    assert URL in sitemap
    assert f'"{PATH}"' in builder
