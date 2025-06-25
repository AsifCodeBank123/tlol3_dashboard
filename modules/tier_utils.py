# modules/tier_utils.py

def assign_tiers(df):
    def get_tier(score):
        if score >= 500:
            return "Diamond"
        elif score >= 250:
            return "Gold"
        elif score >= 100:
            return "Silver"
        else:
            return "Bronze"

    df['Tier'] = df['Total Score'].apply(get_tier)
    return df
