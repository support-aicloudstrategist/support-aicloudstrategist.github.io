# AICloudStrategist analytics dashboard

## Stack (no new paid services)

- **Collector:** `POST /api/events` → Cloudflare KV (`LEAD_LOG`), non-PII allowlist
- **Reports:** `GET /api/metrics` with `Authorization: Bearer $AICS_REPORT_TOKEN`
- **Leads:** voluntary records from `POST /api/contact` (`contact-*` keys in `CONTACT_LOG` or `LEAD_LOG`)
- **UI:** `/analytics/` (private, `noindex`) — static HTML + polling JS
- **Optional:** Cloudflare Web Analytics (Pages dashboard) for extra privacy-preserving aggregates

## File map

| Path | Role |
| --- | --- |
| `analytics/index.html` | Dashboard UI |
| `css/aics-analytics-dashboard.css` | Dashboard styles |
| `js/aics-analytics-dashboard.js` | Token auth, range controls, 15s live poll |
| `js/aics-analytics-shim.js` | Page views, CTA/download clicks, scroll, dwell, presence pings |
| `js/aics-email-capture.js` | Engagement-triggered opt-in (≈50s / 60% scroll); optional name |
| `functions/api/events.ts` | Event allowlist + CF country / UA browser enrichment |
| `functions/api/metrics.ts` | Dashboard aggregates + realtime + leads |
| `functions/_middleware.ts` | Serves `/analytics` as private noindex HTML |

## Real-time

- `presence_ping` heartbeats every 15s while the tab is visible
- Active window ≈ **2 minutes**; entering window ≈ **5 minutes**
- Dashboard polls `/api/metrics` every **15 seconds** (no full page reload)
- Real-time panels are **aggregated only** (counts by page / source / country)

## Leads / emails — hard constraint

Browsers cannot expose visitor emails without the person typing them (or equivalent voluntary input).  
**Do not** attempt autofill scraping, fingerprinting, or covert identity.

Contacts in the dashboard come only from:

1. Email capture popup (after meaningful engagement)
2. Fit-review form (`/request-fit-review/`)

## Local use

1. Open `/analytics/` on production (or a Pages preview with KV + token bound)
2. Paste `AICS_REPORT_TOKEN`
3. Choose daily / weekly / monthly / custom range
