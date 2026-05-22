# India Private School Lead Intelligence

Autonomous pipeline to discover **new private schools in India** (established ~2020+) with **weak or missing digital presence** — no working website, social-only presence, JustDial/Sulekha listings, Gmail/Yahoo contacts, and active admissions signals.

## Outputs (updated each cron run)

| File | Description |
|------|-------------|
| `data/master_school_leads.json` | Master deduplicated database |
| `output/india_school_leads.json` | API-ready export |
| `output/india_school_leads.csv` | CRM import |
| `output/india_school_leads.txt` | Human-readable lead cards |
| `output/schools_without_websites.txt` | No-website segment |
| `output/high_conversion_prospects.txt` | Lead score ≥ 8 |
| `output/priority_outreach_list.txt` | High-priority states |

## Run locally

```bash
pip install requests
chmod +x run_hourly.sh
./run_hourly.sh
```

Or:

```bash
python3 scripts/build_india_school_leads.py
```

## Automation

- Cron schedule: hourly (`0 * * * *`)
- Search query rotation: `config/search_queries.json` + `data/discovery_state.json`
- Deduplication: school name + city + phone (last 10 digits)
- Website checks: HTTP probe with status classification (`scripts/website_checker.py`)

## Lead scoring (1–10)

Higher scores favor: no/broken website, recent establishment, CBSE/English medium, priority states, Gmail contact, WhatsApp/phone CTAs, active social/directory listings.

## Verification

All fields are sourced from **public search snippets**. Verify on Instagram, Google Maps, or a phone call before outreach. Excluded by policy: government schools, KV, army schools, colleges, coaching centers, and entries marked `exclude` in the builder.

## Target

Grow `master_school_leads.json` toward **1000+ unique verified leads** with management contacts and weak web presence.
