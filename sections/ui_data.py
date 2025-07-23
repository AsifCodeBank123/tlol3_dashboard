import streamlit as st
import os
import base64

def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_global_styles()



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

def build_card_html(title, team1, players1, team2, players2,
                    team1_logo, team2_logo,
                    team1_pct, team2_pct,
                    has_voted=False, voted_abbr=None):

    abbr1 = TEAM_ABBR.get(team1.strip().replace(" 🏆", "").replace(" 🦆", ""), team1[:2].upper())
    abbr2 = TEAM_ABBR.get(team2.strip().replace(" 🏆", "").replace(" 🦆", ""), team2[:2].upper())

    p1 = " & ".join(players1) if players1 else "TBD"
    p2 = " & ".join(players2) if players2 else "TBD"

    show_logo1 = team1_logo if os.path.exists(team1_logo) else "assets/tbd_logo.png"
    show_logo2 = team2_logo if os.path.exists(team2_logo) else "assets/tbd_logo.png"

    if "🏆" in team1:
        show_logo1 = "assets/winner.png"
    elif "🦆" in team1:
        show_logo1 = "assets/blnt.jpg"
    if "🏆" in team2:
        show_logo2 = "assets/winner.png"
    elif "🦆" in team2:
        show_logo2 = "assets/blnt.png"

    logo1_b64 = encode_image(show_logo1)
    logo2_b64 = encode_image(show_logo2)

    html = f"""
    <div class="match-card">
      <div class="match-title">{title}</div>
      <div style="display:flex; justify-content:space-between; align-items:stretch;">
        <div class="team-box">
          <div class="team-flex">
            <img src="{logo1_b64}" class="team-img" />
            <div class="team-abbr">{abbr1} ({team1_pct}%)</div>
          </div>
          <div class="team-name">{team1}</div>
          <div class="player-names">{p1}</div>
        </div>
        <div class="match-versus">⚔️</div>
        <div class="team-box">
          <div class="team-flex">
            <img src="{logo2_b64}" class="team-img" />
            <div class="team-abbr">{abbr2} ({team2_pct}%)</div>
          </div>
          <div class="team-name">{team2}</div>
          <div class="player-names">{p2}</div>
        </div>
      </div>
    </div>
    """
    return html

def display_card(title, team1, players1, team2, players2,
                 match_id, round_name, card_index=0):

    def is_real_team(team):
        team_clean = str(team).strip().upper()
        return (
            team_clean not in ["", "TBD", "TBC", "NONE"]
            and not team_clean.startswith("WINNER MATCH")
        )

    abbr1 = TEAM_ABBR.get(team1.strip().replace(" 🏆", "").replace(" 🦆", ""), team1[:2].upper())
    abbr2 = TEAM_ABBR.get(team2.strip().replace(" 🏆", "").replace(" 🦆", ""), team2[:2].upper())

    unique_prefix = f"{match_id}_{round_name.lower().replace(' ', '_')}"
    vote_key_1 = f"{unique_prefix}_{abbr1}_votes"
    vote_key_2 = f"{unique_prefix}_{abbr2}_votes"
    user_vote_key = f"vote_{unique_prefix}_voted"
    button_key_1 = f"{unique_prefix}_{abbr1}_vote_btn_{card_index}"
    button_key_2 = f"{unique_prefix}_{abbr2}_vote_btn_{card_index}"

    # Init
    if vote_key_1 not in st.session_state:
        st.session_state[vote_key_1] = 0
    if vote_key_2 not in st.session_state:
        st.session_state[vote_key_2] = 0
    if user_vote_key not in st.session_state:
        st.session_state[user_vote_key] = None

    t1_votes = st.session_state[vote_key_1]
    t2_votes = st.session_state[vote_key_2]
    total = t1_votes + t2_votes
    pct1 = int(t1_votes / total * 100) if total else 0
    pct2 = 100 - pct1 if total else 0

    is_same_team = team1.strip().split()[0] == team2.strip().split()[0]

    # CARD UI
    html = build_card_html(
        title=title,
        team1=team1,
        players1=players1,
        team2=team2,
        players2=players2,
        team1_logo=TEAM_LOGOS.get(team1.strip().replace(" 🏆", "").replace(" 🦆", ""), "assets/tbd_logo.png"),
        team2_logo=TEAM_LOGOS.get(team2.strip().replace(" 🏆", "").replace(" 🦆", ""), "assets/tbd_logo.png"),
        team1_pct=pct1,
        team2_pct=pct2,
        has_voted=st.session_state[user_vote_key] is not None,
        voted_abbr=st.session_state[user_vote_key]
    )
    st.markdown(html, unsafe_allow_html=True)


    if (
        is_real_team(team1)
        and is_real_team(team2)
        and st.session_state[user_vote_key] is None
        and not is_same_team
    ):
        # Create centered buttons in a single row
        _, col1, _, col2,_, = st.columns([1, 10, 0.05, 10, 1], gap="small")
        with col1:
            if st.button(f"🙌 Support {abbr1}", key=button_key_1):
                st.session_state[vote_key_1] += 1
                st.session_state[user_vote_key] = abbr1
                st.rerun()
        with col2:
            if st.button(f"🙌 Support {abbr2}", key=button_key_2):
                st.session_state[vote_key_2] += 1
                st.session_state[user_vote_key] = abbr2
                st.rerun()
    elif is_same_team:
        st.markdown(
            "<div style='text-align:center; color:gray;'>📌 Voting not available for same-team matches</div>",
            unsafe_allow_html=True
        )
    # elif st.session_state[user_vote_key]:
    #     st.markdown(
    #         f"<div style='text-align:center; color:#388e3c; font-weight:600;'>✅ You supported: {st.session_state[user_vote_key]}</div>",
    #         unsafe_allow_html=True
    #     )
