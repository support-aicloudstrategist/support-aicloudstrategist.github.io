# Bengaluru verified prospect list evidence

Output CSV: `/home/OpenClaw/.openclaw/workspace/reports/week1-brief/prospect-list/aics-prospects-bengaluru-verified.csv`

Verification timestamp: 2026-05-24T17:20:00+05:30

## Method

- Preserved the existing 300-row draft and wrote a new verified CSV only.
- Excluded any Google Maps `/search/` URLs.
- Used actual business websites / branch pages as `source_url`.
- Required a visible WhatsApp deep link (`wa.me` or `api.whatsapp.com/send?phone=`) on the fetched website/page before including a row.
- Left `owner_name` blank unless publicly verified; no owner names were safely verified from the fetched source pages.

## Verified WhatsApp evidence

- Apollo Dental branch pages under `https://apollodental.in/bengaluru/.../our-clinics/...` expose WhatsApp link: `https://wa.me/917066028645`.
- Aarthi Scans Bengaluru branch pages under `https://aarthiscan.com/branches/bengaluru/.../` expose WhatsApp link: `https://api.whatsapp.com/send?phone=7550075500`.
- Prima Diagnostics website/Whitefield page exposes WhatsApp link: `https://wa.me/919844882200`.
- Apollo Diagnostics site / Bangalore centre page exposes WhatsApp link: `https://api.whatsapp.com/send/?phone=918978689444`.
- Orange Health Labs website exposes WhatsApp link: `https://wa.me/919008111144`.
- Metropolis Healthcare website exposes WhatsApp link: `https://wa.me/918422801801`.
- Medall website exposes WhatsApp link: `https://wa.me/917550177777`.

## Caveat

The strict WhatsApp requirement sharply reduced owner-led/small clinic yield from public fetchable sources. The resulting list is verified for real Bengaluru dental/diagnostic prospects and public WhatsApp URLs, but includes several chain branches marked with risk notes/lower fit scores rather than fabricating small-business contacts.
