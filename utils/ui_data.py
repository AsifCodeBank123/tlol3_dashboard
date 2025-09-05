import streamlit as st
import os
import base64
from utils.html_blocks import build_card_html
import hashlib

def get_stable_hash(*args):
    input_string = "_".join([str(arg) for arg in args])
    return hashlib.md5(input_string.encode()).hexdigest()[:8]


TEAM_LOGOS = {
    "Gully Gang": "assets/gg_logo.png",
    "Badshah Blasters": "assets/bb_logo.png",
    "Dabangg Dynamos": "assets/dd_logo.png",
    "Rockstar Rebels": "assets/rr_logo.png"
}

TEAM_ABBR = {
    "Gully Gang": "GG",
    "Badshah Blasters": "BB",
    "Dabangg Dynamos": "DD",
    "Rockstar Rebels": "RR"
}

TEAM_COLORS = {
    "Gully Gang": "#FFF2DE",
    "Badshah Blasters": "#E3F2FD",
    "Dabangg Dynamos": "#E6F4EA",
    "Rockstar Rebels": "#F3E5F5"
}

def encode_image(path):
    if path and os.path.exists(path):
        with open(path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return ""

# === Helpers ===
def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === Main Card Renderer ===
def display_card(title, team1, players1, team2, players2,
                 match_id, round_name, card_index=0, result1="", result2=""):

    
    with st.container():
        html = build_card_html(
            title=title,
            team1=team1,
            players1=players1,
            team2=team2,
            players2=players2,
            team1_logo=TEAM_LOGOS.get(team1.strip(), "assets/tbd_logo.png"),
            team2_logo=TEAM_LOGOS.get(team2.strip(), "assets/tbd_logo.png"),
            result1=result1,
            result2=result2,
           
        )
        st.markdown(html, unsafe_allow_html=True)
        
  