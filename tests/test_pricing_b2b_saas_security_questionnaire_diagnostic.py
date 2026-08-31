import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
SLUG = "global-b2b-saas-security-questionnaire-diagnostic-package"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PATH = f"/resources/{SLUG}/"


def pricing_html() -> str:
    return PRICING.read_text(encoding="utf-8")


def itemlist_json() -> dict:
    html = pricing_html()
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    for raw in scripts:
        doc = json.loads(raw)
        if doc.get("@type") == "ItemList" and doc.get("@id", "").endswith("#fixed-scope-diagnostics"):
            return doc
    raise AssertionError("fixed-scope diagnostics ItemList JSON-LD missing")


def test_pricing_cross_links_b2b_saas_security_questionnaire_package_from_sellable_offer():
    html = pricing_html()
    assert "B2B SaaS demo-to-security-questionnaire follow-up diagnostic" in html
    assert "Related: B2B SaaS security questionnaire diagnostic package" in html
    assert PATH in html
    assert "security-questionnaire, vendor-risk, DPA/MSA, AI-use, trust-centre and deal-desk blocker queues" in html
    assert "no credentials, CRM export, confidential security report, customer evidence, legal, privacy, security, compliance, procurement, ranking, revenue or ROI claims" in html


def test_pricing_itemlist_preserves_b2b_saas_offer_and_references_questionnaire_package():
    doc = itemlist_json()
    old_url = "https://aicloudstrategist.com/resources/global-b2b-saas-demo-security-questionnaire-follow-up-evidence-checklist/"
    matches = [item for item in doc["itemListElement"] if item.get("url") == old_url]
    assert len(matches) == 1
    offer = matches[0]["item"]
    assert offer["name"] == "B2B SaaS demo-to-security-questionnaire follow-up diagnostic"
    assert offer["subjectOf"]["url"] == URL
    assert doc["numberOfItems"] == len(doc["itemListElement"]) == 20
