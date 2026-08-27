import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FREE_REVIEW = (ROOT / "free-business-review" / "index.html").read_text(encoding="utf-8")
FREE_REVIEW_FILE = (ROOT / "free-business-review.html").read_text(encoding="utf-8")
CONTACT = (ROOT / "contact.html").read_text(encoding="utf-8")
CONTACT_API = (ROOT / "functions" / "api" / "contact.ts").read_text(encoding="utf-8")
LEAD_API = (ROOT / "functions" / "api" / "lead.ts").read_text(encoding="utf-8")
PRIVACY = (ROOT / "privacy.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
TRACKING = (ROOT / "js" / "aics-conversion-tracking.js").read_text(encoding="utf-8")
ANALYTICS_SHIM = (ROOT / "js" / "aics-analytics-shim.js").read_text(encoding="utf-8")
MIDDLEWARE = (ROOT / "functions" / "_middleware.ts").read_text(encoding="utf-8")
WEBINAR_API = (ROOT / "functions" / "api" / "webinar-register.ts").read_text(encoding="utf-8")
WEBINAR_PAGE = (ROOT / "webinars" / "dpdp-for-clinics-2026" / "index.html").read_text(encoding="utf-8")
CONTACT_INDEX = (ROOT / "contact" / "index.html").read_text(encoding="utf-8")
REDIRECTS = (ROOT / "_redirects").read_text(encoding="utf-8")


def test_free_review_uses_durable_lead_endpoint_with_verified_success():
    assert '<link rel="canonical" href="https://aicloudstrategist.com/free-business-review/"' in FREE_REVIEW
    assert '<link rel="canonical" href="https://aicloudstrategist.com/free-business-review/"' in FREE_REVIEW_FILE
    assert FREE_REVIEW == FREE_REVIEW_FILE
    assert "/free-business-review /free-business-review/ 301" in REDIRECTS
    form = re.search(r'<form\b[^>]*id="lostLeadAuditForm"[^>]*>', FREE_REVIEW, flags=re.I)
    assert form is not None
    assert 'action="/api/lead"' in form.group(0)
    assert 'method="POST"' in form.group(0)
    assert "fetch('/api/lead'" in FREE_REVIEW
    assert "if (!response.ok || !result.ok)" in FREE_REVIEW
    assert "result.lead_id" in FREE_REVIEW
    assert "window.location.href=aicsLeadMailto(payload)" not in FREE_REVIEW


def test_free_review_uses_a_browser_valid_phone_pattern():
    assert r'pattern="^\+?[0-9][0-9\s\-]{8,18}$"' in FREE_REVIEW
    assert r'pattern="^\+?[0-9][0-9\s-]{8,18}$"' not in FREE_REVIEW


def test_contact_submission_preserves_structured_interest_and_first_touch_attribution():
    for field in (
        "company",
        "role",
        "service",
        "stage",
        "landing_page",
        "referrer",
        "utm_source",
        "utm_medium",
        "utm_campaign",
    ):
        assert f"{field}:" in CONTACT
        assert f"payload.{field}" in CONTACT_API


def test_contact_records_begin_in_an_owned_pipeline_state():
    assert 'pipeline_stage: "new"' in CONTACT_API
    assert 'lead_status: "unreviewed"' in CONTACT_API
    assert 'owner: "AICloudStrategist Growth Operations"' in CONTACT_API
    assert 'notification_status: "manual_review_pending"' in CONTACT_API


def test_contact_form_has_a_non_intrusive_spam_trap_and_restricted_cors():
    assert 'name="company_website"' in CONTACT
    assert 'autocomplete="off"' in CONTACT
    assert "payload.company_website" in CONTACT_API
    assert "Suspicious form submission" in CONTACT_API
    assert '"Access-Control-Allow-Origin": "https://aicloudstrategist.com"' in CONTACT_API
    assert '"Access-Control-Allow-Origin": "*"' not in CONTACT_API
    for endpoint in (CONTACT_API, LEAD_API):
        assert "hasTrustedBrowserProvenance(context.request)" in endpoint
        assert 'request.headers.get("CF-Connecting-IP")' in endpoint
        assert 'await submissionId(' in endpoint


def test_cloudflare_redirects_and_internal_artifact_denials_are_valid():
    assert "301!" not in REDIRECTS
    assert "404!" not in REDIRECTS
    for path in (
        "/CLAUDE.md",
        "/contact-channels.json",
        "/client-desk",
        "/client-desk.html",
        "/phase-",
        "/internal",
        "/internal.html",
        "/preview/",
        "/tests/",
        "/scripts/",
        "/seo/",
        "/tools/brand_trust_monitor.py",
        "/tools/layman_problem_search_score.py",
        "/docs/",
        "/.github/",
        "/_redirects",
    ):
        assert f'"{path}"' in MIDDLEWARE
    assert "status: 404" in MIDDLEWARE
    assert "X-Robots-Tag" in MIDDLEWARE
    assert "decodeURIComponent(decoded)" in MIDDLEWARE
    assert 'replace(/\\\\/g, "/")' in MIDDLEWARE
    assert 'replace(/\\/{2,}/g, "/")' in MIDDLEWARE
    assert 'pathname === prefix.slice(0, -1)' in MIDDLEWARE


def test_webinar_registration_is_durable_manual_review_not_public_email_relay():
    assert "sendGraphMail" not in WEBINAR_API
    assert "sendMail" not in WEBINAR_API
    assert "M365_" not in WEBINAR_API
    assert "hasTrustedBrowserProvenance(context.request)" in WEBINAR_API
    assert "await enforceRateLimit(context.env, context.request)" in WEBINAR_API
    assert "await context.env.LEAD_LOG.put" in WEBINAR_API
    assert 'notification_status: "manual_review_pending"' in WEBINAR_API
    assert "confirmation_sent: false" in WEBINAR_API
    assert "crypto.randomUUID()" in WEBINAR_API
    assert "minute.replace" not in WEBINAR_API
    assert "company_website" in WEBINAR_PAGE
    assert "form_loaded_at" in WEBINAR_PAGE
    assert "within 5 minutes" not in WEBINAR_PAGE


def test_redirects_do_not_loop_extensionless_pages_back_to_html():
    assert "/local-business-website-india /local-business-website-india.html" not in REDIRECTS
    assert "/factory-website-development-india /factory-website-development-india.html" not in REDIRECTS


def test_free_review_has_a_non_intrusive_spam_trap():
    assert 'name="company_website"' in FREE_REVIEW
    assert "payload.company_website" in LEAD_API
    assert "Suspicious form submission" in LEAD_API


def test_free_review_leads_preserve_attribution_and_pipeline_state():
    for field in ("landing_page", "referrer", "utm_source", "utm_medium", "utm_campaign"):
        assert f"payload.{field}" in LEAD_API
    assert 'pipeline_stage: "new"' in LEAD_API
    assert 'lead_status: "audit-requested"' in LEAD_API
    assert 'owner: "AICloudStrategist Growth Operations"' in LEAD_API
    assert "[AICS-LEAD][AUDIT-REQUEST]" in LEAD_API


def test_free_review_package_context_survives_cta_to_pipeline_notes_and_analytics():
    assert 'name="package_context"' in FREE_REVIEW
    assert "const requestedPackage=reviewParams.get('package')||'';" in FREE_REVIEW
    assert "payload.package_context?'Requested package: '+payload.package_context+'.'" in FREE_REVIEW
    assert "package_context:payload.package_context||''" in FREE_REVIEW
    assert "const packageContext = clean(payload.package_context)" in LEAD_API
    assert "Package context: ${packageContext || \"not set\"}" in LEAD_API


def test_llms_map_is_curated_around_current_public_positioning():
    assert "Enterprise AI" in LLMS
    assert "Business Growth Systems" in LLMS
    assert "AI Creative Studio" in LLMS
    for path in (
        "/services/ai-mlops/",
        "/services/ai-automation/",
        "/services/cloud-finops/",
        "/services/cloud-security/",
        "/services/devops-observability/",
    ):
        assert f"https://aicloudstrategist.com{path}" in LLMS
    assert "canonical positioning is Growth & Control OS" not in LLMS
    assert "Do not infer" in LLMS
    assert "https://support-aicloudstrategist.github.io/publications/2026-08-23/ai-inbox-triage-board.html" in LLMS
    assert len(LLMS.splitlines()) <= 120


def test_contact_route_has_one_api_backed_canonical_owner():
    assert '<link rel="canonical" href="https://aicloudstrategist.com/contact">' in CONTACT
    assert '<link rel="canonical" href="https://aicloudstrategist.com/contact">' in CONTACT_INDEX
    assert 'action="/api/contact"' in CONTACT_INDEX
    form = re.search(r'<form[^>]*id="contactForm".*?</form>', CONTACT_INDEX, re.S)
    assert form is not None
    assert "mailto:contact@aicloudstrategist.com" not in form.group(0)
    assert "/contact/ /contact 301" in REDIRECTS
    assert "- Contact: https://aicloudstrategist.com/contact\n" in LLMS
    assert "- Contact: https://aicloudstrategist.com/contact/" not in LLMS


def test_lead_endpoints_expose_side_effect_free_readiness_checks():
    for endpoint in (CONTACT_API, LEAD_API):
        assert "export const onRequestGet" in endpoint
        assert "storage_configured" in endpoint
        assert 'notification_mode: "manual-review"' in endpoint


def test_live_customer_facing_html_has_no_unresolved_template_placeholders():
    placeholder = re.compile(r"\{\{\s*[A-Za-z_][A-Za-z0-9_\-.]*\s*\}\}")
    for path in ROOT.rglob("*.html"):
        html = path.read_text(encoding="utf-8", errors="replace")
        assert not placeholder.search(html), path


def test_no_customer_journey_points_to_the_dead_calendly_route():
    dead = "calendly.com/aicloudstrategist/15min"
    for path in ROOT.rglob("*.html"):
        assert dead not in path.read_text(encoding="utf-8", errors="replace"), path


def test_customer_click_to_call_links_are_not_masked_or_invalid():
    masked_tel = "tel:+918" + "****" + "0898"
    canonical_tel = "tel:+91" + "8065480898"
    click_to_call_pages = 0
    for path in ROOT.rglob("*.html"):
        html = path.read_text(encoding="utf-8", errors="replace")
        assert masked_tel not in html, path
        if "href=\"tel:" in html and "+91 80654 80898" in html:
            assert canonical_tel in html, path
            click_to_call_pages += 1
    assert click_to_call_pages >= 5


def test_audit_endpoint_is_not_an_arbitrary_confirmation_email_relay():
    assert "async function readPayload" in LEAD_API
    assert "request.formData()" in LEAD_API
    assert "sendConfirmationEmail" not in LEAD_API
    assert "enforceRateLimit" in LEAD_API
    assert "const websiteTrap = clean(payload.company_website)" in LEAD_API
    assert "if (websiteTrap)" in LEAD_API
    assert "toRecipients: [{ emailAddress: { address: lead.prospect_email" not in LEAD_API
    assert "if (!context.env.LEAD_LOG)" in LEAD_API
    assert 'notification_status: "manual_review_pending"' in LEAD_API
    assert "sendLeadEmail(context.env" not in LEAD_API
    assert "sendGraphMail(context.env" not in CONTACT_API


def test_first_touch_attribution_survives_internal_navigation_for_the_session():
    assert "sessionStorage" in TRACKING
    assert "aics:first-touch:v1" in TRACKING
    assert "window.aicsAttribution" in TRACKING
    assert "window.aicsAttribution" in CONTACT
    assert "window.aicsAttribution" in FREE_REVIEW
    assert "landing_page:location.href" not in TRACKING
    assert "props.url=location.href" not in TRACKING
    for endpoint in (CONTACT_API, LEAD_API):
        assert "sanitizeAttributionUrl(payload.landing_page)" in endpoint
        assert "sanitizeAttributionUrl(payload.referrer)" in endpoint
    assert "location.href" not in ANALYTICS_SHIM
    assert "localStorage" not in ANALYTICS_SHIM
    assert "sessionStorage" in ANALYTICS_SHIM


def test_privacy_notice_describes_the_live_form_and_analytics_processors():
    assert "forms currently open your email or WhatsApp" not in PRIVACY
    assert "Microsoft 365" in PRIVACY
    assert "Cloudflare" in PRIVACY
    assert "contact form" in PRIVACY.lower()
    assert "phone or WhatsApp number" in PRIVACY
    assert "business category" in PRIVACY
    assert "session storage" in PRIVACY
