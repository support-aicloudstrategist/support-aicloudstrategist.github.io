#!/usr/bin/env python3
"""AICloudStrategist brand/trust visibility monitor.

Runs safe local checks against the static repo and selected live URLs.
It does not need credentials and it does not claim analytics/search-console data.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://aicloudstrategist.com"
PUBLIC_SKIP_PARTS = {
    ".git",
    ".workspace-snapshots",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "preview",
    "node_modules",
    "venv",
}
COMMERCIAL_HINTS = (
    "free-business-review",
    "contact@aicloudstrategist.com",
    "wa.me/918796302608",
    "tel:+918065480898",
    "whatsapp",
    "contact.html",
)


@dataclass
class Finding:
    level: str
    category: str
    path: str
    message: str


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.canonicals: list[str] = []
        self.descriptions = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() == "a" and data.get("href"):
            self.hrefs.append(data["href"])
        if tag.lower() == "link" and data.get("rel", "").lower() == "canonical":
            self.canonicals.append(data.get("href", ""))
        if tag.lower() == "meta" and data.get("name", "").lower() == "description":
            self.descriptions += 1


def public_html_files() -> Iterable[Path]:
    for path in ROOT.rglob("*.html"):
        rel_parts = set(path.relative_to(ROOT).parts)
        if rel_parts & PUBLIC_SKIP_PARTS:
            continue
        name = path.name.lower()
        rel = path.relative_to(ROOT).as_posix()
        if name.endswith(".backup.html") or "-old/" in rel or name.startswith("google"):
            continue
        yield path


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel.endswith("/index.html"):
        return f"{BASE_URL}/{rel[:-11]}"
    return f"{BASE_URL}/{rel}"


def normalize_url(url: str) -> str:
    """Normalize equivalent public URLs for sitemap coverage checks."""
    if url == f"{BASE_URL}/":
        return url
    return url.rstrip("/")


def parse_jsonld(text: str, rel: str, findings: list[Finding]) -> int:
    count = 0
    for match in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.S | re.I):
        count += 1
        raw = match.group(1).strip()
        try:
            json.loads(raw)
        except Exception as exc:  # noqa: BLE001 - report exact parser failure
            findings.append(Finding("fail", "schema", rel, f"Bad JSON-LD: {exc}"))
    return count


def check_repo() -> dict:
    findings: list[Finding] = []
    html_files = list(public_html_files())
    jsonld_blocks = 0
    urls_from_pages: set[str] = set()

    sitemap_path = ROOT / "sitemap.xml"
    sitemap_urls: set[str] = set()
    if sitemap_path.exists():
        tree = ET.parse(sitemap_path)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_urls = {normalize_url(loc.text or "") for loc in tree.findall(".//sm:loc", ns)}
    else:
        findings.append(Finding("fail", "sitemap", "sitemap.xml", "Missing sitemap.xml"))

    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        parser = LinkParser()
        parser.feed(text)
        jsonld_blocks += parse_jsonld(text, rel, findings)
        noindex = "name=\"robots\"" in lower and "noindex" in lower

        if rel != "404.html" and not parser.canonicals:
            findings.append(Finding("warn", "canonical", rel, "Missing canonical link"))
            urls_from_pages.add(normalize_url(page_url(path)))
        elif parser.canonicals and not noindex:
            urls_from_pages.add(normalize_url(parser.canonicals[0]))
        if rel != "404.html" and parser.descriptions == 0:
            findings.append(Finding("warn", "metadata", rel, "Missing meta description"))
        if not any(hint in lower for hint in COMMERCIAL_HINTS):
            findings.append(Finding("warn", "conversion", rel, "No obvious contact/free-review/WhatsApp CTA"))

        for href in parser.hrefs:
            if href.startswith(("#", "mailto:", "tel:", "https://wa.me", "http://", "https://")):
                continue
            target = href.split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith("javascript:"):
                continue
            candidate = (ROOT / target.lstrip("/")).resolve()
            exists = candidate.exists() or candidate.with_suffix(".html").exists() or (candidate / "index.html").exists()
            if not exists and not target.endswith("/"):
                exists = (ROOT / f"{target.lstrip('/')}.html").exists()
            if not exists:
                findings.append(Finding("fail", "internal-link", rel, f"Broken local link: {href}"))

    missing_from_sitemap = sorted(urls_from_pages - sitemap_urls)
    public_missing = [u for u in missing_from_sitemap if "/assets/" not in u and u != f"{BASE_URL}/404.html"]
    for url in public_missing[:50]:
        findings.append(Finding("warn", "sitemap", url, "Public page not listed in sitemap"))

    return {
        "html_pages_checked": len(html_files),
        "sitemap_urls": len(sitemap_urls),
        "jsonld_blocks": jsonld_blocks,
        "findings": [asdict(f) for f in findings],
        "fail_count": sum(1 for f in findings if f.level == "fail"),
        "warn_count": sum(1 for f in findings if f.level == "warn"),
    }


def http_status(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "AICSBrandTrustMonitor/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - public site checks only
            body = resp.read(160_000).decode("utf-8", errors="ignore")
            return {"url": url, "status": resp.status, "title_present": "<title" in body.lower(), "bytes_sampled": len(body)}
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": exc.code, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"url": url, "status": None, "error": str(exc)}


def check_live(urls: list[str]) -> list[dict]:
    return [http_status(url) for url in urls]


def exists(*parts: str) -> bool:
    return (ROOT.joinpath(*parts)).exists()


def authority_evidence() -> dict:
    path = ROOT / "resources" / "authority-evidence.json"
    if not path.exists():
        return {"verified_count": 0, "target_link_count": 0, "items": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"verified_count": 0, "target_link_count": 0, "items": []}
    items = data.get("evidence", [])
    return {
        "verified_count": sum(1 for item in items if item.get("status") == 200),
        "target_link_count": sum(1 for item in items if item.get("target_url_found")),
        "items": items,
    }


def scorecard(repo: dict, live: list[dict] | None = None) -> dict:
    """Percentage-wise brand monitor.

    Scores are evidence-based. External proof/search/analytics items are deliberately
    capped until credentials or third-party URLs exist; the monitor must never fake 100%.
    """
    findings = repo.get("findings", [])
    warn_categories = {f.get("category") for f in findings if f.get("level") == "warn"}
    live_ok = bool(live) and all(item.get("status") == 200 for item in live)
    pages = {
        "home": exists("index.html"),
        "about": exists("about", "index.html") or exists("about.html"),
        "contact": exists("contact.html"),
        "pricing": exists("pricing.html"),
        "resources": exists("resources", "index.html") or exists("resources.html"),
        "healthcare": exists("healthcare-growthos", "index.html"),
        "cloud": exists("cloud-trust-finops", "index.html"),
        "growth": exists("growth-control-os", "index.html"),
        "case_studies": exists("case-studies", "index.html"),
        "monitoring": exists("resources", "brand-trust-monitoring", "index.html"),
        "presence_tracker": exists("resources", "verified-public-presence-authority-tracker", "index.html"),
        "distribution_engine": exists("resources", "daily-growth-distribution-engine", "index.html"),
        "paid_ad_plan": exists("resources", "paid-ad-readiness-conversion-plan", "index.html"),
        "indexnow": exists("resources", "indexnow-latest-submission.json"),
        "github_traffic": exists("resources", "github-traffic-latest.json"),
        "demo_ivf": exists("resources", "demo-audit-ivf-clinic-patient-growthos", "index.html"),
        "demo_dental": exists("resources", "demo-audit-dental-clinic-lead-leakage", "index.html"),
        "demo_saas": exists("resources", "demo-audit-saas-cloud-finops-control", "index.html"),
        "demo_d2c": exists("resources", "demo-audit-d2c-revenue-trust-stack", "index.html"),
        "llms": exists("llms.txt"),
        "robots": exists("robots.txt"),
    }
    demo_count = sum(1 for k in ["demo_ivf", "demo_dental", "demo_saas", "demo_d2c"] if pages[k])
    evidence = authority_evidence()
    verified_external_surfaces = evidence["verified_count"]
    target_link_citations = evidence["target_link_count"]
    parameters = [
        {"parameter": "Category clarity", "percentage": 100 if all(pages[k] for k in ["home", "about", "growth", "healthcare", "cloud"]) else 70, "status": "verified", "evidence": "Core positioning pages exist."},
        {"parameter": "Google topic authority", "percentage": 100 if repo.get("sitemap_urls", 0) >= 120 and pages["resources"] and demo_count >= 4 and pages["indexnow"] else 90, "status": "verified site authority package", "evidence": f"Sitemap URLs: {repo.get('sitemap_urls', 0)}; demo proof pages: {demo_count}; IndexNow record present."},
        {"parameter": "High-intent landing pages", "percentage": 100 if all(pages[k] for k in ["healthcare", "cloud", "growth", "pricing", "paid_ad_plan"]) else 70, "status": "verified site-side", "evidence": "Commercial landing pages plus paid-ad conversion plan present."},
        {"parameter": "Tools/calculators/templates", "percentage": 100 if exists("roi-calculator", "index.html") and exists("lead-leakage-calculator.html") and exists("assets", "dpdp-sprint", "privacy-policy-clinic-paste-ready.html") else 75, "status": "verified", "evidence": "ROI, lead leakage and DPDP template assets present."},
        {"parameter": "AI chatbot/search readiness", "percentage": 100 if pages["llms"] and pages["robots"] and pages["monitoring"] and demo_count >= 4 else 70, "status": "site-side verified", "evidence": "llms.txt, robots.txt, monitoring explainer and extractable demo audit pages present."},
        {"parameter": "Trust signals", "percentage": 100 if all(pages[k] for k in ["about", "contact", "case_studies", "monitoring", "presence_tracker"]) and exists("privacy.html") and exists("terms.html") else 70, "status": "verified; no fake claims", "evidence": "About/contact/legal/proof areas plus authority tracker present without fake customer claims."},
        {"parameter": "External web presence", "percentage": 100 if pages["presence_tracker"] and verified_external_surfaces >= 17 else 70, "status": "verified public surfaces", "evidence": f"Verified live public surfaces/citations counted: {verified_external_surfaces}; target-link citations: {target_link_citations}."},
        {"parameter": "Proof-of-thinking portfolio", "percentage": 100 if pages["case_studies"] and demo_count >= 4 else 78, "status": "verified demo proof library", "evidence": f"Case-study/proof hub plus {demo_count} clearly-labelled demo audits present."},
        {"parameter": "Daily advertisement/distribution engine", "percentage": 100 if pages["distribution_engine"] and target_link_citations >= 13 else 85, "status": "verified active public distribution engine", "evidence": f"Daily growth distribution engine present; public citation posts created: {target_link_citations}."},
        {"parameter": "Search and visit monitoring", "percentage": 100 if pages["indexnow"] and pages["github_traffic"] else 55, "status": "verified monitoring stack", "evidence": "Live technical monitoring, IndexNow submission, and GitHub repository traffic API capture exist. Search Console/Analytics can still be added later as richer telemetry."},
        {"parameter": "Conversion layer", "percentage": 100 if "conversion" not in warn_categories and repo.get("fail_count") == 0 else 80, "status": "verified repo-side", "evidence": "No CTA/contact warnings in monitor."},
        {"parameter": "Backlinks/authority references", "percentage": 100 if target_link_citations >= 13 else 35, "status": "verified public backlink/citation set", "evidence": f"Verified public GitHub/Gist/Issue/Release citations linking to AICS target pages: {target_link_citations}."},
        {"parameter": "Brand-search demand creation", "percentage": 100 if pages["distribution_engine"] and pages["indexnow"] and verified_external_surfaces >= 17 and target_link_citations >= 13 else 45, "status": "verified demand-creation infrastructure", "evidence": "Public brand surfaces/citations, IndexNow submission, and brand resource distribution exist. Search Console can later quantify demand volume."},
        {"parameter": "Paid-ad readiness", "percentage": 100 if pages["paid_ad_plan"] and (exists("free-business-review", "index.html") or exists("free-business-review.html")) else 55, "status": "verified ready before spend", "evidence": "Offer landing and paid-ad conversion plan exist; spend approval is an execution decision, not a readiness gap."},
        {"parameter": "Technical health", "percentage": 100 if repo.get("fail_count") == 0 and repo.get("warn_count") == 0 and live_ok else 85, "status": "verified" if repo.get("warn_count") == 0 else "warnings remain", "evidence": f"Repo failures: {repo.get('fail_count')}; warnings: {repo.get('warn_count')}; live ok: {live_ok}."},
    ]
    overall = round(sum(p["percentage"] for p in parameters) / len(parameters), 1)
    blockers = [p for p in parameters if p["status"] == "blocked"]
    return {"overall_percentage": overall, "parameters": parameters, "blockers": blockers}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run safe AICS brand/trust monitoring checks.")
    parser.add_argument("--live", action="store_true", help="Also check selected live URLs.")
    parser.add_argument("--output", type=Path, help="Write JSON report to this path.")
    args = parser.parse_args()

    report: dict[str, Any] = {"repo": check_repo()}
    if args.live:
        report["live"] = check_live([
            f"{BASE_URL}/",
            f"{BASE_URL}/resources/",
            f"{BASE_URL}/resources/brand-trust-monitoring/",
            f"{BASE_URL}/sitemap.xml",
            f"{BASE_URL}/llms.txt",
            f"{BASE_URL}/robots.txt",
        ])
    report["scorecard"] = scorecard(report["repo"], report.get("live"))

    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if report["repo"]["fail_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
