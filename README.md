# India Private School Lead Intelligence

Autonomous pipeline to discover **private schools in India** with **no working website** but **active social media / directory marketing**.

## Outputs (updated each cron run)

| File | Description |
|------|-------------|
| `data/master_school_leads.json` | Master deduplicated database (includes rejected for audit) |
| `output/india_school_leads.json` | Qualified leads only (no active website) |
| `output/india_school_leads.csv` | CRM import — qualified only |
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
python3 scripts/run_discovery_cycle.py
```

## Discovery

- **Browser MCP**: Instagram / JustDial profile verification (see `data/seed_batches/batch_browser_*.json`)
- Search query rotation: `config/search_queries.json` + `data/discovery_state.json`
- Seed batches: `data/seed_batches/batch_*.json` merged each run
- Deduplication: school name + city + phone (last 10 digits)
- Website checks: HTTP probe (`scripts/website_checker.py`)
- **Strict reject**: `website_status == active` never exported

## Lead scoring (1–10)

Higher scores favor: no/broken website, recent establishment, CBSE/English medium, priority states, Gmail contact, WhatsApp/phone CTAs, active social/directory listings.

## Verification

All fields are sourced from **public profiles** (browser MCP + search). Verify on Instagram, Google Maps, or phone before outreach.

## Target

Grow qualified export toward **10,000+ unique verified leads** with no working website and social/directory admissions marketing.
