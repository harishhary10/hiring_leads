# T2 Hiring Pipeline — Apify "ATS Hiring Signals" Actor Runbook (aka "WB" workflow)

This Actor replaces the manual per-board sweep from the city-portal plan. It scrapes live job boards on Greenhouse, Lever, Ashby, Workable, SmartRecruiters, Workday and Personio directly from each company's public board API — as fresh as the careers page — and returns scored hiring leads without LinkedIn accounts or anti-bot issues [web:24]. Paid-tool budget check before adopting: Apify's free plan includes $5 monthly usage credit, with paid plans at $39/mo (Starter) and $199/mo (Scale); this Actor is pay-per-result (~$1 / 1,000 results on the pricing page) [web:24].

## Button quick-reference (user-facing inputs)

| Actor control | What it does | T2 setting |
|---|---|---|
| `discoverCompanies` + `discoverLimit` | Randomly samples the built-in ~8,800 job-board directory (harvested from Common Crawl) and returns only companies hiring for your keywords [web:24] | On; 500 boards/run |
| `companyNames` | Paste plain company names — the Actor guesses slugs and probes all ATS providers | Use for tracker re-checks of existing accounts |
| `boards` | Direct board URLs or slugs probed across providers | Use for the 6 hub metro groups if needed |
| `keywords` | Match against title, department, location and full description | Title-gate terms (see configs) |
| `keywordsMode` | `any` (broad) or `all` (precise) [web:24] | `any` for discovery; `all` only in "AI Engineer" mode |
| `searchDescriptions` | Search full job descriptions — per Actor docs, this is how tech stacks are detected | On (C2 config / tech-stack evidence) |
| `locationFilter` | Location restriction | `remote` |
| `postedWithinDays` | Only jobs posted in the last N days — actor docs call freshness "the strongest signal" | `30` — this IS the 30-day role gate |
| `rolePresets` | Curated keyword bundles incl. AI/ML | Optional alternative to the manual whitelist; verify it doesn't pull ML Engineer / Data Scientist you exclude |
| `excludeStale` | Drops postings open 45+ days — the Actor flags these as "likely evergreen/ghost jobs — a weaker buying signal" [web:24] | On |
| `checkFunding` | SEC EDGAR Form D check over last 12 months; +15 composite intent [web:24] | On, but READ CAVEAT below |
| `extractTechStack` | Detects ~120 technologies per job (on by default, no extra cost) [web:24] | On |
| `onlyNewJobs` | Delta mode — outputs only postings not seen in previous runs; designed for scheduled daily/weekly pushes into Slack/n8n/email [web:24] | On for all scheduled runs |
| `outputMode` | `companies` / `jobs` / `both` / `flat_leads` (flat row per company for CSV/CRM import) [web:24] | `both` |

## Three run configurations

The config JSON file ships all three. Summary:

- **C1 — Weekly discovery (bare joint terms):** keywords `["AI Engineer","GenAI Engineer","Generative AI Engineer","Generative AI"]`, `keywordsMode: any`, `locationFilter: remote`, `postedWithinDays: 30`, `excludeStale: true`, `discoverCompanies` = greenhouse/lever/ashby/workday/personio, `discoverLimit: 500`, output `both`, 3 results. Purpose: first-pass gate: one whitelisted title or description-side AI/GenAI mention within 30 days.
- **C2 — Strict title + contract probe:** keywords `["AI Engineer","GenAI Engineer","Generative AI Engineer","contract","contractor","W2","C2C"]`, `keywordsMode: any`, `searchDescriptions: true`, same filters. Purpose: catch genuine contract language (terms don't appear in board title fields, per Actor docs: Title, Department, Location, Workplace_Type, Post_url, Workplace_Type etc. are returned, but contract type is not a first-class board field).
- **C3 — Desc-mode stack evidence:** AI title keywords + stack terms (LangChain, RAG, vector DB, Terraform, Kubernetes, Snowflake…) for Fit score evidence via the `tech_stack` field (~120 technologies detected) [web:24].

## Verification protocol (non-negotiable)

The Actor helps you FIND; you still verify TIER, SIZE and EXCLUSIONS before a row ships:

1. Actor row → open `post_url` / `board_url` → confirm posted date ≤30 days and role is live on the board today.
2. Run the tier evidence pass in priority order (revenue → funding → employees → LinkedIn followers) — the Actor's Form D result is only a funding *hint*.
3. Headcount check 50–500 (LinkedIn associated members accepted as-is per standing rule).
4. Exclusion pass: staffing / IT services / consulting / government / nonprofit (the built-in Common Crawl directory explicitly includes agencies — your #1 false-positive class).
5. Only then write the row to the tracker with confidence + composite.

## Caveats (log these)

- **SEC Form D coverage bias:** Form D applies to US private placements — it confirms *a* raise occurred, not stage, amount reliability for tier-assignment, or ARR. Non-US companies and revenue-based borrowers stay dark. Never tier solely on `funding_check: true`. [web:24]
- **Workday boards:** Workday produces no public FE API and frequently requires session handshakes; expect lower extraction yield than Greenhouse/Lever/Ashby boards and spot-check Workday rows manually. [web:24]
- **`compensation` field only on Ashby** (publisher-provided). Salary detection in other ATS records comes from description text (`salary_detected`).
- **Evergreen roles:** `excludeStale` removes 45+ day postings, which the Actor itself treats as a weaker buying signal — 45+ day openings are "likely evergreen/ghost jobs." [web:24]
- **Contract detection is probabilistic** (description-text match) — treat "contract = yes" from C2 as a note, not a proof point; confirm on the posting page.

## Scheduling

- Monday 09:00 IST — C1 run (fresh week intake, `onlyNewJobs: true`) → tracker staging tab.
- Monday 11:00 IST — verification pass per the protocol above; package Batch of 25.
- Thursday — C2 contract-probe run against accounts already in tracker (refresh Employment_Type signal on live rows only).
- Standing: C3 once per account at qualification time, then archive `tech_stack` into the tracker Notes column.
