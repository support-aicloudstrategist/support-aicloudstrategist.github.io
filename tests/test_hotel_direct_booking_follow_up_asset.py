from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-hotel-direct-booking-enquiry-follow-up-checklist" / "index.html"
REL = "/resources/global-hotel-direct-booking-enquiry-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_hotel_direct_booking_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "Hotel Direct Booking Enquiry Follow-Up Checklist",
        "hotel direct booking leads not converting",
        "hotel missed calls reservation enquiry follow up",
        "hotel WhatsApp booking follow-up",
        "hotel website enquiries not converting",
        "OTA handoff leakage",
        "hotel owner dashboard",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "Cloudbeds, Mews, SiteMinder, Little Hotelier",
        "Truth boundary",
    ]:
        assert marker in source


def test_hotel_direct_booking_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real hotel case study",
        "not a real resort case study",
        "not production data",
        "not guest data",
        "not reservation data",
        "not payment data",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not hospitality compliance advice",
        "not direct-booking evidence",
        "not occupancy evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real hotel, resort, guest house, serviced apartment, guest, traveller, customer, client, logo, certification or customer outcome is claimed",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-hotel-direct-booking-enquiry-follow-up-checklist" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_hotel_direct_booking_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
