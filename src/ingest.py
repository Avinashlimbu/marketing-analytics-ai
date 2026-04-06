# ingest.py
# Loads all 4 platform CSVs and normalizes them into one unified DataFrame
# Each platform has different column names — this script reconciles them all

import pandas as pd
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────

DATA_DIR = "data/mock"

# ── PLATFORM LOADERS ──────────────────────────────────────────────────────────

def load_meta(filepath):
    """Load and normalize Meta Ads data."""
    df = pd.read_csv(filepath)
    df["platform"] = "meta"

    # Meta already uses our target column names — just select what we need
    return df[[
        "date", "platform", "campaign_id", "campaign_name",
        "impressions", "clicks", "spend", "conversions",
        "conversion_value", "ctr", "cpc", "cpm", "roas"
    ]]


def load_google_ads(filepath):
    """Load and normalize Google Ads data."""
    df = pd.read_csv(filepath)
    df["platform"] = "google_ads"

    # Google calls it "cost" — rename to "spend"
    df = df.rename(columns={"cost": "spend"})

    return df[[
        "date", "platform", "campaign_id", "campaign_name",
        "impressions", "clicks", "spend", "conversions",
        "conversion_value", "ctr", "cpc", "cpm", "roas"
    ]]

def load_dv360(filepath):
    """Load and normalize DV360 data."""
    df = pd.read_csv(filepath)
    df["platform"] = "dv360"

    # DV360 uses "insertion_order" instead of "campaign"
    # It also uses "media_cost" instead of "spend"
    df = df.rename(columns={
        "insertion_order_id":   "campaign_id",
        "insertion_order_name": "campaign_name",
        "media_cost":           "spend",
    })

    # Calculate roas since DV360 doesn't include it directly
    df["roas"] = (df["conversion_value"] / df["spend"]).round(2)
    df["roas"] = df["roas"].fillna(0)

    return df[[
        "date", "platform", "campaign_id", "campaign_name",
        "impressions", "clicks", "spend", "conversions",
        "conversion_value", "ctr", "cpc", "cpm", "roas"
    ]]

def load_x_ads(filepath):
    """Load and normalize X Ads data."""
    df = pd.read_csv(filepath)
    df["platform"] = "x_ads"

    # X already uses our target column names — just select what we need
    return df[[
        "date", "platform", "campaign_id", "campaign_name",
        "impressions", "clicks", "spend", "conversions",
        "conversion_value", "ctr", "cpc", "cpm", "roas"
    ]]


# ── MAIN INGEST FUNCTION ──────────────────────────────────────────────────────

def ingest_all():
    """Load all platforms and return one unified DataFrame."""

    loaders = {
        "meta":       (load_meta,       f"{DATA_DIR}/meta.csv"),
        "google_ads": (load_google_ads, f"{DATA_DIR}/google_ads.csv"),
        "dv360":      (load_dv360,      f"{DATA_DIR}/dv360.csv"),
        "x_ads":      (load_x_ads,      f"{DATA_DIR}/x_ads.csv"),
    }

    dfs = []
    for platform, (loader, filepath) in loaders.items():
        if not os.path.exists(filepath):
            print(f"  ⚠️  File not found, skipping: {filepath}")
            continue
        df = loader(filepath)
        dfs.append(df)
        print(f"  ✅ Loaded {platform}: {len(df)} rows")

    # Combine all platforms into one table
    unified = pd.concat(dfs, ignore_index=True)

    # Ensure date is a proper datetime type
    unified["date"] = pd.to_datetime(unified["date"])

    # Sort by date then platform
    unified = unified.sort_values(["date", "platform"]).reset_index(drop=True)

    print(f"\n  📊 Unified table: {len(unified)} rows, {len(unified.columns)} columns")
    print(f"  📅 Date range: {unified['date'].min().date()} → {unified['date'].max().date()}")
    print(f"  🏷️  Platforms: {unified['platform'].unique().tolist()}")

    return unified


# ── RUN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Ingesting all platform data...\n")
    df = ingest_all()

    print("\nSample output (first 4 rows, one per platform):")
    print(df.groupby("platform").first().to_string())

    # Save unified output
    output_path = "data/mock/unified.csv"
    df.to_csv(output_path, index=False)
    print(f"\n  💾 Saved to {output_path}")