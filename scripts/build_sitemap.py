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
CANONICAL_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', re.I)
ROBOTS_RE = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']', re.I)

CURATED_PATHS = [
    "/",
    "/free-business-review/",
    "/contact",
    "/pricing",
    "/about/",
    "/how-we-work/",
    "/services/ai-mlops/",
    "/services/ai-automation/",
    "/services/cloud-finops/",
    "/services/cloud-security/",
    "/services/devops-observability/",
    "/services/website-digital-presence/",
    "/services/lead-generation-seo/website-lead-capture/",
    "/services/workflow-automation/",
    "/services/us-law-firm-ai-intake-answering-service/",
    "/ai-creative-studio/",
    "/growth-control-os/",
    "/trust-compliance/",
    "/healthcare-growthos/",
    "/ai-automation-agency/",
    "/resources/",
    "/resources/lead-follow-up-automation-guide/",
    "/resources/cloud-cost-optimization-finops-control/",
    "/resources/cloud-ai-economics-decision-pack/",
    "/resources/customer-problem-search/aws-cloud-bill-too-high/",
    "/resources/customer-problem-search/manual-work-wasting-staff-time/",
    "/resources/customer-problem-search/clinic-not-getting-patients/",
    "/resources/customer-problem-search/business-compliance-privacy-confusion/",
    "/resources/customer-problem-search/find-right-consultant-vendor/",
    "/resources/customer-problem-search/small-shop-customer-increase/",
    "/resources/customer-problem-search/factory-manual-work-reduce/",
    "/resources/customer-problem-search/restaurant-local-service-customers-increase/",
    "/resources/us-ai-startup-llm-gpu-finops-diagnostic-package/",
    "/resources/us-ai-startup-llm-gpu-finops-vs-cloud-cost-tools-comparison/",
    "/resources/property-management-maintenance-request-follow-up-checklist/",
    "/resources/uae-saas-cloud-trust-finops-readiness-checklist/",
    "/resources/uae-saas-cloud-finops-trust-diagnostic-package/",
    "/resources/us-clinic-ai-receptionist-hipaa-patient-follow-up-checklist/",
    "/resources/us-clinic-ai-receptionist-vs-patient-engagement-platforms-comparison/",
    "/resources/us-clinic-ai-receptionist-hipaa-patient-follow-up-diagnostic-package/",
    "/resources/us-clinic-top-5-consideration-proof-pack/",
    "/resources/us-specialty-clinic-prior-auth-evidence-pack/",
    "/resources/us-law-firm-ai-intake-answering-service-faq/",
    "/resources/saas-security-questionnaire-takes-too-long-ai-evidence-checklist/",
    "/resources/customer-problem-search/coaching-school-admission-increase/",
    "/resources/singapore-saas-ai-security-review-evidence-pack-checklist/",
    "/resources/europe-saas-ai-evidence-room-template/",
    "/resources/europe-saas-ai-governance-evidence-diagnostic-package/",
    "/case-studies/",
    "/case-studies/aicloudstrategist-geo-turnaround/",
]


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


def main() -> None:
    if len(CURATED_PATHS) != len(set(CURATED_PATHS)):
        raise SystemExit("duplicate sitemap paths")
    if len(CURATED_PATHS) > 50:
        raise SystemExit(f"curated sitemap too large: {len(CURATED_PATHS)}")
    for path in CURATED_PATHS:
        validate_path(path)
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in CURATED_PATHS:
        loc = html.escape(f"{BASE_URL}{path}")
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{changefreq_for(path)}</changefreq><priority>{priority_for(path)}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(CURATED_PATHS)} curated sitemap URLs")


if __name__ == "__main__":
    main()
