import streamlit as st
import os
import pandas as pd
from modules.constants import TLOL_SPORTS
from modules.data_loader import load_and_merge_scores
from modules.avatar_utils import get_avatar_url


def render():
    # Centered Welcome Layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        #st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>🌟 Welcome to TLOL3!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:18px;'>Get ready for the ultimate showdown of skills, spirit, and sportsmanship!</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Load player data
    with st.spinner("Fetching highlight stats..."):
        df = load_and_merge_scores("reports")
        df.columns = df.columns.str.strip()

        if "TLOL Auction Player Type" in df.columns:
            df["Tier"] = df["TLOL Auction Player Type"].astype(str).str.strip().str.lower().map({
                "icon": "Icon",
                "lead": "Lead",
                "rest": "Rest"
            }).fillna("Rest")
        else:
            df["Tier"] = "Rest"

        sport_columns = [col for col in df.columns if col in TLOL_SPORTS]
        df["Total Score"] = df[sport_columns].sum(axis=1)

    # 🧿 Icon Players
    st.subheader("🌟 Featured Icon Players")
    icons = df[df["Tier"] == "Icon"]
    if not icons.empty:
        icon_cols = st.columns(len(icons))
        for i, (_, row) in enumerate(icons.iterrows()):
            with icon_cols[i % len(icon_cols)]:
                st.markdown(f"""
                    <div style='background: linear-gradient(to bottom right, #ffb347, #ffcc33); border-radius:12px; padding:12px; text-align:center; box-shadow:1px 1px 5px rgba(0,0,0,0.2); margin-bottom:10px;'>
                        <img src='{get_avatar_url(row['Player'], row['Gender'])}' width='64' style='border-radius:50%; border:2px solid #ffffff; margin-bottom:8px;' />
                        <div style='font-weight:bold; font-size:14px; color:#222;'>{row['Player']}</div>
                        <div style='font-size:13px; color:#333;'>Total Points: <strong>{int(row['Total Score'])}</strong></div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No icon players found.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # 🔥 Top Player from Each Sport
    st.subheader("🏅 Best Player in Each Sport")
    sport_emojis = {
        "Cricket": "🏏", "Chess": "♟️", "Carrom": "🎯", "Foosball": "⚽",
        "Here Places Treasure Hunt": "🗺️", "Housie": "🎲", "Olympics": "🏅",
        "PS5": "🎮", "Pen Fighting": "🖊️", "QPR cup activity": "🏆", "Table Tennis": "🏓"
    }

    for sport in TLOL_SPORTS:
        if sport in df.columns:
            top = df[["Player", sport]].sort_values(by=sport, ascending=False).head(1)
            if not top.empty and top.iloc[0][sport] > 0:
                name = top.iloc[0]["Player"]
                score = int(top.iloc[0][sport])
                emoji = sport_emojis.get(sport, "")
                st.markdown(f"""
                    <div style='background-color:#f4f4f4; color:#222; padding:10px 16px; border-radius:10px; margin:8px 0; box-shadow:0 1px 4px rgba(0,0,0,0.1);'>
                        <strong>{emoji} {sport}</strong>: {name} — <span style='font-weight:bold;'>{score} pts</span>
                    </div>
                """, unsafe_allow_html=True)
