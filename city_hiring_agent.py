"""
City-Wise Hiring Company Research Agent
=========================================
Feed it a list of cities -> for each city, it uses Claude with web-search
tool-calling to research companies (50-500 employees, T2A/T2B tiers) that
are hiring for TeamXT-relevant roles (Niche 1: Databricks/Snowflake data
engineering, Niche 2: AI/agentic engineering), and writes results to CSV.

Requires: pip install anthropic
Set ANTHROPIC_API_KEY as an environment variable before running.
"""

import os
import csv
import json
import time
from datetime import datetime
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-opus-4-1-20250805"  # swap to a cheaper/faster model if you want lower cost per city

# ---------------------------------------------------------------------------
# 1. INPUT: the list of cities to research. Edit this list or load from CSV.
# ---------------------------------------------------------------------------
CITIES = [
    {"city": "Austin", "state": "TX", "country": "US"},
    {"city": "Denver", "state": "CO", "country": "US"},
    {"city": "Raleigh", "state": "NC", "country": "US"},
    # add more cities, or load from us_top200_other_cities_job_portals.csv
]

# ---------------------------------------------------------------------------
# 2. THE RESEARCH BRIEF — encodes every rule from the T2 project + TeamXT v1.7
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a B2B market research analyst finding companies that
are actively hiring, for a technical staff-augmentation sales team (TeamXT by Focaloid).

QUALIFICATION RULES (apply strictly):

1. HEADCOUNT: 50-500 employees. LinkedIn associated-member count is acceptable evidence.

2. TIER (decide using this strict priority order - use the first signal available):
   - T2A "Seed/Early Funded": revenue <$10M OR funding stage Seed to early Series A
     ($2M-$10M raised), 50-100 employees. Tactical fit, fast decisions, limited ceiling.
   - T2B "Growth-Stage Funded": revenue $10M-$50M ARR OR Series B/C funding,
     100-500 employees. Sweet spot: real budget, tech-forward, room to expand.
   Priority order for evidence: (1) revenue if disclosed, (2) funding stage if revenue
   unknown or company is pre-seed through Series A, (3) employee count only if neither
   revenue nor funding is known, (4) LinkedIn follower count as a last-resort directional
   fallback only (mark confidence as Medium if this is the only signal used).

3. HIRING SIGNAL - the company must have a LIVE, VERIFIABLE open role in one of:
   NICHE 1 (Data engineering): Data Engineer, Senior Data Engineer, Data Platform Engineer,
     Databricks Engineer, Snowflake Engineer (bonus if description mentions Databricks/Snowflake)
   NICHE 2 (AI & agentic engineering): AI Engineer, GenAI Engineer, Generative AI Engineer,
     Applied AI Engineer, LLM Engineer, Agentic AI Engineer, AI Platform Engineer,
     Machine Learning Engineer, MLOps Engineer, AI/ML Engineer, Conversational AI Engineer.
   EXCLUDE from role match: Data Scientist, Research Scientist, AI Research Scientist,
     AI Product Manager (these are not production engineering roles).

4. EXCLUSIONS (auto-drop the company entirely, do not include in output):
   Staffing agencies, recruiting agencies, IT services firms, managed service providers,
   system integrators, management consulting firms, outsourcing/BPO companies,
   government/public sector entities, non-profits/NGOs, universities.
   Also exclude if the role posting is on a vendor portal or clearly agency-mediated
   (i.e. the posting company is a staffing intermediary, not the end employer).

5. LOCATION: the company must have a real presence, office, or the role must be based in
   the specific CITY given for this research task (remote-first companies headquartered
   elsewhere do not count unless the city is explicitly named in the posting as a hub).

6. EVIDENCE STANDARD: every claim needs a source. Do not guess or estimate silently.
   If you cannot verify a fact, write "unverified" rather than inventing a number.
   Prefer: company careers page / ATS board (Greenhouse, Lever, Ashby, Workable,
   SmartRecruiters, Workday, Personio) for the role; funding databases, press releases,
   or SEC filings for funding/revenue; LinkedIn company page for headcount.

OUTPUT FORMAT: Return ONLY a JSON array (no prose, no markdown fences) where each
element has exactly these fields:
{
  "company_name": string,
  "website_domain": string,
  "city": string,
  "state": string,
  "industry_vertical": string,
  "role_title": string,
  "role_title_family": "Niche1" or "Niche2",
  "role_source_url": string,
  "role_posted_date_or_recency": string,
  "work_mode": "Remote" | "Hybrid" | "Onsite",
  "employment_type": "Contract" | "Full-time" | "Unknown",
  "evidence_level_used": "Revenue" | "Funding stage" | "Employee count" | "LinkedIn followers",
  "revenue_or_funding_detail": string,
  "funding_source_url": string,
  "employee_count": string,
  "employee_source": string,
  "tier": "T2A" | "T2B",
  "tier_basis_reason": string,
  "confidence_level": "High" | "Medium" | "Low",
  "notes": string
}

If you find zero qualifying companies for a city after genuine research effort,
return an empty JSON array: []
Do not fabricate companies. Only include companies you found real evidence for.
"""

USER_PROMPT_TEMPLATE = """Research companies headquartered in or with a significant
office in {city}, {state}, {country} that meet all the qualification rules above.

Find up to 8 qualifying companies. For each, verify the hiring signal on their actual
careers page or ATS board before including them. Use web search extensively -
check the company's careers page, LinkedIn, recent funding news, and revenue estimates.

Return the JSON array now."""


def research_city(city_obj: dict, max_retries: int = 2) -> list:
    """Runs one Claude agent research pass for a single city, using the
    web_search server tool so Claude can browse for live evidence."""
    city, state, country = city_obj["city"], city_obj.get("state", ""), city_obj.get("country", "US")

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=[{
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": 15
                }],
                messages=[{
                    "role": "user",
                    "content": USER_PROMPT_TEMPLATE.format(city=city, state=state, country=country)
                }]
            )

            # Concatenate all text blocks from the final response
            text_out = "".join(
                block.text for block in response.content if block.type == "text"
            )

            # Extract JSON array robustly (Claude may wrap it in prose despite instructions)
            start = text_out.find("[")
            end = text_out.rfind("]") + 1
            if start == -1 or end == 0:
                print(f"  [WARN] No JSON array found for {city}. Raw output saved to notes.")
                return []
            json_str = text_out[start:end]
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            print(f"  [RETRY {attempt+1}] JSON parse failed for {city}: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"  [RETRY {attempt+1}] API error for {city}: {e}")
            time.sleep(5)

    print(f"  [FAIL] Giving up on {city} after {max_retries+1} attempts.")
    return []


def run_batch(cities: list, output_csv: str = "city_hiring_companies_output.csv"):
    all_rows = []
    fieldnames = [
        "Research_City", "Research_State", "Research_Country",
        "Company_Name", "Website_Domain", "Industry_Vertical",
        "Role_Title", "Role_Title_Family", "Role_Source_URL",
        "Role_Posted_Date_Or_Recency", "Work_Mode", "Employment_Type",
        "Evidence_Level_Used", "Revenue_Or_Funding_Detail", "Funding_Source_URL",
        "Employee_Count", "Employee_Source", "Tier", "Tier_Basis_Reason",
        "Confidence_Level", "Notes", "Batch_Run_Timestamp"
    ]
    run_ts = datetime.now().isoformat(timespec="seconds")

    for city_obj in cities:
        print(f"Researching {city_obj['city']}, {city_obj.get('state','')}...")
        companies = research_city(city_obj)
        print(f"  -> {len(companies)} qualifying companies found")

        for c in companies:
            all_rows.append({
                "Research_City": city_obj["city"],
                "Research_State": city_obj.get("state", ""),
                "Research_Country": city_obj.get("country", "US"),
                "Company_Name": c.get("company_name", ""),
                "Website_Domain": c.get("website_domain", ""),
                "Industry_Vertical": c.get("industry_vertical", ""),
                "Role_Title": c.get("role_title", ""),
                "Role_Title_Family": c.get("role_title_family", ""),
                "Role_Source_URL": c.get("role_source_url", ""),
                "Role_Posted_Date_Or_Recency": c.get("role_posted_date_or_recency", ""),
                "Work_Mode": c.get("work_mode", ""),
                "Employment_Type": c.get("employment_type", ""),
                "Evidence_Level_Used": c.get("evidence_level_used", ""),
                "Revenue_Or_Funding_Detail": c.get("revenue_or_funding_detail", ""),
                "Funding_Source_URL": c.get("funding_source_url", ""),
                "Employee_Count": c.get("employee_count", ""),
                "Employee_Source": c.get("employee_source", ""),
                "Tier": c.get("tier", ""),
                "Tier_Basis_Reason": c.get("tier_basis_reason", ""),
                "Confidence_Level": c.get("confidence_level", ""),
                "Notes": c.get("notes", ""),
                "Batch_Run_Timestamp": run_ts,
            })

        time.sleep(1)  # polite pacing between cities

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nDone. {len(all_rows)} total company rows written to {output_csv}")


def load_cities_from_csv(path: str, limit: int = None) -> list:
    """Load cities from the us_top200_other_cities_job_portals.csv format,
    or any CSV with City/State/Country columns."""
    cities = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cities.append({
                "city": row.get("City", "").strip(),
                "state": row.get("State", "").strip(),
                "country": row.get("Country", "US").strip() or "US",
            })
            if limit and len(cities) >= limit:
                break
    return cities


if __name__ == "__main__":
    # Option A: use the hardcoded CITIES list above
    run_batch(CITIES, output_csv="city_hiring_companies_output.csv")

    # Option B: load cities from your existing CSV instead, e.g.:
    # cities = load_cities_from_csv("us_top200_other_cities_job_portals.csv", limit=10)
    # run_batch(cities, output_csv="city_hiring_companies_output.csv")
