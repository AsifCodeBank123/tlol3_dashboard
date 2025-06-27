# modules/tier_utils.py

def assign_tiers(df):
    # Try renaming if old Tier exists
    if "TLOL Auction Player Type" in df.columns:
        df["Tier"] = df["TLOL Auction Player Type"]
    elif "Tier" in df.columns:
        df["Tier"] = df["Tier"]
    else:
        df["Tier"] = "Rest"  # default fallback
    return df


