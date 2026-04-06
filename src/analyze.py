# analyze.py
# Answers core marketing questions from the unified dataset
# Import these functions into other scripts or run directly

import pandas as pd

# ── LOAD DATA ─────────────────────────────────────────────────────────────────

def load_unified(filepath="data/mock/unified.csv"):
    """Load the unified dataset."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df


# ── ANALYSIS FUNCTIONS ────────────────────────────────────────────────────────

def platform_summary(df):
    """Total spend, impressions, clicks, conversions and avg ROAS by platform."""
    summary = df.groupby("platform").agg(
        total_spend=("spend", "sum"),
        total_impressions=("impressions", "sum"),
        total_clicks=("clicks", "sum"),
        total_conversions=("conversions", "sum"),
        total_conversion_value=("conversion_value", "sum"),
        avg_ctr=("ctr", "mean"),
        avg_cpc=("cpc", "mean"),
        avg_cpm=("cpm", "mean"),
        avg_roas=("roas", "mean"),
    ).round(2)

    summary["overall_roas"] = (
        summary["total_conversion_value"] / summary["total_spend"]
    ).round(2)

    return summary.sort_values("total_spend", ascending=False)


def best_worst_campaigns(df, metric="roas", top_n=5):
    """Top and bottom N campaigns by a given metric."""
    campaign_perf = df.groupby(["platform", "campaign_name"]).agg(
        total_spend=("spend", "sum"),
        total_conversions=("conversions", "sum"),
        total_conversion_value=("conversion_value", "sum"),
        avg_roas=("roas", "mean"),
        avg_cpc=("cpc", "mean"),
        avg_cpm=("cpm", "mean"),
    ).round(2).reset_index()

    campaign_perf["overall_roas"] = (
        campaign_perf["total_conversion_value"] / campaign_perf["total_spend"]
    ).round(2)

    top = campaign_perf.nlargest(top_n, metric)
    bottom = campaign_perf.nsmallest(top_n, metric)

    return top, bottom


def weekly_trends(df):
    """Weekly aggregated performance across all platforms."""
    df = df.copy()
    df["week"] = df["date"].dt.to_period("W").astype(str)

    trends = df.groupby(["week", "platform"]).agg(
        spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversions", "sum"),
        conversion_value=("conversion_value", "sum"),
    ).round(2).reset_index()

    trends["roas"] = (
        trends["conversion_value"] / trends["spend"]
    ).round(2)

    return trends


def cost_efficiency(df):
    """Compare CPM and CPC across platforms — how efficient is each?"""
    efficiency = df.groupby("platform").agg(
        avg_cpm=("cpm", "mean"),
        avg_cpc=("cpc", "mean"),
        avg_ctr=("ctr", "mean"),
    ).round(4)

    # Rank platforms — lower CPM/CPC is better
    efficiency["cpm_rank"] = efficiency["avg_cpm"].rank().astype(int)
    efficiency["cpc_rank"] = efficiency["avg_cpc"].rank().astype(int)

    return efficiency.sort_values("avg_cpm")


def conversion_leaders(df, top_n=5):
    """Which campaigns drove the most conversion value?"""
    leaders = df.groupby(["platform", "campaign_name"]).agg(
        total_conversion_value=("conversion_value", "sum"),
        total_conversions=("conversions", "sum"),
        total_spend=("spend", "sum"),
    ).round(2).reset_index()

    leaders["cost_per_conversion"] = (
        leaders["total_spend"] / leaders["total_conversions"]
    ).round(2)

    return leaders.nlargest(top_n, "total_conversion_value")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading unified data...\n")
    df = load_unified()

    print("=" * 60)
    print("1. PLATFORM SUMMARY")
    print("=" * 60)
    print(platform_summary(df).to_string())

    print("\n" + "=" * 60)
    print("2. TOP 5 CAMPAIGNS BY ROAS")
    print("=" * 60)
    top, bottom = best_worst_campaigns(df, metric="overall_roas")
    print(top[["platform", "campaign_name", "total_spend",
               "total_conversions", "overall_roas"]].to_string())

    print("\n" + "=" * 60)
    print("3. BOTTOM 5 CAMPAIGNS BY ROAS")
    print("=" * 60)
    print(bottom[["platform", "campaign_name", "total_spend",
                  "total_conversions", "overall_roas"]].to_string())

    print("\n" + "=" * 60)
    print("4. COST EFFICIENCY BY PLATFORM")
    print("=" * 60)
    print(cost_efficiency(df).to_string())

    print("\n" + "=" * 60)
    print("5. TOP 5 CONVERSION VALUE LEADERS")
    print("=" * 60)
    print(conversion_leaders(df).to_string())