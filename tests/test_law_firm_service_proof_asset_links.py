from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "us-law-firm-ai-intake-answering-service" / "index.html"


def test_law_firm_service_links_buyer_proof_assets_and_keeps_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")

    assert '<link rel="canonical" href="https://aicloudstrategist.com/services/us-law-firm-ai-intake-answering-service/"' in html
    assert "Buyer proof assets for this service" in html
    assert "/resources/us-law-firm-ai-intake-confidentiality-checklist/" in html
    assert "/resources/us-law-firm-ai-intake-answering-service-faq/" in html
    assert "/resources/us-law-firm-ai-intake-vs-legal-crm-answering-services-comparison/" in html
    assert "/case-studies/simulated-us-law-firm-ai-intake-confidentiality-diagnostic/" in html
    assert "/free-business-review/?package=us-law-firm-intake-evidence" in html

    for boundary in [
        "AICS is not a law firm",
        "does not provide legal advice",
        "legal intake services",
        "confidentiality guarantees",
        "before sharing real matter, client, call, conflict or confidential firm data",
    ]:
        assert boundary in html

    for payload in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        json.loads(payload)
