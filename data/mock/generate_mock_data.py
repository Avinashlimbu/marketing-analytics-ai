# generate_mock_data.py
# Generates fake but realistic marketing data for all 4 platforms
# Output: one CSV per platform in data/mock/

import pandas as pd
import random
from datetime import datetime, timedelta

# ── CONFIG ────────────────────────────────────────────────────────────────────

START_DATE = "2026-01-01"
END_DATE   = "2026-03-31"
OUTPUT_DIR = "data/mock"

# Fake campaign names per platform
CAMPAIGNS = {
    "meta": [
        "Brand Awareness Q1",
        "Retargeting — Website Visitors",
        "Prospecting — Lookalike 1%",
        "App Install — iOS",
    ],
    "google_ads": [
        "Search — Brand Keywords",
        "Search — Competitor Keywords",
        "Performance Max — All Products",
        "Display — Retargeting",
    ],
    "dv360": [
        "Programmatic Display — Prospecting",
        "YouTube Pre-roll — Brand",
        "Programmatic Video — Retargeting",
    ],
    "x_ads": [
        "Promoted Tweets — Engagement",
        "Website Clicks — Fintech Audience",
        "Follower Campaign — Brand",
    ],
}

# ── HELPERS ───────────────────────────────────────────────────────────────────

def date_range(start, end):
    """Generate list of dates between start and end."""
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt   = datetime.strptime(end,   "%Y-%m-%d")
    days = (end_dt - start_dt).days + 1
    return [(start_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

def rand(min_val, max_val, decimals=0):
    """Random number between min and max, optionally with decimals."""
    val = random.uniform(min_val, max_val)
    return round(val, decimals) if decimals > 0 else int(val)

# ── GENERATORS ────────────────────────────────────────────────────────────────

def generate_meta(dates):
    rows = []
    for date in dates:
        for i, campaign in enumerate(CAMPAIGNS["meta"]):
            impressions     = rand(5000, 80000)
            clicks          = rand(50, int(impressions * 0.05))
            spend           = rand(50, 500, 2)
            conversions     = rand(0, int(clicks * 0.1))
            conversion_value = round(conversions * rand(20, 150, 2), 2)
            rows.append({
                "date":             date,
                "campaign_id":      f"META_00{i+1}",
                "campaign_name":    campaign,
                "objective":        random.choice(["CONVERSIONS", "TRAFFIC", "AWARENESS"]),
                "impressions":      impressions,
                "clicks":           clicks,
                "spend":            spend,
                "conversions":      conversions,
                "conversion_value": conversion_value,
                "ctr":              round(clicks / impressions, 4),
                "cpc":              round(spend / clicks, 2) if clicks > 0 else 0,
                "cpm":              round(spend / impressions * 1000, 2),
                "roas":             round(conversion_value / spend, 2) if spend > 0 else 0,
            })
    return pd.DataFrame(rows)


def generate_google_ads(dates):
    rows = []
    for date in dates:
        for i, campaign in enumerate(CAMPAIGNS["google_ads"]):
            impressions      = rand(3000, 60000)
            clicks           = rand(30, int(impressions * 0.06))
            cost             = rand(40, 600, 2)
            # Google conversions can be fractional
            conversions      = round(random.uniform(0, clicks * 0.08), 1)
            conversion_value = round(conversions * rand(20, 200, 2), 2)
            rows.append({
                "date":             date,
                "campaign_id":      f"GADS_00{i+1}",
                "campaign_name":    campaign,
                "campaign_type":    random.choice(["SEARCH", "DISPLAY", "PERFORMANCE_MAX"]),
                "impressions":      impressions,
                "clicks":           clicks,
                "cost":             cost,
                "conversions":      conversions,
                "conversion_value": conversion_value,
                "ctr":              round(clicks / impressions, 4),
                "cpc":              round(cost / clicks, 2) if clicks > 0 else 0,
                "cpm":              round(cost / impressions * 1000, 2),
                "roas":             round(conversion_value / cost, 2) if cost > 0 else 0,
                "quality_score":    rand(4, 10),
            })
    return pd.DataFrame(rows)


def generate_dv360(dates):
    rows = []
    for date in dates:
        for i, campaign in enumerate(CAMPAIGNS["dv360"]):
            impressions              = rand(10000, 200000)
            clicks                   = rand(20, int(impressions * 0.02))
            media_cost               = rand(100, 800, 2)
            total_cost               = round(media_cost * random.uniform(1.1, 1.2), 2)
            conversions              = round(random.uniform(0, clicks * 0.05), 1)
            conversion_value         = round(conversions * rand(20, 180, 2), 2)
            view_through_conversions = rand(0, 20)
            click_through_conversions = int(conversions)
            rows.append({
                "date":                       date,
                "insertion_order_id":         f"DV_IO_00{i+1}",
                "insertion_order_name":       campaign,
                "line_item_id":               f"DV_LI_00{i+1}",
                "line_item_name":             campaign + " — Line Item 1",
                "channel":                    random.choice(["DISPLAY", "VIDEO", "YOUTUBE"]),
                "impressions":                impressions,
                "clicks":                     clicks,
                "media_cost":                 media_cost,
                "total_cost":                 total_cost,
                "conversions":                conversions,
                "conversion_value":           conversion_value,
                "ctr":                        round(clicks / impressions, 4),
                "cpc":                        round(media_cost / clicks, 2) if clicks > 0 else 0,
                "cpm":                        round(media_cost / impressions * 1000, 2),
                "view_through_conversions":   view_through_conversions,
                "click_through_conversions":  click_through_conversions,
            })
    return pd.DataFrame(rows)


def generate_x_ads(dates):
    rows = []
    for date in dates:
        for i, campaign in enumerate(CAMPAIGNS["x_ads"]):
            impressions      = rand(2000, 40000)
            clicks           = rand(20, int(impressions * 0.04))
            spend            = rand(30, 300, 2)
            conversions      = rand(0, int(clicks * 0.05))
            conversion_value = round(conversions * rand(15, 100, 2), 2)
            engagements      = rand(clicks, int(impressions * 0.08))
            rows.append({
                "date":             date,
                "campaign_id":      f"X_00{i+1}",
                "campaign_name":    campaign,
                "objective":        random.choice(["WEBSITE_CLICKS", "ENGAGEMENTS", "FOLLOWERS"]),
                "impressions":      impressions,
                "clicks":           clicks,
                "spend":            spend,
                "conversions":      conversions,
                "conversion_value": conversion_value,
                "engagements":      engagements,
                "ctr":              round(clicks / impressions, 4),
                "cpc":              round(spend / clicks, 2) if clicks > 0 else 0,
                "cpm":              round(spend / impressions * 1000, 2),
                "engagement_rate":  round(engagements / impressions, 4),
                "roas":             round(conversion_value / spend, 2) if spend > 0 else 0,
            })
    return pd.DataFrame(rows)

# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dates = date_range(START_DATE, END_DATE)
    print(f"Generating data for {len(dates)} days ({START_DATE} to {END_DATE})...")

    generators = {
        "meta":       generate_meta,
        "google_ads": generate_google_ads,
        "dv360":      generate_dv360,
        "x_ads":      generate_x_ads,
    }

    for platform, generator in generators.items():
        df = generator(dates)
        filepath = f"{OUTPUT_DIR}/{platform}.csv"
        df.to_csv(filepath, index=False)
        print(f"  ✅ {platform}: {len(df)} rows → {filepath}")

    print("\nDone! All mock data generated.")