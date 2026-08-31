#!/usr/bin/env python3
"""Build the curated AICS sitemap for public commercial/discoverability pages."""
from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://aicloudstrategist.com"
TODAY = dt.date.today().isoformat()
MAX_SITEMAP_URLS = 1000
CANONICAL_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', re.I)
ROBOTS_RE = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']', re.I)

CURATED_PATHS = [
    "/",
    "/free-business-review/",
    "/services/ai-mlops/",
    "/services/ai-automation/",
    "/services/cloud-finops/",
    "/services/cloud-security/",
    "/services/devops-observability/",
    "/services/website-digital-presence/",
    "/services/lead-generation-seo/website-lead-capture/",
    "/services/workflow-automation/",
    "/ai-creative-studio/",
    "/growth-control-os/",
    "/trust-compliance/",
    "/healthcare-growthos/",
    "/resources/global-b2b-saas-trial-to-paid-conversion-follow-up-evidence-checklist/",
    "/resources/global-b2b-saas-customer-onboarding-implementation-delay-checklist/",
    "/resources/global-b2b-saas-renewal-risk-owner-evidence-checklist/",
    "/resources/global-b2b-saas-demo-security-questionnaire-follow-up-evidence-checklist/",
    "/resources/global-b2b-saas-security-questionnaire-diagnostic-package/",
    "/resources/global-b2b-saas-security-questionnaire-vs-grc-trust-center-tools-comparison/",
    "/resources/global-retail-inventory-manual-work-owner-evidence-checklist/",
    "/resources/global-retail-inventory-manual-work-diagnostic-package/",
    "/resources/global-retail-inventory-pos-erp-inventory-app-comparison-checklist/",
    "/resources/global-ai-vendor-security-questionnaire-answer-source-map/",
    "/resources/global-clinic-after-hours-missed-call-follow-up-checklist/",
    "/resources/global-hotel-direct-booking-enquiry-follow-up-checklist/",
    "/resources/global-auto-dealer-internet-lead-follow-up-checklist/",
    "/resources/global-insurance-agency-quote-claims-follow-up-checklist/",
    "/resources/lead-follow-up-automation-guide/",
    "/resources/global-local-services-missed-lead-follow-up-faq/",
    "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/",
    "/resources/crm-automation-examples-guide/",
    "/resources/custom-ai-solutions-vs-off-the-shelf-ai-tools-guide/",
    "/resources/global-enterprise-ai-agent-human-override-failure-escalation-checklist/",
    "/resources/cloud-cost-optimization-finops-control/",
    "/resources/cloud-ai-economics-decision-pack/",
    "/resources/global-enterprise-ai-cost-anomaly-approval-runbook/",
    "/resources/kubernetes-namespace-cost-owner-dashboard-demo/",
    "/resources/customer-problem-search/aws-cloud-bill-too-high/",
    "/resources/customer-problem-search/manual-work-wasting-staff-time/",
    "/resources/customer-problem-search/clinic-not-getting-patients/",
    "/resources/clinic-website-not-converting-patients-checklist/",
    "/resources/saudi-private-clinic-whatsapp-appointment-follow-up-checklist/",
    "/resources/singapore-private-clinic-pdpa-patient-follow-up-evidence-checklist/",
    "/resources/singapore-private-clinic-missed-call-whatsapp-owner-evidence-checklist/",
    "/resources/singapore-private-clinic-patient-growthos-vs-clinic-software-ai-receptionist-comparison/",
    "/resources/customer-problem-search/business-compliance-privacy-confusion/",
    "/resources/customer-problem-search/find-right-consultant-vendor/",
    "/industries/law-firms/",
    "/resources/global-law-firm-missed-call-client-intake-follow-up-checklist/",
    "/industries/manufacturing-exporters/",
    "/industries/financial-services/",
    "/resources/global-financial-services-ai-intake-approval-evidence-checklist/",
    "/resources/global-accounting-firm-tax-season-client-intake-follow-up-checklist/",
    "/resources/global-accounting-firm-tax-season-owner-dashboard-demo/",
    "/resources/customer-problem-search/factory-manual-work-reduce/",
    "/resources/customer-problem-search/restaurant-local-service-customers-increase/",
    "/resources/restaurant-missed-bookings-whatsapp-follow-up-checklist/",
    "/resources/us-ai-startup-ai-spend-board-review-checklist/",
    "/resources/us-ai-startup-llm-gpu-spend-owner-dashboard-demo/",
    "/resources/us-ai-startup-llm-gpu-finops-diagnostic-package/",
    "/resources/us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison/",
    "/resources/global-gym-fitness-membership-lead-follow-up-checklist/",
    "/resources/uae-saas-cloud-ai-spend-evidence-template/",
    "/resources/global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist/",
    "/resources/global-home-services-missed-call-dispatch-evidence-checklist/",
    "/resources/global-freight-forwarding-shipment-exception-follow-up-checklist/",
    "/resources/global-construction-contractor-quote-change-order-follow-up-checklist/",
    "/resources/global-manufacturing-production-follow-up-excel-evidence-checklist/",
    "/resources/global-home-care-referral-intake-caregiver-scheduling-evidence-checklist/",
    "/resources/uk-care-home-family-enquiry-follow-up-evidence-checklist/",
    "/resources/uae-saas-cloud-trust-finops-readiness-checklist/",
    "/resources/uae-healthtech-cloud-trust-patient-data-evidence-source-map/",
    "/resources/uae-healthtech-no-credentials-patient-data-intake-policy/",
    "/resources/us-clinic-ai-receptionist-hipaa-patient-follow-up-checklist/",
    "/resources/us-clinic-source-to-owner-leak-map-template/",
    "/resources/us-clinic-ai-receptionist-vs-patient-engagement-platforms-comparison/",
    "/resources/us-clinic-ai-receptionist-hipaa-patient-follow-up-diagnostic-package/",
    "/resources/us-clinic-top-5-consideration-proof-pack/",
    "/resources/us-specialty-clinic-prior-auth-evidence-pack/",
    "/resources/us-specialty-clinic-referral-prior-auth-decision-memo/",
    "/resources/us-outpatient-imaging-referral-prior-auth-leakage-checklist/",
    "/resources/north-america-healthtech-ai-cloud-trust-diagnostic-package/",
    "/resources/north-america-healthtech-cloud-trust-finops-no-credentials-intake-policy/",
    "/resources/north-america-healthtech-redacted-cloud-ai-intake-template/",
    "/resources/north-america-healthtech-ai-cloud-owner-dashboard-demo/",
    "/resources/north-america-healthtech-ai-cloud-first-review-checklist/",
    "/resources/north-america-healthtech-ai-procurement-questionnaire-owner-handoff/",
    "/resources/north-america-healthtech-ai-human-review-escalation-policy-template/",
    "/resources/north-america-healthtech-ai-trust-first-review-executive-summary/",
    "/resources/us-healthtech-hipaa-ai-procurement-evidence-source-map/",
    "/resources/us-medical-group-healthcare-growthos-vendor-shortlist-checklist/",
    "/resources/us-medical-group-referral-prior-auth-owner-handoff-faq/",
    "/resources/us-medical-group-no-show-recovery-owner-dashboard-checklist/",
    "/resources/us-medical-group-no-credentials-patient-access-intake-policy/",
    "/resources/us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison/",
    "/resources/global-ai-pilot-board-review-faq/",
    "/resources/global-ai-pilot-data-residency-subprocessor-faq/",
    "/resources/global-ai-pilot-human-override-escalation-matrix/",
    "/resources/global-ai-pilot-model-evaluation-regression-drift-faq/",
    "/resources/global-ai-pilot-vendor-lock-in-exit-readiness-faq/",
    "/resources/global-ai-pilot-budget-overrun-approval-log-template/",
    "/resources/global-ai-pilot-data-residency-subprocessor-evidence-checklist/",
    "/resources/global-ai-pilot-governance-checklist-vs-mlops-grc-tools-comparison/",
    "/resources/global-ai-pilot-external-claim-approval-log-template/",
    "/resources/global-ai-pilot-readiness-intake-questionnaire/",
    "/resources/global-ai-pilot-board-risk-register-template/",
    "/resources/global-ai-pilot-board-risk-register-review-diagnostic-package/",
    "/resources/global-ai-pilot-board-risk-register-demo-board-pack/",
    "/resources/global-ai-pilot-rollback-readiness-checklist/",
    "/resources/global-ai-pilot-remediation-decision-log-template/",
    "/resources/us-dental-practice-missed-call-treatment-plan-follow-up-checklist/",
    "/resources/europe-private-clinic-gdpr-patient-growthos-evidence-checklist/",
    "/resources/europe-private-clinic-patient-growthos-dashboard-demo/",
    "/resources/europe-private-clinic-patient-growthos-vs-practice-management-platforms-comparison/",
    "/resources/europe-private-clinic-no-credentials-intake-policy/",
    "/resources/europe-healthtech-cloud-trust-finops-no-credentials-intake-policy/",
    "/resources/europe-healthtech-cloud-trust-finops-board-decision-memo-template/",
    "/resources/europe-healthtech-cloud-trust-finops-evidence-room/",
    "/resources/europe-healthtech-cloud-trust-finops-executive-summary/",
    "/resources/europe-healthtech-gdpr-dpia-security-questionnaire-source-map/",
    "/resources/europe-healthtech-eu-ai-act-high-risk-decision-log-template/",
    "/resources/europe-healthtech-ai-trust-questionnaire-answer-bank-template/",
    "/resources/europe-healthtech-procurement-response-readiness-checklist/",
    "/resources/europe-healthtech-cloud-trust-review-vs-finops-grc-tools-comparison/",
    "/resources/india-clinic-lab-dpdp-whatsapp-followup-evidence-checklist/",
    "/resources/india-cardiology-tmt-echo-followup-dpdp-checklist/",
    "/resources/india-cardiology-patient-growthos-vs-clinic-software-whatsapp-crm-ai-receptionist-comparison/",
    "/resources/india-ophthalmology-patient-growthos-vs-clinic-software-whatsapp-crm-ai-receptionist-comparison/",
    "/resources/india-dental-clinic-missed-calls-whatsapp-follow-up-checklist/",
    "/resources/india-radiology-mri-ct-referral-followup-dpdp-finops-checklist/",
    "/lead-leakage-calculator",
    "/case-studies/",
    "/case-studies/aicloudstrategist-geo-turnaround/",
    "/tools/",
    "/trust-assets/",
    "/trust-security/",
    "/webinars/dpdp-for-clinics-2026/",
    "/website-digital-presence/",
    "/website-lead-capture-sprint",
    "/whatsapp-automation-services/",
    "/whatsapp-lead-management-india",
    "/whatsapp-link-generator",
    "/workflow-automation-services/",
]

# Regression note: /resources/europe-saas-ai-evidence-room-template/ remains a
# public resource linked from the hub and llms.txt, but it is outside the current
# 50-URL sitemap queue while buyer-intent industry/resource routes are promoted.


def local_page(path: str) -> Path:
    if path == "/":
        return ROOT / "index.html"
    if path.endswith("/"):
        return ROOT / path.lstrip("/") / "index.html"
    return ROOT / f"{path.lstrip('/')}.html"


def validate_path(path: str) -> None:
    page = local_page(path)
    if not page.is_file():
        raise SystemExit(f"missing page for {path}: {page.relative_to(ROOT)}")
    source = page.read_text(encoding="utf-8", errors="ignore")
    robots = ROBOTS_RE.search(source)
    if robots and "noindex" in robots.group(1).lower():
        raise SystemExit(f"noindex page cannot be in sitemap: {path}")
    canonical = CANONICAL_RE.search(source)
    expected = f"{BASE_URL}{path}"
    if not canonical or canonical.group(1) != expected:
        found = canonical.group(1) if canonical else "missing"
        raise SystemExit(f"canonical mismatch for {path}: expected {expected}, found {found}")


def priority_for(path: str) -> str:
    if path == "/":
        return "1.0"
    if path in {"/free-business-review/", "/contact", "/pricing"}:
        return "0.9"
    if path.startswith("/services/") or path in {"/healthcare-growthos/", "/growth-control-os/"}:
        return "0.8"
    if path.startswith("/resources/") or path.startswith("/case-studies/"):
        return "0.7"
    return "0.6"


def changefreq_for(path: str) -> str:
    return "weekly" if path in {"/", "/resources/", "/case-studies/"} else "monthly"


def html_pages() -> list[Path]:
    ignored_parts = {".git", "node_modules", "assets", "tests"}
    pages: list[Path] = []
    for page in ROOT.rglob("*.html"):
        rel_parts = set(page.relative_to(ROOT).parts)
        if ignored_parts & rel_parts:
            continue
        if page.name == "404.html":
            continue
        pages.append(page)
    return sorted(pages)


def canonical_path_for(page: Path) -> str | None:
    source = page.read_text(encoding="utf-8", errors="ignore")
    robots = ROBOTS_RE.search(source)
    if robots and "noindex" in robots.group(1).lower():
        return None
    canonical = CANONICAL_RE.search(source)
    if not canonical:
        return None
    url = canonical.group(1)
    if not url.startswith(BASE_URL):
        return None
    path = url.removeprefix(BASE_URL)
    return path or "/"


def discover_paths() -> list[str]:
    """Return all indexable public pages, with commercial routes first.

    The monitor treats sitemap coverage as a technical-health gate. Keep the
    manually curated high-intent URLs at the top, then append every remaining
    canonical, indexable HTML page so the live sitemap does not hide legitimate
    public pages from crawlers or AI answer engines.
    """
    paths = []
    seen: set[str] = set()

    def add(path: str) -> None:
        key = path.rstrip("/") or "/"
        if key not in seen:
            paths.append(path)
            seen.add(key)

    for path in CURATED_PATHS:
        validate_path(path)
        add(path)

    for page in html_pages():
        path = canonical_path_for(page)
        if path and path.startswith("/"):
            add(path)

    if len(paths) > MAX_SITEMAP_URLS:
        paths = paths[:MAX_SITEMAP_URLS]
    return paths


def main() -> None:
    if len(CURATED_PATHS) != len(set(CURATED_PATHS)):
        raise SystemExit("duplicate sitemap paths")
    paths = discover_paths()
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in paths:
        loc = html.escape(f"{BASE_URL}{path}")
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{changefreq_for(path)}</changefreq><priority>{priority_for(path)}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(paths)} indexable sitemap URLs")


if __name__ == "__main__":
    main()
