import streamlit as st
import os
import base64
import altair as alt
import pandas as pd
from utils.html_blocks import build_card_html
import hashlib
from fixtures_modules.database_handler import load_votes, save_votes

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
            team1_logo=TEAM_LOGOS.get(team1.strip(), "assets/tbd_logo.png"),
            team2_logo=TEAM_LOGOS.get(team2.strip(), "assets/tbd_logo.png"),
            result1=result1,
            result2=result2,
            has_voted=has_voted,
            voted_abbr=voted_for
        )
        st.markdown(html, unsafe_allow_html=True)

        # --- Ensure votes cache exists ---
        if "votes_df" not in st.session_state:
            st.session_state.votes_df = load_votes()  # single API call
        votes_df = st.session_state.votes_df

        # --- Initialize per-match session keys ---
        if vote_key not in st.session_state:
            st.session_state[vote_key] = None
        has_voted = st.session_state[vote_key] is not None
        voted_for = st.session_state[vote_key]

       # --- Compute current vote counts ---
        def compute_vote_counts(votes_df, match_id, abbr1, abbr2):
            match_votes = votes_df[votes_df["match_id"].astype(str) == str(match_id)]
            votes = {abbr1: 0, abbr2: 0}
            for abbr in [abbr1, abbr2]:
                row = match_votes[match_votes["abbr"] == abbr]
                if not row.empty:
                    votes[abbr] = int(row.iloc[0]["votes"])
            return votes

        vote_counts = compute_vote_counts(votes_df, match_id, abbr1, abbr2)

        # --- Voting UI ---
        if is_real_team(team1) and is_real_team(team2):
            if not has_voted:
                vote = st.radio(
                    "🙌 Support your team:",
                    [abbr1, abbr2],
                    key=radio_key,
                    horizontal=True
                )
                if st.button("Submit Vote", key=submit_key):
                    # Update local session cache
                    match_mask = (votes_df["match_id"].astype(str) == str(match_id)) & (votes_df["abbr"] == vote)
                    if match_mask.any():
                        votes_df.loc[match_mask, "votes"] += 1
                    else:
                        votes_df = pd.concat([
                            votes_df,
                            pd.DataFrame([[match_id, vote, 1]], columns=["match_id", "abbr", "votes"])
                        ], ignore_index=True)

                    st.session_state.votes_df = votes_df  # save updated cache
                    st.session_state[vote_key] = vote     # mark user as voted

                    # --- Push update to Google Sheets ---
                    save_votes(votes_df)

                    st.rerun()
            

        # --- Display vote counts with CSS cards ---
        votes_list = [vote_counts[abbr1], vote_counts[abbr2]]
        total_votes = sum(votes_list)

        # Fallback info if no votes
        if total_votes == 0:
            st.info("No votes yet. Be the first to support your team! 🎉")

        # --- CSS styles for vote cards ---
        st.markdown(
            """
            <style>
            .vote-container {
                display: flex;
                justify-content: space-around;
                margin-top: 10px;
                margin-bottom: 20px;
            }
            .vote-card {
                flex: 1;
                margin: 0 5px;
                padding: 12px;
                border-radius: 12px;
                background: linear-gradient(135deg, #2196f3, #21cbf3);
                color: white;
                font-weight: bold;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .vote-card.team2 {
                background: linear-gradient(135deg, #e91e63, #f06292);
            }
            .vote-count {
                font-size: 18px;
                margin-top: 6px;
            }
            </style>
            """, unsafe_allow_html=True
        )

        # --- Generate HTML for vote cards ---
        html_votes = f"""
        <div class="vote-container">
            <div class="vote-card team1">
                {abbr1}
                <div class="vote-count">{votes_list[0]} vote{'s' if votes_list[0] != 1 else ''}</div>
            </div>
            <div class="vote-card team2">
                {abbr2}
                <div class="vote-count">{votes_list[1]} vote{'s' if votes_list[1] != 1 else ''}</div>
            </div>
        </div>
        """

        st.markdown(html_votes, unsafe_allow_html=True)






