# City-Wise Hiring Research Agent — Setup Guide

This is a real, runnable Claude agent: you give it a list of cities, and for each one it uses Claude with live web search to find qualifying companies, applying every rule from the T2 project and TeamXT v1.7 (tiers, Niche 1/2 roles, exclusions, evidence priority). It writes one consolidated CSV.

## 1. What it actually does

For each city in your input list, the script sends Claude a system prompt encoding all your qualification rules, gives it a `web_search` tool, and lets it browse: company careers pages, LinkedIn, funding news, revenue estimates. Claude returns strict JSON per company (name, role, tier, evidence, sources), and the script appends every city's results into one CSV — no manual copy-paste between city runs.

This replaces the "Apify actor" idea entirely — it's Claude doing the researching and reasoning itself, city by city, instead of an ATS-board scraper.

## 2. One-time setup

1. Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com) (separate from your Claude.ai subscription — this is pay-per-token API access).
2. Install the SDK: `pip install anthropic`
3. Set the key as an environment variable before running:
   - Mac/Linux: `export ANTHROPIC_API_KEY=sk-ant-...`
   - Windows (PowerShell): `$env:ANTHROPIC_API_KEY="sk-ant-..."`
4. Save `city_hiring_agent.py` locally.

## 3. Running it

**Quick test (hardcoded cities):** edit the `CITIES` list at the top of the file — it ships with Austin, Denver, Raleigh as examples — then run:
```
python city_hiring_agent.py
```

**Feed it your existing city list:** the script has `load_cities_from_csv()` built to read directly from your `us_top200_other_cities_job_portals.csv` (or any CSV with City/State/Country columns). Uncomment the two lines at the bottom of the file:
```python
cities = load_cities_from_csv("us_top200_other_cities_job_portals.csv", limit=10)
run_batch(cities, output_csv="city_hiring_companies_output.csv")
```
Start with `limit=10` to control API cost before scaling to all 190 cities.

## 4. What comes out

One CSV, `city_hiring_companies_output.csv`, with every qualifying company across all researched cities: company name, domain, role title, role source URL, tier, tier-basis reasoning, evidence level used, employee count + source, funding/revenue detail + source, confidence level, and notes. This slots directly into the T2 master tracker template (v3) columns you already have — same field logic, same tier priority order.

## 5. Cost and scale notes

- Each city run is one Claude API call with up to 15 web searches; cost scales with number of cities and search depth. Running all 190 cities in one go will use meaningful API credit — test on 5–10 cities first to gauge typical spend before scaling.
- `MODEL` is set to Claude Opus for research depth; swap to a faster/cheaper Claude model in the script if you want lower per-city cost at some quality tradeoff.
- The script retries twice per city on JSON parse failures or API errors, then logs a failure and moves on — it won't hang on one bad city.
- `time.sleep(1)` between cities is a polite pacing buffer; remove it if you want faster throughput and your API tier supports it.

## 6. Where this fits your GitHub setup

Since GitHub is connected, you can version this script as a repo (e.g. `teamxt-city-hiring-agent`) — commit the script, keep `city_hiring_companies_output.csv` runs as dated files, and track prompt-rule changes (like the Niche 2 whitelist expansion) as commits so you have a history of exactly which rule version produced which batch. Say the word and I can create the repo and push this file directly.

## 7. Known limitations to watch

- Claude's web search quality varies by how well-indexed a company's careers page is — very small or brand-new startups may return "unverified" fields more often. That's intentional (the prompt forbids guessing), not a bug.
- The agent cannot check ATS boards behind login walls or heavily JS-rendered career pages the way a dedicated scraper can — for those, cross-check manually or pair this with a direct careers-page fetch.
- Exclusions (staffing/consulting/government) rely on Claude's judgment from search results, not a fixed keyword list — spot-check a sample batch before trusting it fully, same as any new sourcing method.
