# GEO 90+ Content Authority Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task after Raj approves public website copy changes.

**Goal:** Move AICloudStrategist from Fair GEO readiness toward 85–90+ by converting technical GEO plumbing into honest proof, stronger homepage extraction text, deeper brand/entity signals, and measurable external authority actions.

**Architecture:** Keep the current premium visual design and existing positioning. Add only truthful, publicly defensible proof assets: self-case studies, diagnostic teardowns, sample scenarios clearly labelled as examples, and client case-study slots only after approval. Avoid fake client names, fake logos, fake outcomes, fake reviews, or implied legal guarantees.

**Tech Stack:** Static HTML/CSS site in `support-aicloudstrategist.github.io`, Cloudflare Pages/GitHub Pages deployment, JSON-LD schema, llms.txt, sitemap.xml, social/profile/entity updates outside repo.

---

## Non-negotiable claim policy

We can improve the case-study score without inventing customers:

- Allowed: public self-case study using the real GEO result: 37/100 → 67/100 after technical fixes.
- Allowed: sample/representative case-study pages clearly labelled "sample scenario" or "example audit teardown".
- Allowed: anonymized pilot/client result only if Raj confirms it is real and approved.
- Not allowed: fake client names, fake testimonials, fake ratings, fake logos, fake certifications, fake savings, fake healthcare clinic outcomes.

This protects the brand while still giving AI systems extractable proof-style content.

---

## Task 1: Replace thin case-studies placeholder with honest proof hub

**Objective:** Turn `/case-studies/` from a 133-word placeholder into a citable proof hub.

**Files:**
- Modify: `case-studies/index.html`
- Potential create: `case-studies/aicloudstrategist-geo-turnaround/index.html`
- Potential create: `case-studies/sample-healthcare-growthos-lead-recovery/index.html`
- Potential create: `case-studies/sample-cloud-finops-cost-optimization/index.html`

**Implementation:**
1. Keep the existing proof policy but move it below the hero.
2. Add three cards:
   - "AICloudStrategist GEO turnaround: 37 → 67 in one implementation cycle" — real self-case study.
   - "Sample Healthcare GrowthOS lead-recovery teardown" — clearly labelled sample scenario.
   - "Sample AI/cloud cost optimization teardown" — clearly labelled sample scenario.
3. Add copy explaining which pages are real results vs sample scenarios.
4. Add `ItemList` schema for the proof hub.
5. Add `CreativeWork`/`Article` schema for the self-case-study page.
6. Do not add Review/AggregateRating yet.

**Verification:**
- Live `/case-studies/` has at least 700–1,000 words of useful proof/process content.
- Page has no fabricated client names or testimonials.
- JSON-LD parses with 0 errors.

---

## Task 2: Publish real self-case study: GEO turnaround

**Objective:** Create the first legitimate case study using our own audited website improvement.

**Files:**
- Create: `case-studies/aicloudstrategist-geo-turnaround/index.html`
- Modify: `sitemap.xml`
- Modify: `llms.txt`

**Content outline:**
- Before: GEO score 37/100 Critical.
- After: GEO score 67/100 Fair.
- Improvements shipped:
  - AI crawlers unblocked.
  - `llms.txt` published.
  - Organization/WebSite/WebPage/Person/Breadcrumb schema added.
  - FAQPage, Article, Service, Offer schema added where relevant.
  - Cloudflare Managed robots setting corrected.
- Result: +30 score movement in same-day re-audit.
- Boundary: This is an internal/public self-case study, not a client case study.
- Next target: proof, homepage depth, profile authority, verified reviews.

**Schema:**
- `Article`
- `CreativeWork`
- `AboutPage` or `WebPage`
- `BreadcrumbList`

**Verification:**
- Page is indexable and linked from `/case-studies/`.
- `llms.txt` references the case study under proof/results.
- Sitemap includes `lastmod`.

---

## Task 3: Add substantive homepage intro block without damaging the premium splash design

**Objective:** Make the root URL citable while preserving the current path-chooser look.

**Files:**
- Modify: `index.html`

**Implementation:**
1. Add a compact intro block directly below the hero text and above the two path cards.
2. Keep it visually light: three short proof/positioning cards or a one-row summary.
3. Suggested copy:
   - "AICloudStrategist builds Growth & Control OS systems for serious businesses: premium websites, enquiry capture, follow-up automation, trust readiness, AI creative assets, and AI/cloud cost control."
   - "For healthcare and local-service businesses, the focus is missed-lead recovery, WhatsApp follow-up, DPDP-aware consent flows, and owner dashboards."
   - "For SaaS, AI, fintech, and cloud-heavy teams, the focus is spend visibility, waste detection, GPU/LLM inference cost review, and FinOps action plans."
4. Add `Service`/`ItemList` schema for the two main lines if not already represented.

**Verification:**
- Homepage remains visually premium and mobile-friendly.
- Root page has enough extractable text to answer "what does AICloudStrategist do?" without needing inner pages.
- JSON-LD parses with 0 errors.

---

## Task 4: Strengthen founder/entity narrative consistently

**Objective:** Reduce positioning confusion across site, llms.txt, and social profiles.

**Files:**
- Modify: `about/index.html`
- Modify: `llms.txt`
- Potential modify: footer/profile links if needed

**Implementation:**
1. Keep Anushka Bhattacharya as public Director and main public-facing person.
2. Present Rajiv's 22+ years IT/cloud/operations experience only where already approved as public and factual.
3. Unify positioning as:
   - "AICloudStrategist builds Growth & Control OS systems: Healthcare GrowthOS for clinics/local services plus Cloud Trust/FinOps for cloud-heavy teams."
4. Avoid over-rotating into unrelated SaaS Series A–C messaging on the main site unless it is framed as the Cloud Trust/FinOps lane.

**Verification:**
- About page, homepage, llms.txt, and Organization description do not conflict.
- No private identity exposure beyond already-approved public facts.

---

## Task 5: Backfill sitemap `lastmod` values

**Objective:** Fix the remaining low-priority technical issue from the audit.

**Files:**
- Modify: `sitemap.xml`

**Implementation:**
1. Identify URLs without `lastmod`.
2. Add ISO dates for all key pages and newer resource URLs.
3. Ensure newly created case-study URLs are included.

**Verification:**
- XML parses successfully.
- All important URLs have `lastmod`.

---

## Task 6: Create brand authority execution checklist outside the repo

**Objective:** Improve the biggest remaining GEO ceiling: third-party corroboration.

**Files:**
- Create: `docs/plans/2026-06-09-brand-authority-execution-checklist.md`

**Implementation checklist:**
1. LinkedIn company page:
   - Add full company description.
   - Link back to website.
   - Publish 3 posts: GEO case study, Healthcare GrowthOS, Cloud Trust/FinOps.
2. YouTube:
   - Add description and website link.
   - Publish/prepare 1 short explainer video or at least a channel trailer placeholder.
3. Reddit/DEV.to:
   - Publish useful non-spam educational posts linking to relevant resource pages.
4. Google Business Profile / Clutch:
   - Create/complete profile if available.
   - Request only real reviews from real customers/partners/pilots.
5. Directory/listicle outreach:
   - Submit to India DPDP/compliance, healthcare marketing, cloud cost/FinOps, and AI automation directories.

**Verification:**
- Each profile links back to the website.
- Each profile uses consistent description, contact, and category.
- No fake reviews or fake third-party claims.

---

## Task 7: Add Review/AggregateRating schema only after real reviews exist

**Objective:** Prepare schema enhancement without prematurely publishing false ratings.

**Files:**
- Modify later: `index.html`, `case-studies/index.html`, relevant service pages

**Implementation:**
1. Wait until verified reviews exist on Google/Clutch or client-approved testimonials exist.
2. Add `Review` or `AggregateRating` only with the actual source and rating data.
3. Link the visible review text to the schema.

**Verification:**
- Visible review content matches schema exactly.
- Source is public or client-approved.

---

## Expected score movement

**Realistic next re-audit target after repo work only:** 75–82.

**Path to 90+:** possible only after off-site authority exists: populated profiles, verified reviews, third-party mentions/listings, and repeated content activity. Technical/site-side changes alone should not be promised as 90+ because the audit itself says brand authority is the biggest ceiling.

---

## Rollout sequence

1. Raj approves this plan and public copy direction.
2. Implement Tasks 1–5 in repo.
3. Validate locally: HTML links, JSON-LD, sitemap XML.
4. Commit and push to production branch.
5. Verify production pages with `curl` and visual browser check.
6. Start Task 6 off-site profile/content authority work.
7. Re-run GEO audit after production deploy.
8. Re-run again after 2–4 weeks of third-party/profile activity.
