# T2 Hiring-Companies Project — End-to-End Runbook v3 (Consolidated)

Single source of truth. Supersedes earlier fragments: tier SOP, role gate spec, city-portal sweep plan.

## 1. ICP
US product companies (SaaS / fintech / AI infra / healthtech / marketplace / enterprise software), **50–500 employees**, that have posted a remote **AI Engineer / GenAI Engineer** role (whitelist below) in the **last 30 days**, and fit Tier 2A or 2B.

## 2. Tiers

| Tier | Label | Revenue / ARR | Funding | Headcount | Position |
|---|---|---|---|---|---|
| T2A | Seed / Early Funded | < $10M | Seed → early Series A, $2M–$10M | 50–100 | Fast decisions, limited expansion ceiling |
| T2B | Growth-Stage Funded | $10M–$50M | Series B / C | 100–500 | Sweet spot: budget, tech-forward, room to expand |

Tier evidence priority (first available wins): **1. Revenue → 2. Funding stage → 3. Employee count → 4. LinkedIn followers** (followers-only rows capped at Medium confidence and revalidated before outreach).

## 3. Role gate (all 4 must pass)
1. Title in whitelist: AI Engineer / GenAI Engineer / Generative AI Engineer / Gen AI Engineer / Artificial Intelligence Engineer / AI/ML Engineer / AI Application Engineer. NOT ML Engineer, Data Scientist, Research Scientist, MLOps, Prompt Engineer.
2. Posted within last 30 days (ATS/API posting date first; board-indexed date acceptable if logged).
3. Remote.
4. Contract preferred (+10 intent bonus); full-time remote accepted as B-signal.

## 4. Exclusions (auto-drop, log reason)
Staffing, recruiting agency, IT services, managed services, system integrator, management consulting, outsourcing/BPO, government/public sector, non-profit/NGO, university. Keyword hit → 30-sec manual header confirm.

## 5. Pipeline (the "WB" automation spine)
The Apify ATS Hiring Signals actor (`opensignals/ats-hiring-signals`, ~$1/1,000 results on the pricing page [web:24]) replaces manual board sweeps:

1. **C1 config** weekly Monday discovery run against the actor's ~8,800-board Common Crawl directory [web:24], with `postedWithinDays: 30`, `locationFilter: remote`, `excludeStale: true` — the run output already satisfies gate checks 2–3.
2. City-portal CSV stays as **backup** for niche-community coverage (Silicon Florist, Techlahoma, Refresh Miami) if C1 yield is thin.
3. Each surviving company passes: posted-date spot check on ATS → tier evidence pass (priority order §2) → headcount 50–500 (LinkedIn associated members accepted) → exclusion pass → enter tracker.
4. `checkFunding` (SEC Form D last 12 months, +15 composite intent [web:24]) is ON — but treat as a hint only; confirm stage/amount from press/Crunchbase before tier assignment.

## 6. Scoring (0–100 each, composite = 45% Fit + 45% Intent + 10% ConfidencePoints)
- **Fit:** size band in range 30; tier (T2B=30/T2A=20); vertical match 20; tech-forward signals (actor's `tech_stack`/`top_technologies`, ~120 detected technologies [web:24]) 20.
- **Intent:** passing-role count 35; newest role ≤14d +25 / 15–30d +15; 30-day hiring velocity 25; contract language +10; multiple passing roles +10 (cap 100).
- **Confidence:** High = posted date re-verified on board ≤7d + tier signal source-backed. Medium = directional tier signal or verification >7–30d. Points: 100/60/20.
- **Bands:** ≥75 Ready-to-Outreach · 60–74 monitor · <60 drop.

Note: the actor's own `signal_score` (40 volume / 20 focus / 20 freshness / 20 velocity [web:24]) is a *sorting hint* only — it doesn't know your tiers or exclusions. Never copy it into the tracker.

## 7. Ops cadence
- Mon 09:00 C1 run (`onlyNewJobs: true` — delta mode outputs just new postings [web:24]) → staging → verify → Batch of 25 by Mon 14:00.
- Thu C2 contract probe on live roles only.
- Per-new-account: C3 stack extraction once, archived to Notes.
- Ready-to-Outreach rows revalidated every 14 days; funding triggers >90 days re-verified.

## 8. Definition of done (per batch of 25)
Every row: tier + basis reason, evidence level, ≥1 passing role with post URL + date, exclusion PASS, confidence set, composite computed, validation date ≤7 days. Zero followers-only rows at High confidence. Hand-off note with tier split + top 5 composites.
