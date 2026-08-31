from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-ai-vendor-security-questionnaire-answer-source-map/"
URL = f"https://aicloudstrategist.com{REL}"
PAGE = ROOT / "resources" / "global-ai-vendor-security-questionnaire-answer-source-map" / "index.html"
CSV = ROOT / "resources" / "global-ai-vendor-security-questionnaire-answer-source-map" / "ai-vendor-security-questionnaire-answer-source-map.csv"
SVG = ROOT / "resources" / "global-ai-vendor-security-questionnaire-answer-source-map" / "ai-vendor-security-questionnaire-answer-source-map.svg"


def test_ai_vendor_security_questionnaire_source_map_is_buyer_safe():
    html = PAGE.read_text(encoding="utf-8")

    assert "AI vendor security questionnaire answer source map" in html
    assert "answer source, owner, current status, limitation, review date and safe claim boundary" in html
    assert "not a real customer case study" in html
    assert "not legal/security/compliance/procurement advice" in html
    assert "Request source-map fit check" in html
    assert "No outreach was sent" in html
    assert "ai-vendor-security-questionnaire-answer-source-map.csv" in html
    assert "ai-vendor-security-questionnaire-answer-source-map.svg" in html
    assert "Downloadable source-map visual" in html
    assert "no real customer, prospect, CRM, contract, security report, compliance evidence, revenue data, testimonial or ranking proof" in html


def test_source_map_svg_is_downloadable_synthetic_and_owner_safe():
    svg = SVG.read_text(encoding="utf-8")
    for marker in [
        "Demo AI vendor security questionnaire answer source map",
        "Buyer question",
        "Evidence source",
        "Owner review",
        "Safe reply",
        "Unsafe claim stops",
        "No invented compliance status",
        "No security approval claim",
        "No AI accuracy guarantee",
        "No revenue, ROI or win-rate proof",
        "NO CUSTOMER, CRM, SECURITY REPORT, CONTRACT OR REVENUE DATA",
    ]:
        assert marker in svg

def test_source_map_csv_is_downloadable_and_buyer_safe():
    csv = CSV.read_text(encoding="utf-8")
    required = [
        "question_area,buyer_question,evidence_source_to_attach,named_owner,status,safe_answer_boundary,review_date",
        "AI data use",
        "Training use",
        "Model risk",
        "Security controls",
        "Compliance posture",
        "Commercial claims",
        "Production ownership",
        "Final approval",
        "Do not claim revenue lift, rankings, savings or customer outcomes without verified proof.",
        "Block any answer without a source, owner, status, limitation and review date.",
    ]
    for marker in required:
        assert marker in csv


def test_source_map_has_faq_and_article_structured_data():
    html = PAGE.read_text(encoding="utf-8")
    blocks = [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)]

    graph = next(block["@graph"] for block in blocks if isinstance(block, dict) and "@graph" in block)
    article = next(item for item in graph if item.get("@type") == "Article")
    assert article["mainEntityOfPage"] == URL
    assert "AI trust center evidence" in article["about"]

    faq = next(block for block in blocks if isinstance(block, dict) and block.get("@type") == "FAQPage")
    assert len(faq["mainEntity"]) == 3
    assert "approved source" in faq["mainEntity"][0]["acceptedAnswer"]["text"]


def test_source_map_is_discoverable_from_resource_hub_llms_and_sitemap_queue():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    assert REL in resources
    assert URL in llms
    assert REL in sitemap_script
    assert URL in sitemap
