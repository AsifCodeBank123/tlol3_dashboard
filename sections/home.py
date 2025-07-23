import streamlit as st
import os

from modules.data_loader import load_and_merge_scores
from modules.avatar_utils import get_avatar_url

import base64
import streamlit.components.v1 as components

def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_global_styles()



def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

def render():
    load_global_styles()

    # Background
    image_path = "assets/curtain.jpg"
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            bg_img = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""<style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{bg_img}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>""",
            unsafe_allow_html=True,
        )
    # Title
    st.markdown("""
        <div style='text-align:center; padding-top: 55px;'>
            <h1 style='
                font-family: "Impact", "Copperplate", sans-serif;
                font-size: 64px;
                color: #ffcc00;
                text-shadow: 3px 3px 5px #000;
                letter-spacing: 2px;'>
                🎬 TCOE League of Legends 3
            </h1>
            <marquee scrollamount="8" direction="left" style='
                font-family: "Rock Salt","Brush Script MT",cursive;
                font-size: 22px;
                color: #fffbe7;
                background: rgba(0,0,0,0.45);
                border-radius:14px;
                padding: 8px 0; 
                margin-bottom:8px;
                letter-spacing: 1.5px;
                width:98%; display: block; margin-left:auto; margin-right:auto;'>
                💥 Breaking: Welcome to TCOE League of Legends Season 3! Prepare for epic showdowns, iconic players & bollywood drama. Stay tuned for daily updates & team rankings! 🔥
            </marquee>
            <p style='
                font-family: "Brush Script MT", cursive;
                font-size: 28px;
                color: #fff;
                text-shadow: 2px 2px 4px #000;
                margin-top: -10px;'>
                "Lights,Camera,Dhamaal – Ab hoga asli bawaal!"
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#ffcc00;'>", unsafe_allow_html=True)


    # 🧿 Icon Players
    st.markdown("<h3 style='color:#ffc107; text-align:center; font-weight:bold;'>🌟 Hamare Kohinoor</h3>", unsafe_allow_html=True)
    
    # Make sure df is loaded before this point!
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

    icons = df[df["Tier"] == "Icon"]
    if not icons.empty:
        icon_cols = st.columns(min(len(icons), 6))
        for i, (_, row) in enumerate(icons.iterrows()):
            with icon_cols[i % len(icon_cols)]:
                img_url = get_avatar_url(row['Player'], row['Gender'])

                components.html(f"""
    <div style='
        background: radial-gradient(circle at top left, #fff8e1, #ffe082);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        transition: 0.3s ease;
        position: relative;
        width: 100%;
    '>
        <div style='
            width: 80px;
            height: 80px;
            margin: 0 auto 8px;
            border-radius: 50%;
            border: 3px solid #ffd600;
            padding: 3px;
            background-color: #fff;
        '>
            <img src="{img_url}" width="100%" style='border-radius:50%;'>
        </div>

        <div style='font-weight: 700; font-size: 14.5px; color: #3e3e3e;'>{row['Player']}</div>
        <div style='font-size: 13px; color: #6d4c41;'>
            Total Points: <span style='font-weight:700;'>{int(row['Total Score'])}</span>
        </div>
    </div>
""", height=230)

    else:
        st.info("No icon players found.")




# --- Captains Section (to be inserted in home.py) ---

    st.markdown("""
    <style>
    .captain-card {
        background-color: #fff8e1;
        border-radius: 13px;
        padding: 17px 8px 11px 8px;
        text-align: center;
        box-shadow: 0 3px 16px rgba(251,181,67,0.13);
        margin: 13px 5px 15px 5px;
        min-height: 225px;
    }
    .captain-card img {
        border-radius: 50%;
        width: 92px;
        height: 92px;
        object-fit: cover;
        margin-bottom: 10px;
        box-shadow: 0 2px 22px rgba(255,186,86,0.16);
    }
    .captain-name {
        font-weight: bold;
        font-size: 17px;
        color: #b3741b;
        margin-bottom: 2px;
    }
    .team-name {
        color: #f57c00;
        font-size: 14px;
        font-style: italic;
        margin-bottom: 2px;
    }
    </style>
""", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#ff6f00; text-align:center;'>🎬 Hamare Kaptaans</h3>", unsafe_allow_html=True)

    captains = [
        {"team": "Gully Gang", "captain": "Jay Jagad", "img": "assets/gg_captain.jpg"},
        {"team": "Badshah Blasters", "captain": "Somansh Datta", "img": "assets/bb_captain.jpg"},
        {"team": "Rockstar Rebels", "captain": "Blessen Thomas", "img": "assets/rr_captain.jpg"},
        {"team": "Dabangg Dynamos", "captain": "Lalit Chavan", "img": "assets/dd_captain.jpg"},
    ]

    cols = st.columns(len(captains))
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

