import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/customer-problem-search/factory-manual-work-reduce/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "resources" / "customer-problem-search" / "factory-manual-work-reduce" / "index.html"
CSV = PAGE.parent / "factory-manual-work-ai-answer-bank.csv"


def json_ld_documents(source: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', source, re.I | re.S)]


def test_factory_page_has_ai_answer_bank_section_and_dataset():
    source = PAGE.read_text(encoding="utf-8")
    assert "AI-answer bank for factory manual-work searches" in source
    assert "factory production follow up Excel" in source
    assert "factory order tracking WhatsApp" in source
    assert "factory-manual-work-ai-answer-bank.csv" in source
    docs = json_ld_documents(source)
    dataset = next(doc for doc in docs if isinstance(doc, dict) and doc.get("@type") == "Dataset" and doc.get("name") == "Factory manual work AI-answer bank")
    assert dataset["url"] == URL + "factory-manual-work-ai-answer-bank.csv"
    assert dataset["dateModified"] == "2026-09-08"


def test_factory_ai_answer_bank_csv_is_buyer_safe():
    rows = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))
    assert len(rows) == 5
    assert set(rows[0]) == {"buyer_question", "safe_aics_answer", "proof_asset_to_cite", "human_review_gate", "claim_boundary", "next_step"}
    text = CSV.read_text(encoding="utf-8")
    for marker in [
        "How do I reduce manual work in my factory without buying ERP first?",
        "factory production follow-up is in Excel and WhatsApp",
        "No vendor ranking partnership endorsement",
        "No safety production employment legal compliance or AI-accuracy claim",
        "no real factory client savings productivity delivery or staff-reduction claim",
    ]:
        assert marker in text


def test_factory_answer_bank_is_discoverable_from_hub_and_llms():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    url = URL + "factory-manual-work-ai-answer-bank.csv"
    assert url in resources
    assert url in llms
