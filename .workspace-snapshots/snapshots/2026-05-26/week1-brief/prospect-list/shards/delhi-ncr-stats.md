# Delhi NCR Prospect Shard Stats

- File: `/home/OpenClaw/.openclaw/workspace/reports/week1-brief/prospect-list/shards/delhi-ncr.csv`
- Total rows: 60
- Dental clinics: 40
- Diagnostic labs: 20
- Metro: Delhi NCR
- Cities/localities covered: Delhi, Noida, Gurugram/Gurgaon, Ghaziabad, Faridabad and NCR localities

## Source mix
- Practo: 40
- Official site: 20

## Data quality notes
- Dental rows were extracted from public Practo dentist listing structured data and de-duplicated by `practice_id`.
- Diagnostic lab rows use public official websites as listing sources; no outreach was performed.
- `whatsapp_number` is blank where a WhatsApp number was not directly verified from the public listing.
- Google ratings/review counts are blank because this shard did not access Google Maps result data directly.
- Status is `researched` for every row as requested.
