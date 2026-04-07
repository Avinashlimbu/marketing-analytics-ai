# visualize.py
# Turns analysis output into charts
# Uses Plotly for interactive HTML charts

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

from analyze import load_unified, platform_summary, best_worst_campaigns, weekly_trends, cost_efficiency, conversion_leaders

# ── CONFIG ────────────────────────────────────────────────────────────────────

OUTPUT_DIR = "data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PLATFORM_COLORS = {
    "meta":       "#1877F2",
    "google_ads": "#34A853",
    "dv360":      "#FF6D00",
    "x_ads":      "#000000",
}

# ── CHARTS ────────────────────────────────────────────────────────────────────

def chart_platform_spend(df):
    """Bar chart — total spend by platform."""
    summary = platform_summary(df).reset_index()

    fig = px.bar(
        summary,
        x="platform",
        y="total_spend",
        color="platform",
        color_discrete_map=PLATFORM_COLORS,
        title="Total Spend by Platform (Q1 2026)",
        labels={"total_spend": "Total Spend (USD)", "platform": "Platform"},
        text="total_spend",
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(showlegend=False, plot_bgcolor="white")
    fig.write_html(f"{OUTPUT_DIR}/spend_by_platform.html")
    print(f"  ✅ Saved: spend_by_platform.html")
    return fig


def chart_roas_comparison(df):
    """Bar chart — overall ROAS by platform."""
    summary = platform_summary(df).reset_index()

    fig = px.bar(
        summary,
        x="platform",
        y="overall_roas",
        color="platform",
        color_discrete_map=PLATFORM_COLORS,
        title="Overall ROAS by Platform (Q1 2026)",
        labels={"overall_roas": "ROAS", "platform": "Platform"},
        text="overall_roas",
    )
    fig.update_traces(texttemplate="%{text:.2f}x", textposition="outside")
    fig.update_layout(showlegend=False, plot_bgcolor="white")
    fig.write_html(f"{OUTPUT_DIR}/roas_by_platform.html")
    print(f"  ✅ Saved: roas_by_platform.html")
    return fig


def chart_weekly_spend(df):
    """Line chart — weekly spend trends per platform."""
    trends = weekly_trends(df)

    fig = px.line(
        trends,
        x="week",
        y="spend",
        color="platform",
        color_discrete_map=PLATFORM_COLORS,
        title="Weekly Spend by Platform (Q1 2026)",
        labels={"spend": "Spend (USD)", "week": "Week", "platform": "Platform"},
        markers=True,
    )
    fig.update_layout(plot_bgcolor="white", xaxis_tickangle=-45)
    fig.write_html(f"{OUTPUT_DIR}/weekly_spend.html")
    print(f"  ✅ Saved: weekly_spend.html")
    return fig


def chart_weekly_roas(df):
    """Line chart — weekly ROAS trends per platform."""
    trends = weekly_trends(df)

    fig = px.line(
        trends,
        x="week",
        y="roas",
        color="platform",
        color_discrete_map=PLATFORM_COLORS,
        title="Weekly ROAS by Platform (Q1 2026)",
        labels={"roas": "ROAS", "week": "Week", "platform": "Platform"},
        markers=True,
    )
    fig.update_layout(plot_bgcolor="white", xaxis_tickangle=-45)
    fig.write_html(f"{OUTPUT_DIR}/weekly_roas.html")
    print(f"  ✅ Saved: weekly_roas.html")
    return fig


def chart_cost_efficiency(df):
    """Scatter plot — CPM vs CPC per platform."""
    efficiency = cost_efficiency(df).reset_index()

    fig = px.scatter(
        efficiency,
        x="avg_cpm",
        y="avg_cpc",
        color="platform",
        color_discrete_map=PLATFORM_COLORS,
        size=[20, 20, 20, 20],
        text="platform",
        title="Cost Efficiency: CPM vs CPC by Platform",
        labels={"avg_cpm": "Avg CPM (USD)", "avg_cpc": "Avg CPC (USD)"},
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(plot_bgcolor="white", showlegend=False)
    fig.write_html(f"{OUTPUT_DIR}/cost_efficiency.html")
    print(f"  ✅ Saved: cost_efficiency.html")
    return fig


def chart_top_campaigns(df):
    """Horizontal bar chart — top 10 campaigns by conversion value."""
    leaders = conversion_leaders(df, top_n=10)

    leaders["label"] = leaders["platform"] + " — " + leaders["campaign_name"]

    fig = px.bar(
        leaders.sort_values("total_conversion_value"),
        x="total_conversion_value",
        y="label",
        orientation="h",
        color="platform",
        color_discrete_map=PLATFORM_COLORS,
        title="Top 10 Campaigns by Conversion Value (Q1 2026)",
        labels={
            "total_conversion_value": "Total Conversion Value (USD)",
            "label": "",
        },
        text="total_conversion_value",
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(plot_bgcolor="white", showlegend=False)
    fig.write_html(f"{OUTPUT_DIR}/top_campaigns.html")
    print(f"  ✅ Saved: top_campaigns.html")
    return fig


def chart_dashboard(df):
    """Combined 2x2 dashboard — spend, ROAS, weekly trends, cost efficiency."""
    summary   = platform_summary(df).reset_index()
    trends    = weekly_trends(df)
    efficiency = cost_efficiency(df).reset_index()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Total Spend by Platform",
            "Overall ROAS by Platform",
            "Weekly Spend Trends",
            "CPM vs CPC Efficiency",
        )
    )

    # Top left — spend
    for _, row in summary.iterrows():
        fig.add_trace(go.Bar(
            x=[row["platform"]], y=[row["total_spend"]],
            name=row["platform"],
            marker_color=PLATFORM_COLORS[row["platform"]],
            showlegend=False,
        ), row=1, col=1)

    # Top right — ROAS
    for _, row in summary.iterrows():
        fig.add_trace(go.Bar(
            x=[row["platform"]], y=[row["overall_roas"]],
            name=row["platform"],
            marker_color=PLATFORM_COLORS[row["platform"]],
            showlegend=False,
        ), row=1, col=2)

    # Bottom left — weekly spend lines
    for platform in trends["platform"].unique():
        pdata = trends[trends["platform"] == platform]
        fig.add_trace(go.Scatter(
            x=pdata["week"], y=pdata["spend"],
            name=platform,
            line=dict(color=PLATFORM_COLORS[platform]),
            mode="lines+markers",
        ), row=2, col=1)

    # Bottom right — CPM vs CPC scatter
    for _, row in efficiency.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["avg_cpm"]], y=[row["avg_cpc"]],
            mode="markers+text",
            name=row["platform"],
            text=[row["platform"]],
            textposition="top center",
            marker=dict(size=14, color=PLATFORM_COLORS[row["platform"]]),
            showlegend=False,
        ), row=2, col=2)

    fig.update_layout(
        title_text="Marketing Analytics Dashboard — Q1 2026",
        height=800,
        plot_bgcolor="white",
    )
    fig.write_html(f"{OUTPUT_DIR}/dashboard.html")
    print(f"  ✅ Saved: dashboard.html")
    return fig


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading data and generating charts...\n")
    df = load_unified()

    chart_platform_spend(df)
    chart_roas_comparison(df)
    chart_weekly_spend(df)
    chart_weekly_roas(df)
    chart_cost_efficiency(df)
    chart_top_campaigns(df)
    chart_dashboard(df)

    print(f"\nAll charts saved to {OUTPUT_DIR}/")
    print("Open any .html file in your browser to view.")