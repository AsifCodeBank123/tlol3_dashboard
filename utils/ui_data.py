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

def display_card(title, team1, players1, team2, players2,
                 match_id, round_name, card_index=0):

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

    # === Safe key hash ===
    unique_hash = get_stable_hash(match_id,round_name,team1 + initials1,team2 + initials2,card_index,title)

    vote_key = f"vote_{unique_hash}"
    team_votes_key = f"votes_{unique_hash}"
    radio_key = f"radio_{unique_hash}"
    submit_key = f"submit_{unique_hash}"

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
            team1_logo=TEAM_LOGOS.get(team1.strip().replace(" 🏆", "").replace(" 🦆", ""), "assets/tbd_logo.png"),
            team2_logo=TEAM_LOGOS.get(team2.strip().replace(" 🏆", "").replace(" 🦆", ""), "assets/tbd_logo.png"),
            team1_pct=0,
            team2_pct=0,
            has_voted=has_voted,
            voted_abbr=voted_for
        )
        st.markdown(html, unsafe_allow_html=True)

        if is_real_team(team1) and is_real_team(team2):
            if not has_voted:
                vote = st.radio(
                    f"🙌 Support your team:",
                    [abbr1, abbr2],
                    key=radio_key,
                    horizontal=True
                )
                if st.button("Submit Vote", key=submit_key):
                    st.session_state[team_votes_key][vote] += 1
                    st.session_state[vote_key] = vote
                    st.rerun()
            else:
                st.markdown(f"✅ You supported: **{voted_for}**")

            vote_counts = st.session_state[team_votes_key]
            data = pd.DataFrame({
                "Team": [abbr1, abbr2],
                "Votes": [vote_counts[abbr1], vote_counts[abbr2]]
            })

            bar_chart = alt.Chart(data).mark_bar(size=40).encode(
                x=alt.X("Votes:Q", title="Votes"),
                y=alt.Y("Team:N", sort="-x", title=None),
                color=alt.Color("Team:N", scale=alt.Scale(range=["#2196f3", "#e91e63"]))
            ).properties(height=120)

            if vote_counts[abbr1] == 0 and vote_counts[abbr2] == 0:
                st.info("No votes yet. Be the first to support your team! 🎉")
            else:
                st.altair_chart(bar_chart, use_container_width=True)


        elif team1.strip().split()[0] == team2.strip().split()[0]:
            st.markdown(
                "<div style='text-align:center; color:gray;'>📌 Voting not available for same-team matches</div>",
                unsafe_allow_html=True
            )

