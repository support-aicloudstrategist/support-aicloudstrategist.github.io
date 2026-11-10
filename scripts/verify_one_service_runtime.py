#!/usr/bin/env python3
"""Verify Cloudflare Pages runtime behavior for the one-service website."""

from __future__ import annotations

import argparse
import json
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(base: str, path: str, accept: str | None = "*/*", method: str = "GET", host: str | None = None):
    opener = build_opener(NoRedirect)
    headers = {"User-Agent": "AICS-release-verifier/1.0"}
    if accept is not None:
        headers["Accept"] = accept
    if host:
        headers["Host"] = host
    request = Request(
        urljoin(base.rstrip("/") + "/", path.lstrip("/")),
        headers=headers,
        method=method,
    )
    try:
        return opener.open(request, timeout=30)
    except HTTPError as error:
        return error


def post_without_consent(base: str):
    payload = json.dumps({"name": "Release probe", "contact": "probe@example.com", "company": "AICS release verification", "need": "Consent validation"}).encode()
    request = Request(
        urljoin(base.rstrip("/") + "/", "api/contact"),
        data=payload,
        method="POST",
        headers={
            "Origin": "https://aicloudstrategist.com",
            "Sec-Fetch-Site": "same-site",
            "Content-Type": "application/json",
            "User-Agent": "AICS-release-verifier/1.0",
        },
    )
    try:
        return build_opener(NoRedirect).open(request, timeout=30)
    except HTTPError as error:
        return error


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", help="Cloudflare preview or production base URL")
    parser.add_argument("--preview-host", help="Optional pages.dev Host header for testing a local Wrangler runtime")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    for path in ["/", "/privacy", "/terms", "/cloud-ai-cost-governance-diagnostic/", "/request-fit-review/", "/trust-data-handling/", "/resources/", "/resources/cloud-ai-economics-decision-pack/"]:
        response = fetch(base, path)
        require(response.status == 200, f"{path} returned {response.status}")
        require("text/html" in response.headers.get("Content-Type", ""), f"{path} is not text/html")

    redirects = {
        "/services/cloud-ai-economics/": "/cloud-ai-cost-governance-diagnostic/",
        "/services/cloud-finops/": "/cloud-ai-cost-governance-diagnostic/",
        "/free-business-review/": "/request-fit-review/",
        "/pricing/": "/cloud-ai-cost-governance-diagnostic/",
    }
    for path, target in redirects.items():
        response = fetch(base, path)
        require(response.status == 301, f"{path} returned {response.status}, expected 301")
        location = response.headers.get("Location", "")
        require(urlparse(location).path == target, f"{path} redirected to {location}")

    for path in ["/advisory.html", "/services/", "/services/production-ai-readiness/", "/definitely-missing-release-check"]:
        response = fetch(base, path, accept="*/*")
        require(response.status == 404, f"{path} with Accept */* returned {response.status}")
        require("noindex" in response.headers.get("X-Robots-Tag", ""), f"{path} lacks noindex")

    consent_response = post_without_consent(base)
    require(consent_response.status == 422, f"contact API accepted missing privacy consent with {consent_response.status}")

    base_hostname = urlparse(base).hostname or ""
    preview_host = args.preview_host or (base_hostname if base_hostname.endswith(".pages.dev") else None)
    if preview_host:
        require(preview_host.endswith(".pages.dev"), "--preview-host must be a pages.dev hostname")
        canonical_html = [
            "/", "/privacy", "/terms", "/cloud-ai-cost-governance-diagnostic/",
            "/request-fit-review/", "/trust-data-handling/", "/resources/",
            "/resources/cloud-ai-economics-decision-pack/",
        ]
        for path in canonical_html:
            for method in ["GET", "HEAD"]:
                for accept in ["*/*", "text/html", None]:
                    response = fetch(base, path, accept=accept, method=method, host=preview_host)
                    require(response.status == 200, f"preview {method} {path} returned {response.status}")
                    require(
                        "noindex" in response.headers.get("X-Robots-Tag", ""),
                        f"preview {method} {path} with Accept {accept!r} lacks noindex",
                    )

    print("PASS: Cloudflare one-service runtime behavior")


if __name__ == "__main__":
    main()
