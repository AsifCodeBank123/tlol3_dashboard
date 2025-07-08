import streamlit as st
import os
import pandas as pd
from modules.constants import TLOL_SPORTS
from modules.data_loader import load_and_merge_scores
from modules.avatar_utils import get_avatar_url
from PIL import Image
from io import BytesIO
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

def render():
    # Centered Welcome Layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Background image (with fallback if image missing)
        image_path = "assets/curtain.jpg"
        if os.path.exists(image_path):
            bg_img = get_base64_image(image_path)
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("{bg_img}");
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        # Bollywood-styled title
        st.markdown("""
            <div style='text-align:center; padding-top: 60px;'>
                <h1 style='
                    font-family: "Impact", "Copperplate", sans-serif;
                    font-size: 64px;
                    color: #ffcc00;
                    text-shadow: 3px 3px 5px #000;
                    letter-spacing: 2px;
                '>
                    🎬 TCOE League of Legends 3
                </h1>
                <p style='
                    font-family: "Brush Script MT", cursive;
                    font-size: 28px;
                    color: #fff;
                    text-shadow: 2px 2px 4px #000;
                    margin-top: -10px;
                '>
                    "Drama, Dangal aur Dhamaka – Ab hoga asli muqabla!"
                </p>
            </div>
        """, unsafe_allow_html=True)

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
    st.subheader("🌟 Hamare Kohinoor")
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

    # # 🔥 Top Player from Each Sport
    # st.subheader("🏅 Best Player in Each Sport")
    # sport_emojis = {
    #     "Cricket": "🏏", "Chess": "♟️", "Carrom": "🎯", "Foosball": "⚽",
    #      "Housie": "🎲", "Olympics": "🏅",
    #     "PS5": "🎮",  "Table Tennis": "🏓"
    # }

    # for sport in TLOL_SPORTS:
    #     if sport in df.columns:
    #         top = df[["Player", sport]].sort_values(by=sport, ascending=False).head(1)
    #         if not top.empty and top.iloc[0][sport] > 0:
    #             name = top.iloc[0]["Player"]
    #             score = int(top.iloc[0][sport])
    #             emoji = sport_emojis.get(sport, "")
    #             st.markdown(f"""
    #                 <div style='background-color:#f4f4f4; color:#222; padding:10px 16px; border-radius:10px; margin:8px 0; box-shadow:0 1px 4px rgba(0,0,0,0.1);'>
    #                     <strong>{emoji} {sport}</strong>: {name} — <span style='font-weight:bold;'>{score} pts</span>
    #                 </div>
    #             """, unsafe_allow_html=True)

# --- Captains Section (to be inserted in home.py) ---

    st.markdown("""
        <style>
        .captain-card {
            background-color: #fff3e0;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px;
        }
        .captain-card img {
            border-radius: 50%;
            width: 100px;
            height: 100px;
            object-fit: cover;
        }
        .captain-name {
            font-weight: bold;
            font-size: 16px;
            color: #000;
        }
        .team-name {
            color: #f57c00;
            font-size: 14px;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color:#e65100;'>🎬 Hamare Kaptaans</h3>", unsafe_allow_html=True)

    captains = [
        {"team": "Gully Gang", "captain": "Jay Jagad", "img": "assets/gg_captain.jpg"},
        {"team": "Badshah Blasters", "captain": "Somansh Datta", "img": "assets/bb_captain.jpg"},
        {"team": "Rockstar Rebels", "captain": "Blessen Thomas", "img": "assets/rr_captain.jpg"},
        {"team": "Dabangg Dynamos", "captain": "Lalit Chavan", "img": "assets/dd_captain.jpg"},
    ]

    cols = st.columns(4)
    for i, cap in enumerate(captains):
        with cols[i]:
            img_base64 = get_base64_image(cap["img"])
            st.markdown(f"""
                <div class='captain-card'>
                    <img src="{img_base64}" />
                    <div class='captain-name'>{cap['captain']}</div>
                    <div class='team-name'>{cap['team']}</div>
                </div>
            """, unsafe_allow_html=True)
