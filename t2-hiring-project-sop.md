# T2 Hiring-Companies Project — Operating SOP

## 1. Objective
Build and maintain a validated list of companies that are **actively hiring**, headcount **50–500**, in **Tier 2A or 2B** bands, for outbound prospecting. Output = scored, source-linked CSV batches ready for outreach.

## 2. Qualification Gates (hard filters — fail any = drop)

| Gate | Rule | Check |
|---|---|---|
| Headcount | 50–500 employees | LinkedIn company page associated members accepted as-is |
| Hiring | ≥1 live role on careers page or ATS board (Greenhouse, Lever, Ashby, Workable, Workday, Personio, SmartRecruiters) | Role must show posting date or be currently on the board today |
| Sector | Product company (SaaS / fintech / AI / health tech / marketplace / enterprise software) | Must be in allowed vertical list |
| Exclusions (auto-drop) | Staffing, recruiting agency, IT services, managed services, system integrator, management consulting, outsourcing/BPO, government/public sector, non-profit/NGO, university | Keyword flag + 30-second site header check |
| Evidence | At least ONE of: revenue, funding, employee count, LinkedIn followers — plus a live hiring signal with source link | No unsupported claims; no silent estimates |

## 3. Tier Definitions

| Tier | Label | Revenue / ARR | Funding Stage | Headcount | Positioning |
|---|---|---|---|---|---|
| T2A | Seed / Early Funded | < $10M | Seed → early Series A, $2M–$10M raised | 50–100* | Tactical fit — fast decisions, limited expansion ceiling |
| T2B | Growth-Stage Funded | $10M–$50M ARR | Series B / C | 100–500 | Sweet spot — real budget, tech-forward buyers, room to expand |

*Adjusted from 30–100 to 50–100 to match the project's 50-employee hard floor. Revert if you want the 30-employee floor instead.

## 4. Tier Decision Logic (strict priority — use first available)

1. **Revenue** — default for any established operating business. If revenue is known, revenue decides the tier, even if funding data also exists.
2. **Funding stage** — replaces revenue for early-stage companies (pre-seed → Series A) and any time revenue is undisclosed.
3. **Employee count** — last resort, only when neither revenue nor funding is known.
4. **LinkedIn follower count** — directional fallback only. Any company tiered on followers alone is capped at Confidence = Medium and must be revalidated before outreach.

Record the level used in `Evidence_Level_Used` and justify in `Tier_Basis_Reason` exactly as the template samples show.

## 5. Scoring Model (0–100 each)

**Fit Score** — size band in range (30) + tier membership (T2B=30 / T2A=20) + vertical match (20) + geography match (10) + tech-forward signals: eng/data/AI hires, modern stack (10).

**Intent Score** — open role count and ICP-relevant roles (35) + role recency: newest role ≤14 days (25) / ≤45 days (15) / >45 days (5) + hiring velocity last 30 days (25) + funding round ≤120 days (15).

**Confidence Levels**
- High: hiring verified on live ATS/careers page within 7 days AND tier signal source-backed
- Medium: tier signal directional only (e.g., LinkedIn followers) or hires unverified >30 days
- Low/Pending: anything else — hold, do not outreach

**Composite** = round(0.45 × Fit + 0.45 × Intent + 0.10 × ConfidencePoints) where ConfidencePoints: High=100, Medium=60, Low=20.

**Composite bands:** ≥75 Ready-to-Outreach · 60–74 Nurture/Monitor · <60 Drop.

## 6. Source Map (free / low-cost first)

| Task | Primary free sources | Enrichment / paid |
|---|---|---|
| Recently funded Seed→A (T2A pipe) | LeadMagic funded lists (weekly), FundedIQ free directory, VCBacked directory, StartupHub.ai (free + API/MCP), VentureDex | Crunchbase paid, Tracxn |
| Series B/C + $10–50M ARR (T2B pipe) | FundedIQ Series B–C pages, VCBacked B/C, press/funding news, company blog rounds | Clearbit/Clay, ZoomInfo |
| Live hiring verification | Company careers page + ATS boards direct; JobPin (daily ATS refresh); Apify ATS Hiring Signals actor (~8,800 job-board directory) | — |
| Revenue estimate | SEC EDGAR (public), free Revenue Finder tools, press/case-study statements | Growjo-type estimators |
| Employees / followers | LinkedIn company page (associated members accepted without extra verification) | Sales Navigator for >200-band validation |
| Contacts (after tiering) | Hunter free tier, LinkedIn, founder names on funding pages | Apollo/Lusha |

## 7. Weekly Workflow (batched)

1. **Monday sweep (60–90 min):** pull newly funded Seed/A + B/C companies from LeadMagic, FundedIQ, VCBacked (previous 7 days). Export to staging sheet.
2. **Exclusion pass:** apply keyword filter + manual header check; drop staffing/IT services/consulting/government/non-profit. Log `Exclusion_Reason`.
3. **Evidence pass per company (2–4 min):** follow priority order — find revenue → if none, funding → if none, LinkedIn employees → followers. Capture amount, date, source link.
4. **Hiring check:** open careers page / ATS board. Log live role count, target-role count, oldest role age, 30-day velocity.
5. **Tier + score:** assign T2A/T2B per §4; compute Fit/Intent/Composite; set Confidence.
6. **Batch packaging:** validated rows move to master tracker in batches of 25, tagged `Batch_ID`. Only High + Medium rows ship; Pending-Revalidation parks separately.
7. **Revalidation cadence:** Ready-to-Outreach rows re-checked every 14 days; funding-trigger rows >90 days old re-verified before any outreach.

## 8. Exclusion Keyword List
`staffing`, `recruit`, `talent agency`, `IT services`, `managed service`, `system integrat`, `consulting`, `outsourc`, `BPO`, `offshor*, government`, `gov.`, `public sector`, `non-profit`, `nonprofit`, `NGO`, `foundation`, `university`, `hospital system` (public). Any keyword hit → 30-sec manual confirm before drop; log reason either way.

## 9. Definition of Done (per batch)
- 25 rows, every row has: tier + tier-basis reason, evidence level used, live ≥1 role with source link, exclusion check = PASS, confidence set, composite computed, validated date ≤7 days.
- Zero rows tiered on LinkedIn followers alone ship as High confidence.
- Hand-off summary: tier split, confidence split, top 5 composite accounts, accounts dropped (with reasons).
