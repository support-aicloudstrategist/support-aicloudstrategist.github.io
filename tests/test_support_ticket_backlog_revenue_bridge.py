from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SLUG = "global-customer-support-ticket-backlog-vs-helpdesk-ai-chatbot-comparison"
RESOURCE_PATH = f"/resources/{SLUG}/"
CSV_PATH = f"/resources/{SLUG}/support-ticket-backlog-comparison-matrix.csv"


def test_pricing_has_support_ticket_backlog_revenue_bridge_without_changing_fixed_offer_count():
    html = (REPO / "pricing.html").read_text(encoding="utf-8")

    assert "Thirty-two concrete first offers" in html
    assert 'data-revenue-bridge="support-ticket-backlog-helpdesk-ai-chatbot"' in html
    assert "Support ticket backlog diagnostic bridge" in html
    assert RESOURCE_PATH in html
    assert CSV_PATH in html
    assert "/free-business-review/?package=support-ticket-backlog-diagnostic&amp;source=pricing-fixed-scope" in html
    assert "helpdesk AI chatbot" in html
    assert "BPO support" in html


def test_support_ticket_backlog_bridge_preserves_buyer_safe_claim_boundaries():
    html = (REPO / "pricing.html").read_text(encoding="utf-8")
    start = html.index('data-revenue-bridge="support-ticket-backlog-helpdesk-ai-chatbot"')
    section = html[start:html.index('</aside>', start)]

    for boundary in [
        "no customer data",
        "support ticket data",
        "helpdesk export",
        "chat transcript",
        "refund record",
        "credential",
        "production access",
        "legal/privacy/security/customer-success advice",
        "ticket-deflection, SLA, CSAT, retention, revenue, savings, ROI or AI-accuracy claim",
    ]:
        assert boundary in section

    assert "Starts from the buyer-safe comparison matrix and synthetic CSV" in section
