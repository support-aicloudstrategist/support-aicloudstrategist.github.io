#!/usr/bin/env python3
"""Restore legacy HTML bodies after the one-time noindex migration trial.

Indexability is enforced centrally by Pages middleware. This keeps the release
reviewable and avoids touching hundreds of historical documents only to add a
robots meta tag.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
KEEP = {
    "index.html", "pricing.html", "pricing/index.html",
    "free-business-review.html", "free-business-review/index.html",
    "about.html", "about/index.html", "resources.html", "resources/index.html",
    "services/production-ai-readiness/index.html",
    "services/cloud-ai-economics/index.html",
}

changed = subprocess.check_output(
    ["git", "diff", "--name-only", "--", "*.html"], cwd=ROOT, text=True
).splitlines()
restored = 0
for rel in changed:
    if rel in KEEP:
        continue
    try:
        content = subprocess.check_output(["git", "show", f"main:{rel}"], cwd=ROOT)
    except subprocess.CalledProcessError:
        continue
    (ROOT / rel).write_bytes(content)
    restored += 1
print(f"Restored {restored} legacy HTML files; middleware now controls their indexing header.")
