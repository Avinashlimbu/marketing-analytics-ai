# dashboard.py
# Streamlit web dashboard — ties together analysis, visualizations, and AI insights
# Run with: streamlit run src/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Make sure src/ modules are importable
sys.path.append(os.path.dirname(__file__))

from analyze import (
    load_unified,
    platform_summary,
    best_worst_campaigns,
    weekly_trends,
    cost_efficiency,
    conversion_leaders,
)
from ai_layer import (
    ai_platform_summary,
    ai_campaign_analysis,
    ai_weekly_trends,
    ai_recommendations,
)

# ── CONFIG ────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

PLATFORM_COLORS = {
    "meta":       "#1877F2",
    "google_ads": "#34A853",
    "dv360":      "#FF6D00",
    "x_ads":      "#000000",
}

# ── LOAD DATA ─────────────────────────────────────────────────────────────────

@st.cache_data
def get_data():
    return load_unified("data/mock/unified.csv")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

def render_sidebar(df):
    st.sidebar.title("📊 Filters")

    # Date range filter
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Handle mid-selection state when only start date is picked
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = date_range[0], max_date
    # Platform filter
    platforms = sorted(df["platform"].unique().tolist())
    selected_platforms = st.sidebar.multiselect(
        "Platforms",
        options=platforms,
        default=platforms,
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown(
        "Marketing analytics dashboard built with Python, "
        "Pandas, Plotly, and Claude AI."
    )

    return start_date, end_date, selected_platforms


def filter_data(df, start_date, end_date, platforms):
    """Apply sidebar filters to the dataframe."""
    mask = (
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date) &
        (df["platform"].isin(platforms))
    )
    return df[mask]

# ── TAB 1: OVERVIEW ───────────────────────────────────────────────────────────

def render_overview(df):
    st.header("Performance Overview")

    # Top KPI metrics
    col1, col2, col3, col4 = st.columns(4)

    total_spend       = df["spend"].sum()
    total_conversions = df["conversions"].sum()
    total_value       = df["conversion_value"].sum()
    overall_roas      = total_value / total_spend if total_spend > 0 else 0

    col1.metric("Total Spend",       f"${total_spend:,.0f}")
    col2.metric("Total Conversions", f"{total_conversions:,.0f}")
    col3.metric("Conversion Value",  f"${total_value:,.0f}")
    col4.metric("Overall ROAS",      f"{overall_roas:.2f}x")

    st.markdown("---")

    # Platform summary table
    st.subheader("Platform Breakdown")
    summary = platform_summary(df).reset_index()
    summary_display = summary[[
        "platform", "total_spend", "total_conversions",
        "total_conversion_value", "overall_roas", "avg_cpc", "avg_cpm"
    ]].copy()

    summary_display.columns = [
        "Platform", "Total Spend", "Conversions",
        "Conversion Value", "ROAS", "Avg CPC", "Avg CPM"
    ]

    # Format currency columns
    for col in ["Total Spend", "Conversion Value", "Avg CPC", "Avg CPM"]:
        summary_display[col] = summary_display[col].apply(lambda x: f"${x:,.2f}")
    summary_display["ROAS"] = summary_display["ROAS"].apply(lambda x: f"{x:.2f}x")

    st.dataframe(summary_display, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Spend vs ROAS side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Total Spend by Platform")
        fig = px.bar(
            summary, x="platform", y="total_spend",
            color="platform",
            color_discrete_map=PLATFORM_COLORS,
            labels={"total_spend": "Total Spend (USD)", "platform": ""},
            text="total_spend",
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("ROAS by Platform")
        fig = px.bar(
            summary, x="platform", y="overall_roas",
            color="platform",
            color_discrete_map=PLATFORM_COLORS,
            labels={"overall_roas": "ROAS", "platform": ""},
            text="overall_roas",
        )
        fig.update_traces(texttemplate="%{text:.2f}x", textposition="outside")
        fig.update_layout(showlegend=False, plot_bgcolor="white", height=350)
        st.plotly_chart(fig, use_container_width=True)

# ── TAB 2: CHARTS ─────────────────────────────────────────────────────────────

def render_charts(df):
    st.header("Performance Charts")

    # Weekly trends
    st.subheader("Weekly Spend Trends")
    trends = weekly_trends(df)
    fig = px.line(
        trends, x="week", y="spend", color="platform",
        color_discrete_map=PLATFORM_COLORS,
        labels={"spend": "Spend (USD)", "week": "Week"},
        markers=True,
    )
    fig.update_layout(plot_bgcolor="white", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Weekly ROAS Trends")
    fig = px.line(
        trends, x="week", y="roas", color="platform",
        color_discrete_map=PLATFORM_COLORS,
        labels={"roas": "ROAS", "week": "Week"},
        markers=True,
    )
    fig.update_layout(plot_bgcolor="white", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Cost efficiency + top campaigns side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cost Efficiency: CPM vs CPC")
        efficiency = cost_efficiency(df).reset_index()
        fig = px.scatter(
            efficiency, x="avg_cpm", y="avg_cpc",
            color="platform",
            color_discrete_map=PLATFORM_COLORS,
            text="platform",
            labels={"avg_cpm": "Avg CPM (USD)", "avg_cpc": "Avg CPC (USD)"},
            size=[20] * len(efficiency),
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(plot_bgcolor="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 Campaigns by Conversion Value")
        leaders = conversion_leaders(df, top_n=10)
        leaders["label"] = leaders["platform"] + " — " + leaders["campaign_name"]
        fig = px.bar(
            leaders.sort_values("total_conversion_value"),
            x="total_conversion_value", y="label",
            orientation="h",
            color="platform",
            color_discrete_map=PLATFORM_COLORS,
            labels={"total_conversion_value": "Conversion Value (USD)", "label": ""},
            text="total_conversion_value",
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(plot_bgcolor="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ── TAB 3: AI INSIGHTS ────────────────────────────────────────────────────────

def render_ai_insights(df):
    st.header("AI Insights")
    st.info(
        "AI analysis is powered by Claude. "
        "Currently running in mock mode — set USE_REAL_API = True "
        "in src/ai_layer.py to enable real analysis.",
        icon="ℹ️"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Platform Performance Analysis")
        if st.button("Generate Platform Analysis", key="btn_platform"):
            with st.spinner("Analyzing..."):
                result = ai_platform_summary(df)
            st.markdown(result)

        st.subheader("Campaign Winners & Losers")
        if st.button("Generate Campaign Analysis", key="btn_campaigns"):
            with st.spinner("Analyzing..."):
                result = ai_campaign_analysis(df)
            st.markdown(result)

    with col2:
        st.subheader("Weekly Trend Analysis")
        if st.button("Generate Trend Analysis", key="btn_trends"):
            with st.spinner("Analyzing..."):
                result = ai_weekly_trends(df)
            st.markdown(result)

        st.subheader("Q2 Budget Recommendations")
        if st.button("Generate Recommendations", key="btn_recommendations"):
            with st.spinner("Analyzing..."):
                result = ai_recommendations(df)
            st.markdown(result)

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    st.title("📊 Marketing Analytics Dashboard")
    st.caption("Q1 2026 — Meta, Google Ads, DV360, X Ads")

    # Load and filter data
    df = get_data()
    start_date, end_date, selected_platforms = render_sidebar(df)
    filtered_df = filter_data(df, start_date, end_date, selected_platforms)

    if filtered_df.empty:
        st.warning("No data for selected filters. Adjust the date range or platforms.")
        return

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Overview", "Charts", "AI Insights"])

    with tab1:
        render_overview(filtered_df)
    with tab2:
        render_charts(filtered_df)
    with tab3:
        render_ai_insights(filtered_df)


if __name__ == "__main__":
    main()