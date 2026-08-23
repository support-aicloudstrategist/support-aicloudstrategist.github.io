#!/usr/bin/env python3
"""Build the AICS sitemap from indexable public HTML canonical URLs.

The brand/trust monitor checks every public HTML page. A curated 50-URL
sitemap created false technical warnings as the site grew, so this script now
keeps sitemap coverage aligned with real indexable pages while excluding
noindex redirects, backups, local previews, and non-public build folders.
"""
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


def public_html_files() -> list[Path]:
    pages: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        parts = set(path.relative_to(ROOT).parts)
        name = path.name.lower()
        if parts & PUBLIC_SKIP_PARTS:
            continue
        if name.endswith(".backup.html") or "-old/" in rel or name.startswith("google"):
            continue
        pages.append(path)
    return sorted(pages)


def is_indexable(source: str) -> bool:
    robots = ROBOTS_RE.search(source)
    return not (robots and "noindex" in robots.group(1).lower())


def canonical_url(path: Path, source: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    match = CANONICAL_RE.search(source)
    if not match:
        raise SystemExit(f"missing canonical: {rel}")
    url = match.group(1).strip()
    if not url.startswith(BASE_URL):
        raise SystemExit(f"non-AICS canonical in public sitemap: {rel} -> {url}")
    return url if url == f"{BASE_URL}/" else url.rstrip("/")


def priority_for(url: str) -> str:
    path = url.removeprefix(BASE_URL)
    if path in {"", "/"}:
        return "1.0"
    if path in {"/free-business-review", "/free-business-review/", "/contact", "/pricing"}:
        return "0.9"
    if path.startswith("/services/") or path in {"/healthcare-growthos", "/growth-control-os", "/ai-cloud-cost-efficiency"}:
        return "0.8"
    if path.startswith("/resources") or path.startswith("/case-studies") or path.startswith("/publications"):
        return "0.7"
    return "0.6"


def changefreq_for(url: str) -> str:
    path = url.removeprefix(BASE_URL)
    if path in {"", "/", "/resources", "/case-studies"} or path.startswith("/publications"):
        return "weekly"
    return "monthly"


def build_urls() -> list[str]:
    urls: set[str] = set()
    for path in public_html_files():
        source = path.read_text(encoding="utf-8", errors="ignore")
        if not is_indexable(source):
            continue
        urls.add(canonical_url(path, source))
    return sorted(urls, key=lambda u: (u != f"{BASE_URL}/", u))


def main() -> None:
    urls = build_urls()
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        loc = html.escape(url)
        lines.append(
            f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{changefreq_for(url)}</changefreq><priority>{priority_for(url)}</priority></url>"
        )
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(urls)} sitemap URLs")


if __name__ == "__main__":
    main()
