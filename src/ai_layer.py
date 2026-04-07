# ai_layer.py
# Connects to Claude API to interpret marketing data in plain English
# Takes analysis output and returns human-readable summaries

import os
import json
import anthropic
from dotenv import load_dotenv

from analyze import (
    load_unified,
    platform_summary,
    best_worst_campaigns,
    weekly_trends,
    cost_efficiency,
    conversion_leaders,
)

# ── SETUP ─────────────────────────────────────────────────────────────────────

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-20250514"

# ── HELPERS ───────────────────────────────────────────────────────────────────

def df_to_text(df, max_rows=20):
    """Convert a DataFrame to a clean text table for the prompt."""
    return df.head(max_rows).to_string()

# ── CONFIG ────────────────────────────────────────────────────────────────────

# Set to True when you have API credits and are ready to use real AI
USE_REAL_API = False

# Cost limits — will be enforced when USE_REAL_API = True
MAX_TOKENS_PER_CALL = 1000      # max tokens per single API call
MAX_CALLS_PER_RUN   = 4         # max API calls per script run
DAILY_SPEND_LIMIT   = 0.10      # USD — max to spend per day

# Token cost estimates for claude-sonnet (USD per token)
COST_PER_INPUT_TOKEN  = 0.000003
COST_PER_OUTPUT_TOKEN = 0.000015

# ── USAGE TRACKER ─────────────────────────────────────────────────────────────

usage = {
    "calls":          0,
    "input_tokens":   0,
    "output_tokens":  0,
    "estimated_cost": 0.0,
}


def ask_claude(system_prompt, user_prompt, max_tokens=MAX_TOKENS_PER_CALL):
    """Send a prompt to Claude and return the response text.
    Falls back to mock response if USE_REAL_API is False.
    Enforces call limits and cost limits when real API is enabled.
    """

    # ── MOCK MODE ─────────────────────────────────────────────────────────────
    if not USE_REAL_API:
        return (
            "[MOCK RESPONSE — API credits not yet added]\n\n"
            "KEY FINDINGS:\n"
            "• Meta leads in ROAS and conversion efficiency\n"
            "• DV360 has highest spend but lowest ROAS of top 3\n"
            "• X Ads best suited for brand awareness, not conversions\n"
            "• Google Search shows attribution gap vs actual value\n\n"
            "Set USE_REAL_API = True in ai_layer.py to enable real analysis."
        )

    # ── LIMIT CHECKS ──────────────────────────────────────────────────────────
    if usage["calls"] >= MAX_CALLS_PER_RUN:
        return f"[LIMIT REACHED] Max {MAX_CALLS_PER_RUN} API calls per run."

    if usage["estimated_cost"] >= DAILY_SPEND_LIMIT:
        return f"[LIMIT REACHED] Daily spend limit of ${DAILY_SPEND_LIMIT} reached."

    # ── REAL API CALL ─────────────────────────────────────────────────────────
    message = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    # Track usage
    input_tokens  = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    call_cost     = (
        input_tokens  * COST_PER_INPUT_TOKEN +
        output_tokens * COST_PER_OUTPUT_TOKEN
    )

    usage["calls"]          += 1
    usage["input_tokens"]   += input_tokens
    usage["output_tokens"]  += output_tokens
    usage["estimated_cost"] += call_cost

    print(f"  [API] Call {usage['calls']}/{MAX_CALLS_PER_RUN} | "
          f"Tokens: {input_tokens}in/{output_tokens}out | "
          f"Cost: ${call_cost:.4f} | "
          f"Total: ${usage['estimated_cost']:.4f}")

    return message.content[0].text


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a senior digital marketing analyst with deep expertise in 
paid media across Meta, Google Ads, DV360, and X Ads.

You are analyzing marketing performance data for a fintech company 
operating in Japan. Your job is to interpret the data and provide 
clear, actionable insights.

Always structure your responses as:
1. KEY FINDINGS (3-5 bullet points, most important insights first)
2. WHAT'S WORKING (what to keep or scale)
3. WHAT NEEDS ATTENTION (what to fix or pause)
4. RECOMMENDED ACTIONS (2-3 concrete next steps)

Be direct. Use plain English. Avoid jargon where possible.
Numbers should always have context — don't just repeat the data, 
interpret it.
"""

# ── AI ANALYSIS FUNCTIONS ─────────────────────────────────────────────────────

def ai_platform_summary(df):
    """Ask Claude to interpret platform-level performance."""
    summary = platform_summary(df)

    prompt = f"""
Here is Q1 2026 marketing performance data across 4 platforms for a fintech company:

{df_to_text(summary)}

Metrics explanation:
- total_spend: total USD spent
- total_conversions: total conversion events
- overall_roas: return on ad spend (conversion value / spend)
- avg_cpm: average cost per 1000 impressions
- avg_cpc: average cost per click

Please analyze this cross-platform performance and provide your assessment.
"""
    return ask_claude(SYSTEM_PROMPT, prompt)


def ai_campaign_analysis(df):
    """Ask Claude to interpret best and worst performing campaigns."""
    top, bottom = best_worst_campaigns(df, metric="overall_roas")

    prompt = f"""
Here are the TOP 5 campaigns by ROAS for a fintech company in Q1 2026:

{df_to_text(top[["platform", "campaign_name", "total_spend", "total_conversions", "overall_roas"]])}

And the BOTTOM 5 campaigns by ROAS:

{df_to_text(bottom[["platform", "campaign_name", "total_spend", "total_conversions", "overall_roas"]])}

Please analyze what these campaigns tell us about performance and 
what actions should be taken.
"""
    return ask_claude(SYSTEM_PROMPT, prompt)


def ai_weekly_trends(df):
    """Ask Claude to identify trends in weekly performance."""
    trends = weekly_trends(df)

    # Pivot for cleaner reading
    spend_pivot = trends.pivot(
        index="week", columns="platform", values="spend"
    ).round(2)

    roas_pivot = trends.pivot(
        index="week", columns="platform", values="roas"
    ).round(2)

    prompt = f"""
Here is weekly spend data by platform for Q1 2026:

{df_to_text(spend_pivot)}

And weekly ROAS by platform:

{df_to_text(roas_pivot)}

Please identify any notable trends, spikes, or patterns and explain 
what they might mean for a fintech advertiser.
"""
    return ask_claude(SYSTEM_PROMPT, prompt)


def ai_recommendations(df):
    """Ask Claude for overall budget reallocation recommendations."""
    summary = platform_summary(df)
    top, bottom = best_worst_campaigns(df, metric="overall_roas")
    leaders = conversion_leaders(df)

    prompt = f"""
You are reviewing Q1 2026 paid media performance for a fintech company.

PLATFORM SUMMARY:
{df_to_text(summary[["total_spend", "total_conversions", "overall_roas", "avg_cpc", "avg_cpm"]])}

TOP CAMPAIGNS BY CONVERSION VALUE:
{df_to_text(leaders[["platform", "campaign_name", "total_conversion_value", "cost_per_conversion"]])}

LOWEST ROAS CAMPAIGNS:
{df_to_text(bottom[["platform", "campaign_name", "total_spend", "overall_roas"]])}

Based on this data, what specific budget reallocation would you recommend 
for Q2 2026? Be specific about which platforms and campaigns to scale, 
maintain, or cut.
"""
    return ask_claude(SYSTEM_PROMPT, prompt, max_tokens=1500)


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading data...\n")
    df = load_unified()

    print("=" * 60)
    print("AI ANALYSIS: PLATFORM PERFORMANCE")
    print("=" * 60)
    print(ai_platform_summary(df))

    print("\n" + "=" * 60)
    print("AI ANALYSIS: CAMPAIGN WINNERS & LOSERS")
    print("=" * 60)
    print(ai_campaign_analysis(df))

    print("\n" + "=" * 60)
    print("AI ANALYSIS: WEEKLY TRENDS")
    print("=" * 60)
    print(ai_weekly_trends(df))

    print("\n" + "=" * 60)
    print("AI ANALYSIS: Q2 RECOMMENDATIONS")
    print("=" * 60)
    print(ai_recommendations(df))

    # Print usage summary if real API was used
    if USE_REAL_API:
        print("\n" + "=" * 60)
        print("API USAGE SUMMARY")
        print("=" * 60)
        print(f"  Total calls:     {usage['calls']}")
        print(f"  Input tokens:    {usage['input_tokens']}")
        print(f"  Output tokens:   {usage['output_tokens']}")
        print(f"  Estimated cost:  ${usage['estimated_cost']:.4f}")