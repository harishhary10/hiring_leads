# Role Gate Spec v2 — AI Engineer / GenAI Engineer (Remote-Contract, ≤30 Days)

This replaces the generic "≥1 live role" hiring gate in the T2 SOP. A company now qualifies ONLY if it passes every check below.

## The gate (all 4 must pass — fail any = drop from batch)

| # | Check | Pass condition |
|---|---|---|
| 1 | Title match | Job title is in the approved whitelist below (exact or listed variant only) |
| 2 | Recency | Posting date is within the last 30 days (ATS-posted date, or job-board indexed date if ATS shows none — log which was used) |
| 3 | Work mode | Role is Remote (fully remote, remote-US, remote-friendly with stated overlap zones) |
| 4 | Employment type | Role is Contract / Contract-to-hire — OR — Full-time is acceptable as a "B-signal" when contract isn't offered (log Employment_Type; contract roles rank higher) |

If only Full-time onsite roles exist → FAIL. If the only matching role is >30 days old → FAIL and park for next weekly sweep (roles refresh often; a stale AI Engineer post is a re-check candidate, not a dead account).

## Approved title whitelist

**Family "GenAI":**
- GenAI Engineer
- Generative AI Engineer
- Gen AI Engineer

**Family "AI":**
- AI Engineer
- Artificial Intelligence Engineer
- AI/ML Engineer (accept — counts under AI family)
- AI Application Engineer (accept)

**Explicitly NOT accepted:** Machine Learning Engineer, Data Scientist, Research Scientist, MLOps Engineer, Prompt Engineer, AI Product Manager, Forward Deployed Engineer. (Tight on purpose — if you want ML Engineer included later, add it as Family "ML" rather than widening AI.)

## Scoring impact (replaces Intent recency row in SOP)

- Newest passing role posted ≤14 days: +25 intent points
- 15–30 days: +15
- Contract / contract-to-hire type: +10 bonus (your staff-aug wedge)
- Multiple passing roles (2+): +10
- Oldest matching role >30 days: gate FAIL, composite not computed, Validation_Status = Dropped or Pending-Re-Sweep

## Tracker changes

New columns in tracker v2: `Role_Title`, `Role_Title_Family`, `Role_Posted_Date`, `Posted_Within_30d` (YES/NO), `Work_Mode` (Remote/Hybrid/Onsite), `Employment_Type` (Contract/Contract-to-hire/Full-time), `Role_Gate_Status` (PASS / FAIL - {reason}), `Role_Source_Link`, `Roles_Passing_Gate_Count`, `Open_Roles_Total`. Sample rows show one PASS and one FAIL path so the filter behavior is unambiguous.

## Where to run the sweep

- Direct ATS boards (Greenhouse/Lever/Ashby) via company careers pages — posting dates are first-party here
- JobPin and Apify ATS Hiring Signals: filter keywords `AI engineer`, `GenAI engineer`, `Generative AI engineer`, role type remote/contract, posted ≤30 days
- LinkedIn Jobs as triangulation only (duplicates inflate counts — dedupe on Role_Title + company before logging Roles_Passing_Gate_Count)

## Batch note

Expect the gate to cut raw funded-startup intake by roughly 60–75%. That is the point: every surdiving row is a contract-fit AI/GenAI hiring signal ≤30 days old, which is the exact wedge for a staff-augmentation pitch.
