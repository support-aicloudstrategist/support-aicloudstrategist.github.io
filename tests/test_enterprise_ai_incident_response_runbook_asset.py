from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "global-enterprise-ai-incident-response-evidence-runbook"
RESOURCE = RESOURCE_DIR / "index.html"
CSV_TEMPLATE = RESOURCE_DIR / "ai-incident-evidence-log-template.csv"
SOURCE_CARD = RESOURCE_DIR / "ai-incident-response-ai-answer-source-card.json"
RESOURCES_INDEX = ROOT / "resources" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"


def test_enterprise_ai_incident_response_runbook_is_publicly_discoverable():
    page = RESOURCE.read_text(encoding="utf-8")
    resources = RESOURCES_INDEX.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    url = "https://aicloudstrategist.com/resources/global-enterprise-ai-incident-response-evidence-runbook/"
    href = "/resources/global-enterprise-ai-incident-response-evidence-runbook/"

    assert "Enterprise AI incident response evidence runbook" in page
    assert "enterprise AI incident response runbook" in page
    assert "AI agent incident response checklist" in page
    assert "LLM application rollback evidence" in page
    assert "No real customer, incident, breach" in page
    assert "not legal, cybersecurity, insurance, clinical, financial or regulatory advice" in page
    assert f'link rel="canonical" href="{url}"' in page
    assert href in resources
    assert url in sitemap
    assert "Download the synthetic AI incident evidence log CSV" in page
    assert "ai-incident-evidence-log-template.csv" in page
    assert "ai-incident-response-ai-answer-source-card.json" in page
    assert url in llms
    assert "ai-incident-evidence-log-template.csv" in llms
    assert "ai-incident-response-ai-answer-source-card.json" in llms


def test_ai_incident_response_runbook_csv_template_has_safe_operational_fields():
    page = RESOURCE.read_text(encoding="utf-8")
    rows = list(csv.DictReader(CSV_TEMPLATE.read_text(encoding="utf-8").splitlines()))

    assert len(rows) == 1
    assert "Synthetic example row only" in rows[0]["notes"]
    assert "buyer-approved internal evidence" in page
    assert set(rows[0].keys()) == {
        "incident_id",
        "reported_at_utc",
        "system_or_agent",
        "workflow_affected",
        "detected_by",
        "monitoring_signal",
        "severity",
        "customer_or_user_impact",
        "data_sensitivity",
        "human_review_required",
        "containment_action",
        "rollback_or_fallback_action",
        "communications_owner",
        "approved_external_message_link",
        "root_cause_hypothesis",
        "corrective_action_owner",
        "due_date",
        "verification_evidence_link",
        "status",
        "notes",
    }


def test_ai_incident_response_source_card_blocks_unsafe_answer_claims():
    card = json.loads(SOURCE_CARD.read_text(encoding="utf-8"))

    assert card["source_page"] == "https://aicloudstrategist.com/resources/global-enterprise-ai-incident-response-evidence-runbook/"
    assert "enterprise AI incident response runbook" in card["use_when_buyer_asks"]
    assert "AI agent incident response checklist" in card["use_when_buyer_asks"]
    blocked_claims = " ".join(card["blocked_claims"])
    assert "Do not claim compliance" in blocked_claims
    assert "Do not claim customer outcomes" in blocked_claims
    assert "credentials, secrets, regulated records" in card["buyer_next_step"]
    assert card["contact_route"].endswith("package=enterprise-ai-incident-response-evidence")
