# AICloudStrategist analytics dashboard

## Stack (no new paid services)

- **Collector:** `POST /api/events` → Cloudflare KV (`LEAD_LOG`), non-PII allowlist
- **Reports:** `GET /api/metrics` with `Authorization: Bearer $AICS_REPORT_TOKEN`
- **Leads:** voluntary records from `POST /api/contact` (`contact-*` keys in `CONTACT_LOG` or `LEAD_LOG`)
- **UI:** `/analytics/` (private, `noindex`) — static HTML + polling JS + Chart.js (CDN)
- **Optional:** Cloudflare Web Analytics (Pages dashboard) for extra privacy-preserving aggregates
- **Also on site:** GA4 tag already embedded separately; the private dashboard reads first-party KV metrics

## File map

| Path | Role |
| --- | --- |
| `analytics/index.html` | Dashboard UI + Chart.js canvases |
| `css/aics-analytics-dashboard.css` | Dashboard styles |
| `js/aics-analytics-dashboard.js` | Token auth, ranges, Chart.js, 15s live poll |
| `js/aics-analytics-shim.js` | Page views, CTA/download clicks, scroll, dwell, presence pings |
| `js/aics-email-capture.js` | Engagement-triggered opt-in (≈50s / 60% scroll); optional name |
| `functions/api/events.ts` | Event allowlist + sensitive-prop blocklist + CF country / UA browser enrichment |
| `functions/api/metrics.ts` | Dashboard aggregates + realtime + leads |
| `functions/_middleware.ts` | Serves `/analytics` as private noindex HTML |

## Charts

Interactive Chart.js visuals (hover tooltips, clickable legends, responsive):

- Overview growth (line)
- Traffic sources / providers (doughnut + bar)
- Content dwell vs views (horizontal bar)
- Engagement event counts (bar)
- Live pages / sources / locations (bar + doughnut)

## Performance notes

- Event keys are day-prefixed (`event:YYYY-MM-DD:…`). Metrics lists **only days in range**, not the entire KV namespace.
- Historical `presence_ping` bodies are skipped using list metadata.
- KV values are fetched in **batched** `Promise.all` chunks.
- Dashboard fetch has a **25s timeout**; Chart.js load is non-blocking with an 8s timeout.
- After the first full load, live panels poll `mode=realtime` (lightweight) every 15s.

## Real-time

- `presence_ping` heartbeats every **30s** while the tab is visible
- Active window ≈ **2 minutes**; entering window ≈ **5 minutes**
- Real-time panels are **aggregated only** (counts by page / source / country)

## Privacy — hard rule (no sensitive personal information)

**Do not collect or store sensitive personal information** in the analytics pipeline or dashboard beyond what is already defined:

Allowed:

- Aggregated / non-PII event analytics (paths, devices, browsers, country/region, UTM, anonymous session/visitor ids, engagement counters)
- Voluntary lead **name** and **email** (and related fit-review fields) only when submitted through consented forms (`/api/contact`)

Never collect via analytics events (enforced by allowlist + sensitive key blocklist):

- Passwords or secrets
- Payment / card data
- Health information
- Government ID numbers
- Precise geolocation (lat/lng) — country/region only
- Autofill scraping or any covert identity

Passive browsing **cannot** produce emails. Contacts appear only from email capture or fit review.

## Leads / emails

1. Email capture popup (after meaningful engagement)
2. Fit-review form (`/request-fit-review/`)

## Local use

1. Open `/analytics/` on production (or a Pages preview with KV + token bound)
2. Paste `AICS_REPORT_TOKEN`
3. Choose daily / weekly / monthly / custom range
