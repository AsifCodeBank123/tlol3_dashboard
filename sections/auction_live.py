# TLOL_Dash/sections/auction_live.py

import streamlit as st
import pandas as pd
import random
import time
from modules.data_loader import load_and_merge_scores
from modules.avatar_utils import get_avatar_url
from modules.constants import TLOL_SPORTS

def render():
    BASE_PRICES = {"Icon": 200, "Lead": 100, "Rest": 50}
    TEAM_NAMES = ["Team Jay", "Team Blessen", "Team Lalit", "Team Somansh"]
    TEAM_BUDGET = 10000
    MAX_TEAM_SIZE = 14
    MAX_ICON_COUNT = 1
    COUNTDOWN_DURATION = 60

    # CSS Styling
    st.markdown("""
        <style>
            .auction-container {
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                gap: 30px;
            }
            .player-card {
                background-color: #fff4e6;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
                width: 100%;
                color: #000;
                text-align: center;
            }
            .player-card h3 {
                margin-bottom: 10px;
                color: #000;
            }
            .player-details {
                font-size: 15px;
                margin-top: 10px;
                line-height: 1.6;
                color: #000;
            }
            .controls-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-top: 16px;
            }
            .button-row {
                display: flex;
                justify-content: center;
                gap: 16px;
                margin-top: 10px;
            }
            .team-grid {
                display: flex;
                flex-direction: column;
                gap: 12px;
                font-size: 13px;
                color: #000;
            }
            .team-box {
                border: 1px dashed #ccc;
                border-radius: 8px;
                padding: 10px;
                background: #fdfdfd;
                color: #000;
            }
            .timer-box {
                font-size: 14px;
                font-weight: bold;
                color: #d72638;
                margin-top: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("🔄 Reset Auction"):
        for key in ["auction_index", "auction_initialized", "auction_results", "team_budgets", "auction_queue", "skipped_players", "start_time"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Auction has been reset.")
        st.rerun()

    if "auction_index" not in st.session_state:
        st.session_state.auction_index = 0
    if "auction_initialized" not in st.session_state:
        st.session_state.auction_initialized = False
    if "auction_results" not in st.session_state:
        st.session_state.auction_results = {team: [] for team in TEAM_NAMES}
    if "team_budgets" not in st.session_state:
        st.session_state.team_budgets = {team: TEAM_BUDGET for team in TEAM_NAMES}
    if "skipped_players" not in st.session_state:
        st.session_state.skipped_players = []
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    st.title("🎥 Live Auction Panel")

    if not st.session_state.auction_initialized:
        df_all = load_and_merge_scores("reports")
        df_all.columns = df_all.columns.str.strip()
        df_all["Tier"] = df_all["TLOL Auction Player Type"].astype(str).str.strip().str.capitalize()
        df_all = df_all[df_all["Tier"].isin(["Icon", "Lead", "Rest"])]
        df_all["Total Score"] = df_all[[col for col in df_all.columns if col in TLOL_SPORTS]].sum(axis=1)

        tier_order = {"Icon": 0, "Lead": 1, "Rest": 2}
        df_all["TierOrder"] = df_all["Tier"].map(tier_order)
        df_all = df_all.sort_values(by=["TierOrder", "Total Score"], ascending=[True, False])
        grouped = df_all.groupby("Tier")

        auction_list = []
        for tier in ["Icon", "Lead", "Rest"]:
            if tier in grouped.groups:
                players = grouped.get_group(tier).to_dict("records")
                random.shuffle(players)
                auction_list.extend(players)

        st.session_state.auction_queue = auction_list
        st.session_state.auction_initialized = True
        st.rerun()
        return

    full_queue = st.session_state.auction_queue + st.session_state.skipped_players

    if st.session_state.auction_index >= len(full_queue):
        st.success("🎉 Auction Complete!")
        if st.button("📥 Export Results as CSV"):
            all_rows = []
            for team, players in st.session_state.auction_results.items():
                for player in players:
                    all_rows.append({"Team": team, **player})
            df_out = pd.DataFrame(all_rows)
            st.download_button("Download CSV", df_out.to_csv(index=False), "TLOL3_Auction_Results.csv")
        return

    player = full_queue[st.session_state.auction_index]
    base_price = BASE_PRICES.get(player["Tier"], 50)

    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        st.markdown("<div class='auction-container'>", unsafe_allow_html=True)

        top_sports = sorted([(sport, player.get(sport, 0)) for sport in TLOL_SPORTS], key=lambda x: -x[1])
        top_skills = ", ".join([s[0] for s in top_sports if s[1] > 0][:2]) or "N/A"

        st.markdown(f"""
        <div class='player-card'>
            <h3>👤 {player['Player']} ({player['Tier']})</h3>
            <img src='{get_avatar_url(player['Player'], player['Gender'])}' width='90' style='border-radius:50%; margin:10px 0;'>
            <div class='player-details'>
                🔢 <b>Total Score:</b> {int(player['Total Score'])}<br>
                💰 <b>Base Price:</b> ${base_price}<br>
                🧍 <b>Gender:</b> {player['Gender']}<br>
                🟢 <b>Availability:</b> {player.get("TLOL Availability", "")}<br>
                🏅 <b>Expertise:</b> {top_skills}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='controls-wrapper'>", unsafe_allow_html=True)
        selected_team = st.radio("Assign to Team:", TEAM_NAMES, key=f"team_{st.session_state.auction_index}", horizontal=True)

        bid_price = None  # Define default

        if st.session_state.team_budgets[selected_team] >= base_price:
            bid_price = st.number_input(
                "💵 Enter Bid Price",
                min_value=base_price,
                max_value=st.session_state.team_budgets[selected_team],
                step=10,
                value=base_price,
                key=f"bid_{st.session_state.auction_index}"
            )
        else:
            st.error(f"{selected_team} does not have enough budget (${st.session_state.team_budgets[selected_team]}) to bid on this player.")

        remaining_time = COUNTDOWN_DURATION - int(time.time() - st.session_state.start_time)
        if remaining_time < 0:
            remaining_time = 0

        st.markdown("<div class='button-row'>", unsafe_allow_html=True)
        #elapsed = int(time.time() - st.session_state.start_time)
        st.markdown(f"<div class='timer-box'>⏱️ Time: {remaining_time} seconds</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("💰 Sold", key=f"sold_{st.session_state.auction_index}"):
                team_players = st.session_state.auction_results[selected_team]
                icon_count = sum(1 for p in team_players if p["Tier"] == "Icon")
                female_count = sum(1 for p in team_players if p["Gender"] == "F")
                if len(team_players) >= MAX_TEAM_SIZE:
                    st.warning(f"{selected_team} already has {MAX_TEAM_SIZE} players.")
                elif player["Tier"] == "Icon" and icon_count >= MAX_ICON_COUNT:
                    st.warning(f"{selected_team} already has an Icon player.")
                else:
                    st.session_state.auction_results[selected_team].append({
                        "Player": player["Player"],
                        "Tier": player["Tier"],
                        "Bid Price": bid_price,
                        "Total Score": int(player["Total Score"]),
                        "Gender": player["Gender"]
                    })
                    st.session_state.team_budgets[selected_team] -= bid_price
                    st.session_state.auction_index += 1
                    st.session_state.start_time = time.time()
                    st.rerun()

        with col_b:
            if st.button("⏭️ Skip", key=f"skip_{st.session_state.auction_index}"):
                st.session_state.skipped_players.append(player)
                st.session_state.auction_index += 1
                st.session_state.start_time = time.time()
                st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

        # with st.expander("📊 Player Score Breakdown"):
        #     for sport in TLOL_SPORTS:
        #         if sport in player and player[sport] > 0:
        #             st.markdown(f"- **{sport}**: {int(player[sport])} pts")

    with col_right:
        st.markdown("### 📋 Teams & Budgets")

        # Summary above team boxes
        total_players = len(st.session_state.auction_queue + st.session_state.skipped_players)
        sold_players = sum(len(p) for p in st.session_state.auction_results.values())
        remaining_players = total_players - sold_players
        st.markdown(f"<div class='summary-box'>👥 Players Left: {remaining_players} | ✅ Sold: {sold_players}</div>", unsafe_allow_html=True)

        st.markdown("<div class='team-grid'>", unsafe_allow_html=True)
        for team in TEAM_NAMES:
            players = st.session_state.auction_results[team]
            icon_count = sum(1 for p in players if p["Tier"] == "Icon")
            female_count = sum(1 for p in players if p["Gender"] == "F")
            unmet_notes = []
            if icon_count == 0:
                unmet_notes.append("🚫 Icon Missing")
            if female_count == 0:
                unmet_notes.append("❗ No Female")
            unmet_text = "<br>" + "<br>".join(unmet_notes) if unmet_notes else ""
            st.markdown(f"""
                <div class='team-box'>
                    <b>{team}</b><br>
                    💰 ${st.session_state.team_budgets[team]}<br>
                    {'<br>'.join(f'- {p["Player"]} (${p["Bid Price"]})' for p in players)}{unmet_text}
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)