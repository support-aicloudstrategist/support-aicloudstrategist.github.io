from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "saas-security-questionnaire-takes-too-long-ai-evidence-checklist"
PAGE = RESOURCE_DIR / "index.html"
CSV = RESOURCE_DIR / "saas-security-questionnaire-sla-risk-tracker.csv"
HUB = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_saas_security_questionnaire_sla_risk_tracker_is_linked_from_page():
    html = PAGE.read_text(encoding="utf-8")
    assert "Synthetic SaaS security questionnaire SLA risk tracker" in html
    assert "SLA risk tracker for stalled questionnaires" in html
    assert "current owner, next action, status, SLA risk, blocker" in html
    assert "Download synthetic SLA risk tracker" in html
    assert "saas-security-questionnaire-sla-risk-tracker.csv" in html


def test_saas_security_questionnaire_sla_risk_tracker_has_safe_owner_queue_fields():
    csv = CSV.read_text(encoding="utf-8")
    assert "question_id,buyer_request_theme,current_owner,next_action,status,sla_risk" in csv
    assert "adviser-needed" in csv
    assert "blocked-claim" in csv
    assert "No verified outcome evidence" in csv
    assert "Revenue savings ROI rankings or customer-result claims" in csv
    assert "Customer names private contracts or unsupported training claims" in csv


def test_saas_security_questionnaire_sla_risk_tracker_is_discoverable():
    rel = "/resources/saas-security-questionnaire-takes-too-long-ai-evidence-checklist/saas-security-questionnaire-sla-risk-tracker.csv"
    assert rel in HUB.read_text(encoding="utf-8")
    assert "Download the synthetic SLA risk tracker" in HUB.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in LLMS.read_text(encoding="utf-8")
