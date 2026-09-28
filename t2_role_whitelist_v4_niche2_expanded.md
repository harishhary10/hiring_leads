# Role Whitelist v4 — Full Niche 2 (AI & Agentic Engineering)

Supersedes the narrow "AI Engineer / GenAI Engineer" list. Applies to Stale Requirement (Playbook 2) and Just Funded (Playbook 4). Niche 2 per TeamXT Outbound Strategy v1.7: "Engineers who build production systems on large language models, plus MLOps. Not data scientists, and not research ML." [file:24]

## Niche 2 — AI & Agentic Engineering (expanded whitelist)

**Core LLM/production titles:**
- AI Engineer
- GenAI Engineer / Gen AI Engineer / Generative AI Engineer
- Applied AI Engineer
- LLM Engineer
- AI Application Engineer
- Agentic AI Engineer / AI Agents Engineer
- AI Platform Engineer
- Machine Learning Engineer — **now included** (v1.7 groups production ML delivery under Niche 2; only *research* ML and *data science* titles are excluded)
- MLOps Engineer — **now included** per explicit doc mention ("plus MLOps")
- AI/ML Engineer
- ML Infrastructure Engineer
- Conversational AI Engineer

**Still explicitly excluded** (doc: "Not data scientists, and not research ML"):
- Data Scientist
- Research Scientist / Research Engineer (ML)
- AI Research Scientist
- Applied Scientist (research-track variants)
- Prompt Engineer (marketing/content-adjacent, not production systems — hold pending team confirmation; flag separately if it appears, don't auto-include or auto-exclude)
- AI Product Manager

## Niche 1 — Data Engineering on Databricks & Snowflake (new bundle, runs in parallel)

- Data Engineer
- Senior Data Engineer
- Analytics Engineer (borderline — include, flag for BDM review since it can skew BI-only)
- Data Platform Engineer
- Lakehouse Engineer
- Databricks Engineer / Snowflake Engineer

Doc note: "Spark, SQL and data modelling are the core skill and the platform is a specialisation on top, so one engineer can often serve both [niches]." [file:24] Practically: a Data Engineer posting mentioning Databricks or Snowflake in the description should be tagged with *both* niche flags.

## Gate logic change by campaign

| Campaign | Recency rule | Titles used |
|---|---|---|
| Just Funded | Posted ≤30 days (fresh signal) | Full Niche 2 + Niche 1, `keywordsMode: any` |
| Stale Requirement | Posted ≥30 days open (unfilled signal — the trigger IS staleness) | Full Niche 2 + Niche 1, single-role match is enough — this campaign is profile-first, one role at a time |
| New Leader | No role-based gate; trigger is a new VP Eng/CTO/Head of Data in last 60 days | Niche 2 + Niche 1 used only to confirm the team is technical, not as the primary trigger |
| Budget Cycle | No specific role required; company-level fit only | N/A — Europe/UK T3A–T4 only |

## Two gates that now filter every candidate role, regardless of title match

- **Gate 2 — Buys direct:** if the posting is agency-sourced, on a vendor portal, or the company is a staffing/IT-services/MSP shop, it does not count as a signal at all (not just excluded from tiering — the doc is explicit that mediated roles "don't count as a signal"). [file:24]
- **Gate 3 — Has a directing team:** requires an identifiable engineering or data manager at the account. No team means the work is project-based and routes to Focaloid, not TeamXT. [file:24]
- **Language check (Europe only):** the job post itself must be in English, or — for trigger campaigns without a specific role — the company's other engineering postings must be in English. A local-language post is a hard stop even if titles match. [file:24]
