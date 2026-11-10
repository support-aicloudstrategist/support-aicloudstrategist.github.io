#!/usr/bin/env python3
"""Fail-closed verifier for the November 2026 one-service website release."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FOCUSED_TESTS = [
    "tests/test_one_service_homepage_foundation.py",
    "tests/test_core_one_service_pages.py",
    "tests/test_motion_and_responsive_contract.py",
    "tests/test_fit_review_privacy_trust.py",
    "tests/test_marketing_readiness_seo.py",
    "tests/test_contact_reliability.py",
    "tests/test_cloud_ai_economics_decision_pack.py",
]


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)


def main() -> None:
    run([sys.executable, "-m", "pytest", *FOCUSED_TESTS, "-q"])
    run(["git", "diff", "--check"])
    print("PASS: one-service release contract")


if __name__ == "__main__":
    main()
