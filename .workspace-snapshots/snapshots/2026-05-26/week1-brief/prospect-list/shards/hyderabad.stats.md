# Hyderabad Prospect Shard Stats

- CSV: `reports/week1-brief/prospect-list/shards/hyderabad.csv`
- Total rows: 60
- Dental clinics: 40
- Diagnostic labs: 20
- City/metro: Hyderabad
- Status: all rows marked `researched`

## Source mix

- Practo: 40 dental clinic rows, deduped by clinic name + locality from Hyderabad dentist listing pages.
- Google Maps: 20 diagnostic lab rows using public Google Maps search/listing URLs for named Hyderabad labs/chains.

## Field notes

- Required fields populated for every row: `business_name`, `city`, `metro`, `source_url`, `source_platform`, `status`.
- `whatsapp_number` left blank where a public WhatsApp number was not directly verifiable.
- `google_rating` and `google_reviews_count` left blank because ratings were not reliably extracted from the public pages used.
- Dental notes include locality, Practo recommendation %, review/story count, and listed dentist experience where available.

## QA

- CSV schema matches requested columns.
- Count check passed: 40 dental + 20 diagnostic = 60.
- No outreach performed.
