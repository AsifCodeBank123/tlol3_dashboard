import streamlit as st
import os
import base64
import altair as alt
import pandas as pd
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

    def is_real_team(team):
        team_clean = str(team).strip().upper()
        return team_clean not in ["", "TBD", "TBC", "NONE"] and not team_clean.startswith("WINNER MATCH")

    is_final = round_name.lower() == "final" if round_name else False

    abbr1 = TEAM_ABBR.get(team1.strip().replace(" 🏆", "").replace(" 🦆", ""), team1[:2].upper())
    abbr2 = TEAM_ABBR.get(team2.strip().replace(" 🏆", "").replace(" 🦆", ""), team2[:2].upper())

    def get_initials(players):
        return ''.join([p.strip()[0].upper() for p in players if p.strip()])
    
    initials1 = get_initials(players1)
    initials2 = get_initials(players2)

    # Check winners
    team1_won = str(result1).strip().upper() == "W"
    team2_won = str(result2).strip().upper() == "W"

    # Stable keys for session state
    unique_hash = get_stable_hash(match_id, round_name, team1 + initials1, team2 + initials2, card_index, title)
    vote_key = f"vote_{unique_hash}"
    team_votes_key = f"votes_{unique_hash}"
   

    if team_votes_key not in st.session_state:
        st.session_state[team_votes_key] = {abbr1: 0, abbr2: 0}

    has_voted = vote_key in st.session_state
    voted_for = st.session_state.get(vote_key)

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
            has_voted=has_voted,
            voted_abbr=voted_for
        )
        st.markdown(html, unsafe_allow_html=True)
        
  