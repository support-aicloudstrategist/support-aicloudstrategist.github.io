# AICloudStrategist Daily Lead Source Engine

_Date: 2026-05-13_  
_Goal: source 200-300 verified prospect contact records/day, scalable to 400/day, for AICloudStrategist without outreach, invented data, credential abuse, CAPTCHA bypass, or aggressive scraping._

## Executive recommendation

Build a **source-mix + verification pipeline**, not a single scraper. The safest daily mix is:

| Bucket | Daily verified target | Why |
|---|---:|---|
| Google Maps / Places + business websites | 80-120 | Broad, current, high phone/website coverage; email usually from site enrichment |
| Vertical directories: Justdial, Sulekha, Practo, coaching/clinic/industry directories | 40-70 | Good local segmentation and phone likelihood; use manual/browser-assisted export where permitted |
| B2B marketplaces: IndiaMART, TradeIndia, export/manufacturing directories | 40-70 | Strong manufacturer/exporter/vendor fit; phone likely, email mixed |
| Public institutions: MSME/Udyam stats, chambers, associations, incubators, startup/SaaS directories | 30-50 | Higher credibility and company context; contact details vary |
| LinkedIn + company sites + Apollo limited enrichment | 25-40 | Decision-maker context; use Apollo only within the 25/day credit limit |
| Referrals/communities/GitHub/product directories | 10-25 | Lower volume, higher relevance for SaaS/tech/cloud/AI segments |

Expected output after dedupe + validation: **200-300 usable records/day** from ~350-500 raw candidates. Push toward 400/day only after measuring bounce/invalid/duplicate rates and ensuring terms/compliance are stable.

## Compliance guardrails

1. **No outreach in this engine.** It only discovers, verifies, classifies, and queues records.
2. **TRAI/TCCCPR caution:** TRAI's TCCCPR framework protects users from unsolicited commercial communications and requires commercial communications to align with recipient preferences/consent. Treat India phone/WhatsApp outreach as high-risk without consent, DND checks, clear opt-out, and proper entity registration/processes.
3. **DPDP Act caution:** Personal data such as named contacts, mobile numbers, and individual emails should be processed only for a lawful purpose, with minimization, retention limits, security controls, and deletion/opt-out handling.
4. **Prefer business-level records first:** company name, public business phone, website, generic email, address, category. Capture named individual contacts only when they are clearly published in a business context.
5. **Respect source terms:** use official APIs/exports where available; otherwise use low-rate manual/browser-assisted collection of publicly visible data. Do not bypass login, paywalls, CAPTCHAs, robots controls, or anti-bot systems.
6. **Maintain suppression lists:** DND/opt-out, previous invalids, competitors, existing customers, and do-not-contact requests.
7. **Evidence every record:** store source URL, capture date, extraction method, and validation status.

## Priority segments for AICloudStrategist

Best-fit prospects for AI/cloud/automation consulting:

1. **Clinics, hospitals, diagnostic centers, dental/IVF/eye clinics** — appointment automation, WhatsApp workflows, CRM, analytics.
2. **Coaching institutes, training centers, schools, colleges, edtech providers** — lead management, admissions automation, content/chatbots.
3. **Manufacturers, exporters, industrial suppliers, machine/component firms** — ERP/CRM integration, quote automation, AI sales assistants, inventory analytics.
4. **Local service chains and SMEs** — salons, gyms, real estate agencies, logistics, repair services; focus on multi-location or high-review businesses.
5. **SaaS/startups/IT services** — cloud optimization, AI feature prototyping, internal automation.
6. **Professional services** — CA/law firms, architects, consultants; AI knowledge search, document automation.

## Source intelligence matrix

Scoring: Quality 1-5; compliance risk Low/Med/High; volume is realistic verified output/day after respectful limits and dedupe.

| Source | Available fields | Phone/WhatsApp likelihood | Email likelihood | Quality | Realistic volume/day | Cost/free limits | Compliance risks | Automation method | Dedupe strategy | Validation method | Recommended segments | First implementation steps |
|---|---|---:|---:|---:|---:|---|---|---|---|---|---|---|
| Google Maps / Google Business Profiles via Places API | business name, category/type, address, geo, rating/reviews, hours, website, national/international phone, business status, Google maps URL/place ID | High | Low directly; medium after website crawl | 4 | 80-150 | Paid API after free credits; fields billed by SKU; contact fields cost more | API ToS, no storing beyond terms without review; avoid scraping Maps UI | Official Places Text/Nearby Search + Place Details with field masks | `google_place_id`, normalized phone, domain, name+pin code | Places phone format, website reachable, businessStatus operational, site email extraction | Clinics, coaching, local SMEs, manufacturers by city/category | Create keyword-city grid; call Text Search for candidate IDs; fetch Details only for shortlisted records; crawl websites for generic emails |
| Business websites found from Maps/search | about/services pages, generic emails, public phones, contact forms, social links, founders/team sometimes | Medium | High for generic email | 4 | 60-120 enrichment records | Free; bandwidth/rate constrained | Respect robots, terms, privacy; no form submissions | Lightweight crawler limited to contact/about/footer pages; no login | root domain, canonical URL, company name | MX check, syntax check, role email classification, phone E.164 normalization | All segments | Build safe crawler: max 5 pages/domain, 1 req/sec/domain, cache HTML, extract emails/phones/schema.org |
| Justdial | local business name, category, address, ratings, phone often visible after interaction/login, hours, photos | High | Low | 3 | 20-50 | Free browsing; paid ads/data options vary | Scraping/automation likely restricted; phone data sensitive | Prefer manual export/vendor/official allowed access; browser-assisted review only | phone, business name+locality, Justdial URL | Call-format validation, Google cross-check, website cross-check | Local services, clinics, coaching, agencies | Define city/category lists; manually collect small batches; avoid bulk scraping or CAPTCHA bypass; enrich from websites |
| Sulekha | local service provider, category, city, phone/contact flow, ratings/reviews, sometimes website | High | Low | 3 | 15-40 | Free browsing; lead/contact flows may require account | Terms/contact-flow restrictions; avoid triggering inquiries | Manual/browser-assisted collection of visible public fields; no automated contact requests | phone, provider name+city, Sulekha URL | Cross-check on Google/site; mark source as directory | Coaching, home/local services, consultants | Use for gaps in local services; collect only public listing info; enrich via search/site |
| Practo / healthcare directories | clinic/doctor name, specialty, address, clinic phone/booking link, fees/hours, ratings | Medium-high for clinic phone | Low | 4 | 10-30 | Free browsing; API not generally open | Medical/professional context; avoid collecting patient data; terms restrictions | Manual/browser-assisted public listing capture | clinic name+address, phone, Practo URL | Google/website cross-check; specialty normalization | Clinics, dental, diagnostics, specialist practices | Use only business/clinic contact data; prioritize clinic pages over individual doctor mobile numbers |
| IndiaMART | company/supplier name, products, city, GST/member indicators, phone/contact button, sometimes email, owner/contact person | High | Medium-low | 4 | 30-70 | Free browsing; paid seller/buyer tools; no assumed bulk export | Marketplace terms, contact reveal flows, anti-bot; avoid scraping logged-in/contact-protected data | Manual/browser-assisted or compliant data provider; collect public supplier pages slowly | IndiaMART supplier URL, phone, company+city, GST if public | Website/GST/public cross-check, phone normalization, product-category fit | Manufacturers, exporters, industrial suppliers | Start with product keywords aligned to AI automation use cases; collect public supplier/company pages; enrich company website |
| TradeIndia | supplier/company, products, location, phone/contact, website sometimes, membership age | High | Medium-low | 4 | 20-50 | Free browsing; paid services | Marketplace terms/contact protection | Manual/browser-assisted public data; possible approved vendor data | TradeIndia URL, phone, company+city | Website/domain validation, phone, product-category taxonomy | Manufacturers/exporters/B2B sellers | Build keyword list: packaging, machine tools, textiles, pharma equipment, auto components; verify companies via website |
| Export/import/manufacturing directories (EEPC, FIEO member lists, ExportersIndia, Kompass, industry portals) | company, sector, city, products, website, phone/email sometimes | Medium | Medium | 4 | 20-50 | Mixed free/paid | Paid/member data terms; avoid copying protected lists | Official directories/manual export where allowed; low-rate public pages | company+domain, phone, membership ID if public | Website/MX, public membership page | Exporters, manufacturers, B2B service firms | Identify 5 industry directories and permitted export formats; collect public member pages only |
| MSME/Udyam public data/data.gov.in | aggregated/list datasets by district/sector; may not include direct contact details | Low | Low | 2 for contact, 4 for market sizing | 0-20 direct; strong for targeting | Public dataset/API; may require API key | Dataset may be aggregate/not for contact; don't infer personal data | Use data.gov.in API/download for targeting city/sector density, then source contacts elsewhere | district+NIC+company if company-level available | Cross-source with Maps/directories | MSME-heavy districts/sectors | Use for prioritizing geographies and NIC/sector keywords; not primary contact source |
| Local chambers/associations (CII/FICCI local chapters, TiE, BNI public pages, district industry associations, trade bodies) | member company, sector, website, office phone/email, leadership | Medium | Medium-high | 4 | 15-40 | Often public; some member-only | Member directory terms; avoid gated lists | Manual export from public pages; email chamber for permission if needed for bulk | domain, membership ID/name+city | Website/MX and association page evidence | Established SMEs, exporters, startups | Build chamber list by city; capture public member pages; tag association/source confidence |
| LinkedIn | company page, employees, job titles, location, website, public profile URLs | Low for phone | Low unless paired with email tools | 4 for role targeting | 20-40 research records | Free search limited; Sales Navigator paid; strict anti-scraping | LinkedIn ToS; personal data; no scraping automation | Manual/Sales Nav exports where licensed; use public company pages; no bot scraping | LinkedIn company URL, domain, person profile URL | Company website, role recency, Apollo/manual email check | SaaS, startups, mid-market, decision makers | Use LinkedIn to identify decision-maker names/titles; keep contact enrichment to Apollo/company site only |
| Apollo.io (25/day limit as specified) | company, contact name/title, work email, sometimes phone, LinkedIn URL, tech/firmographic data | Medium for phone | High | 4 | 25 enriched contacts/day | User-specified 25/day limit; paid tiers vary | Terms, consent, personal data, email outreach restrictions | Official Apollo UI/API/export within credit limits | Apollo person/company ID, email, LinkedIn URL | Apollo verification status + external MX + domain match | SaaS, funded startups, exporters, larger SMEs | Reserve credits for high-intent accounts found elsewhere; enrich only 25/day with target personas |
| GitHub/org repos | org name, website, public emails in org/repo/profile, tech stack, activity | Low | Medium for tech contacts/generic | 3 | 5-15 | GitHub API rate limits; free auth limits | Personal emails; respect public API terms; avoid harvesting private data | GitHub Search/API for orgs by geography/tech; manual review | GitHub org URL, domain, email hash | Domain match, commit recency, website | SaaS/dev shops/open-source vendors | Search India + cloud/AI/SaaS repos; capture org/site, not mass personal emails |
| SaaS/startup directories (Crunchbase, Tracxn, AngelList/Wellfound, Product Hunt, SaaS directories, Startup India) | company, category, location, website, founders sometimes, funding/stage | Low | Medium via website | 4 | 15-35 | Many paid/limited; Startup India public | Terms/paywalls; personal data | Use official exports/subscriptions or manual public pages | domain, directory ID, company name | Website, LinkedIn, email/MX | SaaS/startups/IT services | Use filters: India, B2B SaaS, AI, healthcare/education/manufacturing tech; enrich website |
| Marketplaces (Shopify stores, Amazon/Flipkart sellers where public, ONDC/storefronts, app marketplaces) | seller/store, website, support email/phone sometimes, category | Medium | Medium | 3 | 10-25 | Mixed | Marketplace terms; seller contact may be for support only | Manual public pages; no protected seller data | domain/storefront, support email, brand name | Website/social cross-check | D2C, e-commerce SMEs, app vendors | Collect public brand websites, not marketplace-protected seller accounts |
| Communities/referrals/events (Meetup, Eventbrite, TiE events, WhatsApp groups with permission, local founder communities) | company/person, context, website/social, sometimes email | Low-medium | Medium | 5 but low scale | 5-20 | Free/paid events | Consent and group rules; do not mine private groups | Manual capture only with permission/public pages | person/company+event URL | Manual qualification | High-trust local SMEs/startups | Create referral/source note fields; only add contacts from public attendee/speaker/sponsor pages or explicit referrals |

## Validation and enrichment design

### Record states

1. `raw_candidate` — discovered from a source; not yet deduped.
2. `deduped_account` — account/domain/phone deduped.
3. `contact_verified` — phone/email/website checks passed.
4. `qualified` — segment/persona fit and source evidence checked.
5. `suppressed` — opt-out/DND/existing customer/invalid/duplicate/terms issue.
6. `ready_for_review` — human can approve for CRM import or future compliant outreach process.

### Validation checks

- **Company/account:** source URL reachable, name/category/city present, duplicate check, operational status where available, business website/domain present or phone present.
- **Phone:** normalize to E.164, remove obvious invalid/shared directory numbers, flag mobile vs landline, India DND caution flag for mobile/WhatsApp. Do not call or message.
- **Email:** syntax, role vs personal classification, domain match, MX lookup, disposable-domain check. Avoid SMTP probing unless legally reviewed.
- **Website:** HTTP 200/3xx, domain not parked, contact/about page found, category keywords match segment.
- **Fit score:** industry relevance, business size proxy, tech/automation need signals, location, source confidence.
- **Evidence:** store source URL, extraction timestamp, method, screenshot/hash optional for audit.

## Dedupe strategy

Use layered deterministic + fuzzy matching:

1. Exact keys: `google_place_id`, `source_record_id`, `domain`, `email`, normalized `phone_e164`, LinkedIn company URL.
2. Account fuzzy key: normalized company name + city + postal code/locality.
3. Domain family: canonical root domain, strip `www`, UTM, paths.
4. Phone family: collapse whitespace, country code, leading zero, multiple numbers split into child rows.
5. Person key: lower(email) if present; otherwise person name + company domain + LinkedIn URL.
6. Suppression join before output: opt-out, DND-sensitive, invalid, existing customer, competitor, previously exported.

## Recommended CSV schema

One row should represent **one contact at one account**. For account-only leads, keep person fields blank and use generic role/contact fields.

```csv
record_id,run_date,status,source_primary,source_secondary,source_url,source_record_id,extraction_method,evidence_captured_at,
company_name,company_legal_name,brand_name,segment,subsegment,industry_keywords,products_services,company_size_estimate,
address_line,locality,city,state,country,pincode,latitude,longitude,
website,domain,google_place_id,google_maps_url,linkedin_company_url,github_org_url,other_profile_url,
contact_type,contact_name,job_title,department,seniority,linkedin_profile_url,
email,email_type,email_validation_status,email_validation_notes,phone_raw,phone_e164,phone_type,phone_validation_status,whatsapp_likelihood,
rating,review_count,business_status,opening_hours_present,source_quality_score,fit_score,priority_score,
consent_basis,public_business_contact_flag,dnd_caution_flag,opt_out_status,suppression_reason,
dedupe_account_key,dedupe_contact_key,duplicate_of,enrichment_needed,next_review_action,notes
```

### Minimum required fields for export

`record_id`, `run_date`, `source_primary`, `source_url`, `company_name`, `segment`, `city/state/country`, at least one of `website/email/phone`, `validation_status`, `source_quality_score`, `fit_score`, `dnd_caution_flag`, `opt_out_status`, `dedupe_account_key`.

## Daily workflow for 200-300 verified contacts

### Setup assumptions

- 1 operator + automated scripts for permitted APIs/site crawling.
- No outreach, calls, or WhatsApp messages.
- Daily raw target: 350-500 candidates.
- Expected survival after dedupe/validation: 55-70%.

### Morning: target planning (30 min)

1. Pick 2-3 segments/day, e.g. `clinics Pune`, `coaching Ahmedabad`, `industrial suppliers Coimbatore`.
2. Allocate source quotas:
   - Maps/API: 150 raw
   - Websites/enrichment: 100 raw/enriched
   - B2B directories: 100 raw
   - Associations/startup directories: 50 raw
   - Apollo: 25 enriched people/accounts
3. Exclude recently covered cities/segments and suppression lists.

### Collection block 1: Maps + website enrichment (2-3 hr automated + review)

1. Query Google Places Text Search by keyword-city pairs.
2. Fetch only needed fields with field masks: name, address, types, website, phone, rating/reviews, business status, place ID, maps URL.
3. Dedupe by place ID/domain/phone.
4. Crawl each website contact/about/footer pages only.
5. Extract generic emails and business phones.
6. Validate domain, MX, phone format.
7. Human review low-confidence rows.

Output target: **80-120 verified records**.

### Collection block 2: vertical directories (1.5-2 hr manual/browser-assisted)

1. Use Justdial/Sulekha/Practo/clinic/coaching directories for the same city/segment.
2. Capture only public visible listing data and source URL.
3. Do not trigger contact requests or bypass login/CAPTCHA.
4. Cross-check each account on Google/company site before accepting.

Output target: **40-70 verified records**.

### Collection block 3: B2B/manufacturing/export sources (1.5-2 hr)

1. Use IndiaMART/TradeIndia/ExportersIndia/association directories for product categories.
2. Prefer company pages with website and public phone/email.
3. Enrich from company websites.
4. Tag product/category fit and export/manufacturing indicators.

Output target: **40-70 verified records**.

### Collection block 4: LinkedIn/Apollo/startup/SaaS sources (1 hr)

1. Identify 25 high-fit accounts or personas from LinkedIn/company sites/startup directories.
2. Use Apollo only for the 25 highest-fit daily enrichments.
3. Keep Apollo verification status and source IDs.
4. Do not scrape LinkedIn; manual or licensed workflow only.

Output target: **25-40 verified records**.

### End-of-day QA (45-60 min)

1. Run dedupe and suppression join.
2. Reject rows missing source URL or any valid contact channel.
3. Spot-check 10% of each source bucket.
4. Export `ready_for_review` CSV.
5. Log metrics: raw collected, duplicates, invalid email/phone, suppressed, qualified, by source/segment.

## Daily output math

| Stage | Conservative | Normal | Stretch |
|---|---:|---:|---:|
| Raw candidates | 350 | 450 | 600 |
| After source-level cleanup | 300 | 390 | 510 |
| After dedupe | 250 | 325 | 420 |
| After validation/suppression | 200 | 260-300 | 340-400 |

Use the stretch mode only for API-compliant sources and public websites; do not increase manual directory scraping rates.

## Implementation blueprint

### Phase 1: 3-day manual-assisted pilot

1. Create Airtable/Google Sheet/CSV with the schema above.
2. Run 3 segments x 3 cities:
   - Clinics: Pune, Jaipur, Kochi
   - Coaching: Ahmedabad, Indore, Lucknow
   - Manufacturers: Coimbatore, Rajkot, Faridabad
3. Collect 600 raw records total; measure valid rate by source.
4. Build suppression file from existing customers/known opt-outs/invalids.
5. Decide which 5 sources produce the best valid-rate/cost mix.

### Phase 2: Build compliant automation

1. Google Places API collector with keyword-city queue and field masks.
2. Website enrichment crawler with strict crawl limits.
3. Validation module: phone normalization, email syntax/MX, domain checks.
4. Dedupe module using SQLite/Postgres.
5. Review UI/sheet that shows evidence URL and confidence scores.
6. Export job that emits only `ready_for_review`, never sends outreach.

### Phase 3: Source expansion

1. Add chamber/association directory workflows by city/industry.
2. Add B2B marketplace public-page workflows with manual approval gates.
3. Add Apollo enrichment queue capped at 25/day.
4. Add startup/SaaS source queue from Product Hunt/Startup India/Wellfound/Crunchbase where permitted.
5. Add weekly quality review: invalid rate, opt-out complaints, duplicate rate, conversion after compliant outreach if/when separately approved.

## Source-specific notes and caveats

- **Google Places:** reliable for business-level contact discovery. Use official API rather than scraping Maps. Contact fields and details are billable; request only necessary fields.
- **Justdial/Sulekha/Practo:** useful but legally/operationally risky for automation. Treat as manual research sources unless explicit data access is obtained.
- **IndiaMART/TradeIndia:** high-fit for manufacturers. Do not automate contact reveal flows. Prioritize supplier pages that disclose public business details.
- **MSME/Udyam/data.gov.in:** excellent for targeting sectors and districts; usually weak for direct contacts. Do not infer contact records from aggregate data.
- **LinkedIn:** use for role/company qualification, not scraping. Pair with Apollo/company website for a small number of high-fit contacts.
- **Apollo:** reserve daily limit for the best 25 records; do not spend credits on low-fit local businesses where generic business contact is enough.
- **GitHub:** collect organization/company contacts only where public and business-relevant; avoid mass harvesting personal developer emails.

## Quality scoring model

`source_quality_score` out of 5:

- 5 = official company website / association member page / verified Apollo email / Google profile + website match.
- 4 = Google Places with phone/website or credible B2B marketplace supplier page.
- 3 = local directory listing cross-checked by another source.
- 2 = public dataset/company name without direct current contact.
- 1 = unverified third-party scraped/aggregated record; do not export unless enriched.

`fit_score` out of 100:

- Industry/segment fit: 0-25
- Business size/complexity proxy: 0-20
- Automation/AI/cloud need signals: 0-20
- Contactability with public business channel: 0-15
- Source confidence: 0-10
- Geography/market priority: 0-10

Export only rows with `source_quality_score >= 3`, `fit_score >= 55`, and no suppression reason.

## Safe first week operating plan

| Day | Focus | Verified target |
|---|---|---:|
| 1 | Build schema, suppression list, Places pilot for 3 cities | 100-150 |
| 2 | Add website enrichment and email validation | 180-220 |
| 3 | Add Justdial/Sulekha/Practo manual lanes | 220-260 |
| 4 | Add IndiaMART/TradeIndia manufacturing lane | 250-300 |
| 5 | Add Apollo 25/day and association/startup lanes | 250-320 |
| 6 | QA, dedupe tuning, source quality review | 200-250 |
| 7 | Document SOP and lock daily quotas | 250-300 |

## Key references checked

- TRAI TCCCPR page: explains TCCCPR 2018 protects customers from Unsolicited Commercial Communications and supports commercial communication only according to recipient opt-in/preferences.
- Google Places API data fields documentation: confirms Places field masks and availability of fields such as address, business status, website/phone/contact fields across billing tiers.
- data.gov.in / AIKosh Udyam dataset references: useful for MSME targeting and district/sector context, but not a primary direct-contact source.

## Bottom line

A realistic, ethical engine can deliver **200-300 verified business contacts/day** by combining Google Places, public business websites, selective manual directory collection, B2B marketplaces, associations, and capped Apollo enrichment. The engine should optimize for source evidence, dedupe, validation, and compliance rather than maximum raw scraping volume. For India, phone/WhatsApp outreach should remain blocked unless a separate compliant consent/DND/opt-out process is designed and approved.
