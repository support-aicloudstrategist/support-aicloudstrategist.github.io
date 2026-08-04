#!/usr/bin/env python3
"""Verify the Cloud FinOps Phase 4 release contract without deploying it."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "release" / "cloud-finops-phase4-release.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def redirect_rules() -> dict[str, tuple[str, str]]:
    rules = {}
    for line in (ROOT / "_redirects").read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) == 3 and not line.lstrip().startswith("#"):
            rules[parts[0]] = (parts[1], parts[2])
    return rules


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("production_deployment_authorized") is not False:
        fail("production hold must remain explicit until separate CEO authorization")

    for route, contract in manifest["required_routes"].items():
        page = ROOT / contract["source"]
        if not page.is_file():
            fail(f"missing route source: {page.relative_to(ROOT)}")
        html = page.read_text(encoding="utf-8")
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
        if canonical is None or canonical.group(1) != contract["canonical"]:
            fail(f"canonical mismatch for {route}")
        if contract["indexable"] and re.search(r'<meta[^>]+name="robots"[^>]+noindex', html, re.I):
            fail(f"indexable route is noindex: {route}")
        if '<meta name="robots" content="index, follow, max-image-preview:large">' not in html:
            fail(f"explicit index contract missing: {route}")

    for asset in manifest["required_assets"]:
        path = ROOT / asset
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"missing or empty asset: {asset}")

    rules = redirect_rules()
    for old, new in manifest["legacy_redirects"].items():
        if rules.get(old) != (new, "301"):
            fail(f"redirect mismatch: {old}")

    sitemap_root = ET.parse(ROOT / "sitemap.xml").getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {node.text for node in sitemap_root.findall(".//s:loc", namespace)}
    required_urls = {contract["canonical"] for contract in manifest["required_routes"].values()}
    if not required_urls.issubset(sitemap_urls):
        fail("authority or evidence route missing from sitemap")
    for old in manifest["legacy_redirects"]:
        legacy_url = f"https://aicloudstrategist.com{old}"
        if legacy_url in sitemap_urls:
            fail(f"legacy redirect remains in sitemap: {old}")

    for relative, expected in manifest["sha256"].items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"provenance file missing: {relative}")
        actual = digest(path)
        if actual != expected:
            fail(f"provenance mismatch: {relative}; expected {expected}, got {actual}")

    service = (ROOT / "services/cloud-finops/index.html").read_text(encoding="utf-8")
    pack = (ROOT / "resources/cloud-ai-economics-decision-pack/index.html").read_text(encoding="utf-8")
    if '"@type": "Service"' not in service or '"@type": "CreativeWork"' not in pack:
        fail("connected structured-data entities are missing")
    if 'not client work, a benchmark, a case study or a savings claim' not in pack:
        fail("Decision Pack synthetic evidence boundary is missing")

    print(
        "PASS: Cloud FinOps Phase 4 release contract verified — "
        f"{len(manifest['required_routes'])} routes, "
        f"{len(manifest['legacy_redirects'])} redirects, "
        f"{len(manifest['sha256'])} provenance hashes; production hold intact."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
