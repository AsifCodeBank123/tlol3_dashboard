import streamlit as st
import os
import pandas as pd
import base64
from utils.constants import ticker_messages, winners_by_sport_stage, wall_of_fame, players_by_sport
from fixtures_modules.constants import sports_schedule
import random

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
    <div style="text-align: center; margin-top: -50px; margin-bottom: 3px;">
        <a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FAsifCodeBank123%2Ftlol3_dashboard">
            <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FAsifCodeBank123%2Ftlol3_dashboard&label=LEGENDS%20VISITED&countColor=%23263759" />
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

    # Join into one scrolling string
    ticker_text = "  ".join(ticker_messages)

    st.markdown(f"""<div class="live-ticker"><span>{ticker_text}</span><span>{ticker_text}</span></div>""", unsafe_allow_html=True)

    ## Top-right button
    col1, col2 = st.columns([0.85, 0.15])

    with col2:
        if st.button("📊 Leaderboard is Live", key="leaderboard_live"):
            if st.session_state.get("active_section") != "Kismein Kitna Hai Dum (Leaderboard)":
                st.session_state.active_section = "Kismein Kitna Hai Dum (Leaderboard)"
                st.rerun()

        # inline style override
    st.markdown("""
        <style>
        :root .stApp .block-container .stButton > button {
        background: linear-gradient(135deg, #ffcc00, #ffe071) !important;
        color: #0b1220 !important;
        font-weight: 900 !important;
        font-size: 15px !important;
        border: none !important;
        border-radius: 999px !important;   /* capsule */
        padding: 10px 22px !important;
        white-space: nowrap !important;
        cursor: pointer !important;
        margin: 10px auto auto 0px;   /* <-- push -40px left */

        box-shadow: 0 6px 14px rgba(0,0,0,0.4) !important;
        transition: transform .2s ease, box-shadow .2s ease !important;

        animation: leaderboard-pulse 2.5s infinite;
        }

        :root .stApp .block-container .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px rgba(255,204,0,0.75),
                    0 0 12px rgba(255,204,0,0.4);
        }

        :root .stApp .block-container .stButton > button:active {
        transform: translateY(0) scale(0.96);
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        }

        @keyframes leaderboard-pulse {
        0%   { box-shadow: 0 0 0 rgba(255,204,0,0.35); }
        50%  { box-shadow: 0 0 20px rgba(255,204,0,0.85); }
        100% { box-shadow: 0 0 0 rgba(255,204,0,0.35); }
        }
        </style>
        """, unsafe_allow_html=True)


    # Title
    st.markdown("""
        <div style='text-align:center; padding-top: 10px;'>
            <h1 class="main-title">
            🎬 TCOE League of Legends <span class="season-number">3</span>
            </h1>
            <!--
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

    st.markdown("<div class='winners-title'>🌟 Wall of Fame</div>", unsafe_allow_html=True)
    st.markdown(
    """
    <p style='text-align:center;
              font-size:30px;
              font-style:italic;
              color:#ffcc00;
              margin-top:-6px;
              margin-bottom:14px;
              text-shadow:0 1px 3px rgba(0,0,0,0.6);'>
        Are you the next?
    </p>
    """,
    unsafe_allow_html=True
)

    card_chunks = []
    for sport, wof in wall_of_fame.items():
        # image
        wof_img_b64 = ""
        img_path = wof.get("image")
        if img_path and os.path.exists(img_path):
            wof_img_b64 = get_base64_image(img_path)

        # cricket shows team, others show winner
        is_cricket = sport.lower() == "cricket"
        if is_cricket:
            main_line = (wof.get("team") or "TBD").strip()
            sub_line = "Final • Team Champion"
        else:
            main_line = (wof.get("winner") or "TBD").strip()
            sub_line = f"Final • {wof.get('team')}" if wof.get("team") else "Final"

        bg_style = f'style="background-image:url({wof_img_b64});"' if wof_img_b64 else ""

        # ⬇️ no leading spaces/newlines
        card_chunks.append(
            f'<div class="wof-card">'
            f'  <div class="wof-bg" {bg_style}></div>'
            f'  <div class="wof-overlay"></div>'
            f'  <div class="wof-content">'
            f'    <div class="wof-sport-label">{sport}</div>'
            f'    <div class="wof-title">{wof.get("title","🏅 Champion")}</div>'
            f'    <div class="wof-line-main">{main_line}</div>'
            f'    <div class="wof-line-sub">{sub_line}</div>'
            f'  </div>'
            f'</div>'
        )

    gallery_html = '<div class="wof-gallery">' + "".join(card_chunks) + '</div>'
    st.markdown(gallery_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close winners-section

    #st.markdown("<hr style='border-color:#ffcc00;'>", unsafe_allow_html=True)


    # ===== Sports & Stage-wise Winners (NEW – right after Title) =====
    st.markdown("<div class='winners-section'>", unsafe_allow_html=True)
    st.markdown("<div class='winners-title'>🏅 Live Winners • Sport & Stage-wise</div>", unsafe_allow_html=True)

    # Tabs per sport
    sport_names = list(winners_by_sport_stage.keys())
    if sport_names:
        tabs = st.tabs([f"💪 {name}" for name in sport_names])
        for tab, sport in zip(tabs, sport_names):
            with tab:

                players = players_by_sport.get(sport, [])

                with st.expander(f"👥 {sport} Players/Pairs ({len(players)})", expanded=False):
                    # randomize order every time page refreshes
                    players_random = random.sample(players, len(players))

                    # --- Build team-wise summary ---
                    summary_counts = {}
                    for p in players_random:
                        team = (p.get("team") or "").strip()
                        raw_status = (p.get("status") or "not_played").strip().lower()
                        if team not in summary_counts:
                            summary_counts[team] = {"alive": 0, "eliminated": 0, "not_played": 0}
                        if raw_status == "alive":
                            summary_counts[team]["alive"] += 1
                        elif raw_status in ("eliminated", "elimination", "out"):
                            summary_counts[team]["eliminated"] += 1
                        else:
                            summary_counts[team]["not_played"] += 1

                    # totals across all teams
                    total_alive_all = sum(t["alive"] for t in summary_counts.values())

                    # render summary in a 2-column grid (with left-col + count-row)
                    summary_html = "<div class='team-summary-grid'>"
                    for team, counts in summary_counts.items():

                        if total_alive_all > 0:
                            win_chances = round((counts['alive'] / total_alive_all) * 100, 1)
                        else:
                            win_chances = 0

                        # optional color class for win-box
                        if win_chances >= 40:
                            win_class = "win-good"   # green
                        elif win_chances >= 20:
                            win_class = "win-mid"    # yellow
                        else:
                            win_class = "win-low"    # red

                        summary_html += (
                            "<div class='team-pill'>"
                            "<div class='left-col'>"
                                f"<b>{team}</b>"
                                "<div class='count-row'>"
                                f"<span class='count-pill count-alive'>Alive: {counts['alive']}</span>"
                                f"<span class='count-pill count-eliminated'>Out: {counts['eliminated']}</span>"
                                f"<span class='count-pill count-notplayed'>Not Played: {counts['not_played']}</span>"
                                "</div>"
                            "</div>"
                            f"<div class='win-box {win_class}'><span class='label'>Winning Chances</span><span class='value'>{win_chances}%</span></div>"
                            "</div>"
                        )
                    summary_html += "</div>"
                    st.markdown(summary_html, unsafe_allow_html=True)



                    st.markdown("<hr style='border-color:#ffcc00;'>", unsafe_allow_html=True)

                    # --- Build player boxes ---
                    box_chunks = []
                    for p in players_random:
                        name = (p.get("name") or "").strip()
                        team = (p.get("team") or "").strip()
                        raw_status = (p.get("status") or "not_played").strip().lower()

                        if raw_status == "alive":
                            status_class = "alive"; status_text = "Alive ✅"
                        elif raw_status in ("eliminated", "elimination", "out"):
                            status_class = "eliminated"; status_text = "Eliminated ❌"
                        else:
                            status_class = "not_played"; status_text = "Not Played"

                        box_chunks.append(
                            f'<div class="player-box {status_class}">'
                            f'  <div class="player-name">{name}</div>'
                            f'  <div class="player-team">{team}</div>'
                            f'  <div class="player-status {status_class}">{status_text}</div>'
                            f'</div>'
                        )

                    grid_html = '<div class="player-grid">' + "".join(box_chunks) + '</div>'
                    st.markdown(grid_html, unsafe_allow_html=True)


                stages = winners_by_sport_stage.get(sport, {})
                for stage_name, results in stages.items():
                    if not results:
                        continue

                    # each stage inside its own expander
                    with st.expander(f"🎯 {stage_name}", expanded=False):   # set expanded=False if you want them collapsed by default
                        st.markdown("<div class='stage-block'>", unsafe_allow_html=True)
                        #st.markdown(f"<div class='stage-title'>🎯 {stage_name}</div>", unsafe_allow_html=True)
                        
                        # Clean results and sort by match number if present
                        def extract_match_no(match_str):
                            try:
                                # get digits from string like "Match 12"
                                return int("".join(ch for ch in match_str if ch.isdigit()))
                            except Exception:
                                return 9999  # push non-numeric matches to end

                        # sort results by match number
                        sorted_results = sorted(results, key=lambda r: extract_match_no(r.get("match", "")))

                        card_chunks = []
                        for rec in sorted_results:
                            match = rec.get("match", "")
                            winner = rec.get("winner", "")
                            team = rec.get("team", "")

                            card_chunks.append(
                                f'<div class="winner-card">'
                                f'  <div class="winner-topline">🏆 {sport} • {match}</div>'
                                f'  <div class="winner-name">{winner}</div>'
                                f'  <div class="badge-team">{team}</div>'
                                f'</div>'
                            )

                        grid_html = '<div class="winners-grid">' + "".join(card_chunks) + '</div>'
                        st.markdown(grid_html, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)  # close stage-block


    else:
        st.info("No winners to show yet. Keep an eye on this space!")

    st.markdown("</div>", unsafe_allow_html=True)  # close winners-section
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
