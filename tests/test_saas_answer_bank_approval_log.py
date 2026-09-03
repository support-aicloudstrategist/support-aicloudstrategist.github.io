from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "saas-security-questionnaire-takes-too-long-ai-evidence-checklist"
PAGE = RESOURCE_DIR / "index.html"
CSV = RESOURCE_DIR / "saas-answer-bank-approval-log.csv"
HUB = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_saas_answer_bank_approval_log_is_linked_from_resource_page():
    html = PAGE.read_text(encoding="utf-8")
    assert "Synthetic SaaS answer-bank approval log" in html
    assert "Download synthetic answer-bank approval log" in html
    assert "Download the synthetic SaaS answer-bank approval log CSV" in html
    assert "source evidence, legal/privacy pause rule, expiry date, revocation owner" in html
    assert "Keep customer names, private contracts, audit reports, screenshots, credentials" in html
    assert "saas-answer-bank-approval-log.csv" in html


def test_saas_answer_bank_approval_log_has_safe_reuse_controls():
    csv = CSV.read_text(encoding="utf-8")
    assert "answer_id,buyer_question_theme,approved_answer_boundary,source_evidence_type,approval_status" in csv
    assert "adviser-needed" in csv
    assert "blocked-claim" in csv
    assert "Always pause before accepting legal terms" in csv
    assert "Revenue savings ROI ranking or customer-result claims" in csv
    assert "Customer names or private contracts" in csv


def test_saas_answer_bank_approval_log_is_discoverable_from_hub_and_llms():
    rel = "/resources/saas-security-questionnaire-takes-too-long-ai-evidence-checklist/saas-answer-bank-approval-log.csv"
    assert rel in HUB.read_text(encoding="utf-8")
    assert "Download the synthetic answer-bank approval log" in HUB.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in LLMS.read_text(encoding="utf-8")
