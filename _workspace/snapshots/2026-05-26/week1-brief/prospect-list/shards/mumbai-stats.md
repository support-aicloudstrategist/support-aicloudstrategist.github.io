# Mumbai prospect shard stats

- File: `mumbai.csv`
- Total rows: 60
- Dental clinics: 40
- Diagnostic labs: 20
- Status: all rows marked `researched`
- Outreach performed: no
- WhatsApp numbers: left blank unless publicly verified; none added in this shard.
- Owner names: included only where visible in public Practo/Lybrate snippets; otherwise blank.

## Source mix
- Google Maps: 27
- Justdial: 3
- Lybrate: 8
- Official Site: 12
- Practo: 10

## Caveats / follow-up

- Google ratings/review counts were left blank unless a verified Google listing was directly available. Non-Google ratings seen on Practo/Lybrate/Justdial were captured in notes, not in `google_rating`.
- Several lower-priority rows use public Google Maps search URLs as the source URL where place IDs could not be reliably extracted in this environment. Before outreach, enrich those rows with canonical Google place URLs, phone/WhatsApp, owner/manager, and website validation.
- Prioritized entries are Practo/Lybrate/Justdial/official-site rows because they have stronger public listing evidence.
