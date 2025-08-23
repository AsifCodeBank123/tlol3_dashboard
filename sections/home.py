import streamlit as st
import os
import pandas as pd
import base64
import html
import math
from fixtures_modules.constants import sports_schedule

def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

def render():
    load_global_styles()

    # Background
    image_path = "assets/sports_bg2.jpg"
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

    st.markdown(
    """
    <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FAsifCodeBank123%2Ftlol3_dashboard">
            <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FAsifCodeBank123%2Ftlol3_dashboard&label=LEGENDS%20VISITED&countColor=%23263759" />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

    # Ticker messages
    ticker_messages = [
    "🏆 4 Teams • 7 Games • 1 Trophy – The Clash of Legends Begins! 🔥",
    "⚔️ Agni Pariksha of Skills – Only the Bold Will Rule the Field!",
    "🔥 Yeh Sirf Game Nahi, Yeh Hai Office ka MahaKumbh!",
    "⏳ Countdown Begins – 4 Teams, 7 Games, Sirf Ek Champion!",
    "🎯 Clash of Legends – Jeetega Wahi Jo Dega Sabse Zyada!",
    "💥 7 Games, 4 Teams, 1 Trophy – Baazi Lagao, Dil Jeeto!",
    "🚀 Agni Pariksha Mode: ON – Time to Prove Your Mettle!",
    "🌟 Legends Aren’t Born, They’re Made on the Battlefield!",
    "⚡ Har Game Ek Jung – 7 Chances to Become a Legend!",
    "🎭 Drama, Action & Glory – Office Sports ka Blockbuster!",
    "🔥 4 Teams in a Battle Royale – Only One Will Lift the Trophy!",
    "💪 7 Games of Pure Skill – Agni Pariksha Shuru!",
    "🎯 Apni Team ko Banaye Legend – 4 Teams, Ek Sapna!",
    "🏆 7 Rounds • 4 Teams • 1 Champion – Are You Ready?",
    "⚔️ The Countdown Ends When Legends Rise!",
    "🔥 Yeh Trophy Har Kisi ke Bas ki Baat Nahi!",
    "🚀 Sirf Ek Trophy – Lekin 4 Teams Ki Khwahish Ek Jaise!",
    "🌟 The Clash of Legends: Where Heroes Are Forged!",
    "💥 Ab Khel Mein Hoga Sirf Action, No Distraction!",
    "⚡ 4 Teams ka Sapna, 7 Games ka Safar, 1 Office Champion!"
]

    # Join into one scrolling string
    ticker_text = "  ".join(ticker_messages)

    st.markdown(f"""<div class="live-ticker"><span>{ticker_text}</span><span>{ticker_text}</span></div>""", unsafe_allow_html=True)


    ## Top-right button
    col1, col2 = st.columns([0.85, 0.15])
    with col2:
        st.markdown('<div class="leaderboard-button">', unsafe_allow_html=True)
        if st.button("📊 Leaderboard is Live", key="leaderboard_live"):
            st.session_state.active_section = "Kismein Kitna Hai Dum (Leaderboard)"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


    # Title
    st.markdown("""
        <div style='text-align:center; padding-top: 10px;'>
            <h1 style='
                font-family: "Impact", "Copperplate", sans-serif;
                font-size: 64px;
                color: #ffcc00;
                text-shadow: 3px 3px 5px #000;
                letter-spacing: 2px;'>
                🎬 TCOE League of Legends 3
            </h1>
            <!--
            <marquee scrollamount="8" direction="left" style='
                font-family: "Dancing Script","Great Vibes",cursive;
                font-size: 22px;
                color: #fffbe7;
                background: rgba(0,0,0,0.45);
                border-radius:14px;
                padding: 8px 0; 
                margin-bottom:8px;
                letter-spacing: 1.5px;
                width:98%; display: block; margin-left:auto; margin-right:auto;'>
                💥 Breaking: Welcome to TCOE League of Legends Season 3! Prepare for epic showdowns, iconic players & bollywood drama. Stay tuned for daily updates & team rankings! 🔥
            </marquee> -->
            <p style='
                font-family: "Brush Script MT", cursive;
                font-size: 28px;
                color: #fff;
                text-shadow: 2px 2px 4px #000;
                margin-top: -2px;'>
                "Lights,Camera,Dhamaal – Ab hoga asli bawaal!"
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#ffcc00;'>", unsafe_allow_html=True)

    # --- Hamare Kaptaans ---
    st.markdown("<div class='shared-section-title'>👨‍✈ Hamare Kaptaans</div>", unsafe_allow_html=True)

    captains = [
        {"team": "Gully Gang", "captain": "Jay Jagad", "img": "assets/gg_logo.png"},
        {"team": "Badshah Blasters", "captain": "Somansh Datta", "img": "assets/bb_logo.png"},
        {"team": "Rockstar Rebels", "captain": "Blessen Thomas", "img": "assets/rr_logo.png"},
        {"team": "Dabangg Dynamos", "captain": "Lalit Chavan", "img": "assets/dd_logo.png"},
    ]

    cols = st.columns(len(captains))
    for i, cap in enumerate(captains):
        with cols[i]:
            img_base64 = get_base64_image(cap["img"])
            st.markdown(f"""
            <div class='captain-card'>
                <img src="{img_base64}" alt="Captain Photo"/>
                <div class='captain-name'>{cap['captain']}</div>
                
          
            </div>
            """, unsafe_allow_html=True)
    


    # --- Section Divider ---
    st.markdown("<hr style='border-color:#ffcc00;'>", unsafe_allow_html=True)

    # --- Title ---
    st.markdown("<div class='shared-section-title'>👥 Teams at a Glance</div>", unsafe_allow_html=True)

    # --- Load and Clean Data ---
    df_teams = pd.read_csv("reports/teams.csv")
    df_teams.columns = df_teams.columns.str.strip()
    df_teams.rename(columns={"Player Name": "Player", "Player Type": "Role"}, inplace=True)
    df_teams["Role"] = (
        df_teams["Role"].astype(str).str.strip().str.lower().map({
            "icon": "Icon", "lead": "Lead", "rest": "Rest"
        }).fillna("Rest")
    )

    # --- Custom Team Order and Role Order ---
    team_order = ["Gully Gang", "Badshah Blasters", "Rockstar Rebels", "Dabangg Dynamos"]
    role_order = ["Icon", "Lead", "Rest"]

    # --- CSS Class Maps & Emojis ---
    role_class_map = {
        "Icon": "role-icon",
        "Lead": "role-lead",
        "Rest": "role-rest",
    }
    role_emojis = {
        "Icon": "🌟",
        "Lead": "🧠",
        "Rest": "👤",
    }

    # --- Build UI ---
    for team in team_order:
        team_df = df_teams[df_teams["Team Name"] == team]

        # Team Summary
        total_players = len(team_df[team_df["Player"].str.lower() != "captain"])
        total_spend = pd.to_numeric(team_df["Bid Price"], errors="coerce").fillna(0).sum()

        if "Underdog" in team_df.columns:
            underdog_count = (team_df["Underdog"].astype(str).str.upper() == "Y").sum()
        else:
            underdog_count = 0


        with st.expander(f"🏀 {team}", expanded=(team == team_order[0])):
            # --- Summary Bar ---
            summary_html = f"""
            <div class='team-summary'>
                <span>👥 Players: <b>{total_players}</b></span>
                <span>💰 Total Spend: <b>${int(total_spend)}</b></span>
                <span>🔥 Underdogs: <b>{underdog_count}</b></span>
            </div>
            """
            st.markdown(summary_html, unsafe_allow_html=True)

            # --- Role-wise Players ---
            for role in role_order:
                role_players = team_df[team_df["Role"] == role]
                if role_players.empty:
                    continue

                role_class = role_class_map.get(role, "role-rest")
                emoji = role_emojis.get(role, "")

                # Build pills
                pills_html_parts = []
                for _, row in role_players.iterrows():
                    player = str(row.get("Player", "")).strip()
                    if not player or player.lower() == "captain":
                        continue

                    bid_price = row.get("Bid Price", None)
                    underdog = str(row.get("Underdog", "")).strip().upper()

                    # Price
                    price_html = ""
                    if pd.notna(bid_price) and str(bid_price).strip() != "":
                        try:
                            price_html = f"<span class='bid-price'>${int(float(bid_price))}</span>"
                        except Exception:
                            price_html = f"<span class='bid-price'>${str(bid_price)}</span>"

                    # Underdog badge
                    underdog_html = "<span class='underdog-badge'>Underdog</span>" if underdog == "Y" else ""

                    pills_html_parts.append(
                        f"<span class='player-pill'>{player} {price_html} {underdog_html}</span>"
                    )

                # Render role section
                if pills_html_parts:
                    section_html = (
                        f"<div class='role-block {role_class}'>"
                        f"<div class='section-title'>{emoji} {role}</div>"
                        + "".join(pills_html_parts) +
                        "</div>"
                    )
                    st.markdown(section_html, unsafe_allow_html=True)

    # --- Section Divider ---
    st.markdown("<hr style='border-color:#ffcc00;'>", unsafe_allow_html=True)
    
    # Sports Schedule Section
    
    # Title
    st.markdown("<div class='shared-section-title'>📅 Upcoming Sports Schedule</h2>", unsafe_allow_html=True)

    # Convert dict to list for easy slicing
    sports_items = list(sports_schedule.items())

    # First row: 3 cards
    first_row = sports_items[:3]
    # Second row: remaining cards
    second_row = sports_items[3:]

    # Function to render cards
    def render_sport_cards(items):
        cols = st.columns(len(items))
        for col, (sport_name, schedule_list) in zip(cols, items):
            if not schedule_list:
                continue
            sport = schedule_list[0]
            with col:
                st.markdown(f"""
                <div class='sport-card'>
                    <div class='sport-header'>
                        <img src="{sport['icon']}" alt="{sport['name']} icon">
                        <h3>{sport['name']}</h3>
                    </div>
                    <p><strong>Type:</strong> {sport['type']}</p>
                    <p><strong>Location:</strong> {sport['location']}</p>
                    <p><strong>Format:</strong> {sport['format']}</p>
                    <p><strong>From:</strong> {sport['from']}</p>
                    <p><strong>To:</strong> {sport['to']}</p>
                    <p><strong>Event Head:</strong> {sport['event_head']}</p>
                    <p><strong>Coordinator:</strong> {sport['event_coord']}</p>
                </div>
                """, unsafe_allow_html=True)

    # Render first row (3 cards)
    render_sport_cards(first_row)

    # Add spacing between rows
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Render second row (remaining cards)
    render_sport_cards(second_row)
