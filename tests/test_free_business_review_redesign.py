import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "free-business-review" / "index.html").read_text(encoding="utf-8")
ALIAS = (ROOT / "free-business-review.html").read_text(encoding="utf-8")
CSS = ROOT / "css" / "free-business-review.css"
CANONICAL_OFFER = "Free Business Growth Review"


def test_canonical_route_and_alias_remain_identical():
    assert PAGE == ALIAS
    assert '<link rel="canonical" href="https://aicloudstrategist.com/free-business-review/"' in PAGE


def test_page_uses_one_canonical_offer_name():
    assert CANONICAL_OFFER in PAGE
    for retired_name in (
        "Free Trust & Growth Audit",
        "Free Business Growth Review",
        "Lost-Lead Audit",
        "Lead Capture & Follow-Up Assessment",
    ):
        if retired_name != CANONICAL_OFFER:
            assert retired_name not in PAGE
    assert f"<title>{CANONICAL_OFFER} | AICloudStrategist</title>" in PAGE


def test_hero_has_one_clear_form_anchor_action():
    hero = re.search(r'<section[^>]+class="[^"]*fbr-hero[^"]*".*?</section>', PAGE, re.S)
    assert hero
    assert 'href="#review-form"' in hero.group(0)
    assert "Start Free Review" in hero.group(0)
    assert "14-day action plan" in hero.group(0)


def test_form_is_low_friction_with_durable_native_fallback():
    form = re.search(r'<form\b[^>]*id="lostLeadAuditForm"[^>]*>.*?</form>', PAGE, re.S)
    assert form
    source = form.group(0)
    assert 'action="/api/lead"' in source
    assert 'method="POST"' in source
    assert "novalidate" not in source
    for name in ("prospect_email", "website", "primary_issue", "whatsapp_number"):
        assert f'name="{name}"' in source
    assert 'name="full_name"' not in source
    assert '<input id="business_name" name="business_name" type="hidden" value="Website submitted for review"' in source
    assert '<input id="vertical" name="vertical" type="hidden"' in source
    whatsapp = re.search(r'<input[^>]+name="whatsapp_number"[^>]*>', source)
    assert whatsapp
    assert "required" in whatsapp.group(0)
    assert "Email delivers the review" in source
    assert "delivery confirmation and recovery channel" in source
    assert "No calls or marketing messages" in source
    assert "Privacy" in source
    assert "confidential" in source.lower()
    assert 'id="auditSubmitButton"' in source


def test_turnaround_and_fallback_contact_are_explicit_and_consistent():
    assert "within 48 working hours" in PAGE
    assert "+91 87963 02608" not in PAGE
    assert "WhatsApp +91 80654 80898" in PAGE



def test_service_context_and_attribution_are_preserved():
    for name in (
        "package_context",
        "service_context",
        "form_loaded_at",
        "landing_page",
        "referrer",
        "utm_source",
        "utm_medium",
        "utm_campaign",
    ):
        assert f'name="{name}"' in PAGE
    assert "new URLSearchParams(location.search)" in PAGE
    assert "serviceContext.value=requestedService" in PAGE


def test_representative_preview_is_decision_grade_and_truthfully_labelled():
    preview_start = PAGE.index('<section class="fbr-preview"')
    source = PAGE[preview_start:PAGE.index('id="review-workflow"', preview_start)]
    for phrase in (
        "Business Health Score",
        "Lead Capture Score",
        "Priority Findings",
        "Top Risks",
        "Executive Summary",
        "Priority Matrix",
        "14-day Action Plan",
        "Representative example — not customer evidence.",
    ):
        assert phrase in source
    assert "placeholder" not in source.lower()


def test_selected_board_brief_changes_design_without_rewriting_output_content():
    for component in (
        "fbr-board",
        "fbr-board-health",
        "fbr-board-signals",
        "fbr-board-findings",
        "fbr-board-priority",
        "fbr-board-action",
    ):
        assert component in PAGE
    assert "fbr-report-grid" not in PAGE
    for original_phrase in (
        "Buyer journey needs attention",
        "Needs attention",
        "Follow-up ownership",
        "Trust foundation",
        "High-intent enquiries have no visible response expectation.",
        "Uncertain response time and channel ownership",
        "Clarify the handoff before adding more traffic",
        "Define channel ownership",
        "Repair enquiry confirmation",
        "Instrument response tracking",
    ):
        assert original_phrase in PAGE
    for invented_metric in (">68<", ">74<", ">46<", ">63<", ">51<"):
        assert invented_metric not in PAGE


def test_compact_workflow_combines_scope_output_and_process():
    assert PAGE.count('id="review-workflow"') == 1
    workflow = re.search(r'<section[^>]+id="review-workflow".*?</section>', PAGE, re.S)
    assert workflow
    source = workflow.group(0)
    for phrase in (
        "You submit",
        "We review",
        "Lead capture",
        "Follow-up",
        "Buyer journey",
        "Trust",
        "You receive",
        "Executive Summary",
        "Findings",
        "Priorities",
        "14-day Action Plan",
    ):
        assert phrase in source
    assert PAGE.count("What the audit checks") == 0
    assert PAGE.count("What happens after you submit") == 0


def test_tablet_workflow_is_a_compact_stepped_list():
    css = CSS.read_text(encoding="utf-8")
    tablet = re.search(r'@media\(max-width:980px\)\{(.*?)@media\(max-width:640px\)', css, re.S)
    assert tablet
    source = tablet.group(1)
    assert ".free-business-review-page .fbr-flow{" in source
    assert "gap:0" in source
    assert ".free-business-review-page .fbr-flow-arrow{" in source
    assert "display:none" in source


def test_page_uses_dedicated_scoped_stylesheet_without_inline_css():
    assert CSS.exists()
    assert '/css/free-business-review.css?v=20260807' in PAGE
    assert "<style" not in PAGE
    css = CSS.read_text(encoding="utf-8")
    import tinycss2

    def assert_scoped(rules):
        for rule in rules:
            if rule.type == "qualified-rule":
                selector = tinycss2.serialize(rule.prelude).strip()
                for item in selector.split(","):
                    assert item.strip().startswith(".free-business-review-page"), item.strip()
            elif rule.type == "at-rule" and rule.content is not None:
                assert_scoped(tinycss2.parse_rule_list(rule.content, skip_whitespace=True, skip_comments=True))

    assert_scoped(tinycss2.parse_stylesheet(css, skip_whitespace=True, skip_comments=True))


def test_current_navigation_and_footer_are_preserved():
    nav = re.search(r'<div data-aics-navigation-mount></div>', PAGE, re.S)
    footer = re.search(r'<footer class="aics-global-footer".*?</footer>', PAGE, re.S)
    shellrefs = re.search(
        r'<link rel="stylesheet" href="/css/site-navigation\.css[^>]*><script defer src="/js/site-navigation\.js[^>]*></script>',
        PAGE,
        re.S,
    )
    assert nav and footer and shellrefs
    assert hashlib.sha256(nav.group(0).encode()).hexdigest() == "70ed2dc02013f3bfefe3067ff2034b48e39036ccdaeb9c0d36cd8915d108b9a8"
    assert hashlib.sha256(footer.group(0).encode()).hexdigest() == "d82ff7334cae77eb2150d4048b4fbed898175493e4a12f2ede7bcc9987d554b4"
    assert hashlib.sha256(shellrefs.group(0).encode()).hexdigest() == "0599d16e1bfc5883bacc92780430ea296348801b869425920bbc441a8e5195f2"
