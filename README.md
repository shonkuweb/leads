# India Private School Lead Intelligence

Continuously updated database of **new private schools in India** (established ~2020+) with **weak or missing digital presence** — no working website, social-only outreach, Gmail contacts, WhatsApp-first admissions.

## Outputs (regenerated each run)


| File                                   | Description                        |
| -------------------------------------- | ---------------------------------- |
| `output/india_school_leads.json`       | API-ready master export            |
| `output/india_school_leads.csv`        | Spreadsheet-friendly core fields   |
| `output/india_school_leads.txt`        | Human-readable lead cards          |
| `output/priority_outreach_list.txt`    | Leads with score ≥ 8               |
| `output/high_conversion_prospects.csv` | High-score subset                  |
| `output/schools_without_websites.csv`  | No / broken / parked / FB-only web |
| `output/schools_weak_branding.csv`     | Gmail, broken site, or no domain   |


Persistent store: `data/master_school_leads.json`

## Quick start

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
```

## Hourly automation (cron)

```bash
0 * * * * cd /path/to/repo && python scripts/run_pipeline.py && git add data output && git commit -m "chore: hourly school lead refresh" && git push
```

## Adding leads

1. Curate verified rows from public search (Instagram, Facebook, JustDial, Sulekha, news).
2. Append JSON objects to `data/seed_batches/batch_NNN.json`.
3. Re-run pipeline — deduplication merges into `data/master_school_leads.json`.

Dedup keys: Indian mobile last-10 digits, Instagram handle, or normalized school name + city.

## Lead score (1–10)

Higher = stronger fit for website / ERP / admission marketing outreach:

- No / broken / parked website
- Gmail or generic email
- WhatsApp-primary contact
- Established 2021+
- Priority states (WB, UP, Bihar, Jharkhand, Odisha, Assam, etc.)
- CBSE / English medium / preschool

## Goal

**1000+** unique verified leads. Expand `data/seed_batches/` each hourly run until the master count reaches target.

## Verify before outreach

All fields are sourced from **public indexed snippets**. Confirm on Instagram, Google Maps, or a phone call before contacting management.