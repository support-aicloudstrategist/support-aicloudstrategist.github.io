# One-Service Release Test Retirement and Waiver — 2026-11-10

## Scope

This record applies only to the AICloudStrategist website migration from the historical multi-service estate to the approved single public service: **Cloud & AI Cost Governance Diagnostic**.

## Why the complete historical suite is not the release gate

The repository accumulated hundreds of route- and publication-specific tests for services, pricing bridges, industries, regional landing pages, daily publications and discovery surfaces that the approved one-service strategy intentionally retires from the public journey. Those tests assert the continued promotion and indexability of pages that must now redirect, return 404, or remain outside the launch allowlist.

Treating those expectations as current release requirements would contradict the approved product and information architecture. The tests are retained in Git and in the pre-rebuild archive for historical reconstruction; they are not deleted or represented as passing.

## Recorded results

- Archived production baseline `cfc5ef5f64c7e3aaa7bcbf672c9412d8d188e73b`: **1,024 passed, 636 failed** after manually installing undeclared historical dependencies.
- Final candidate before preview verification: **1,019 passed, 684 failed, 834 subtests passed**.
- The additional failures are concentrated in intentionally retired multi-service navigation, pricing, regional/service pages, publication discovery wiring, old sitemap/indexability rules and legacy conversion routes.

## Current fail-closed release gate

The release is governed by `scripts/verify_one_service_release.py`, which executes the current contracts for:

- one-service homepage and navigation;
- core service, resources, About and representative Decision Pack;
- responsive motion and reduced-motion behavior;
- fit-review form, server-confirmed delivery, privacy consent and trust boundaries;
- canonical metadata, sitemap, redirects, middleware allowlist and security headers;
- contact endpoint reliability;
- the complete ten-output synthetic Decision Pack, searchable PDF and builder.

Current result: **63 passed, 66 subtests passed**.

Browser and deployment evidence remains separately required: HTML validation, Axe, Lighthouse, route/asset crawl, Cloudflare preview behavior, both deployment planes and post-deploy checks.

## What is not waived

This record does not waive security failures, form false-success, accessibility violations, broken canonical routes, missing assets, unsupported claims, data-boundary failures, production/preview disagreement, or rollback failures. Any such finding remains a release blocker.

## Follow-up

Historical tests should later be moved into a clearly labelled archive suite or rewritten against the one-service route disposition ledger. Until then, they remain preserved evidence rather than the active release contract.
