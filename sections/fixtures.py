import streamlit as st
import pandas as pd
import base64, os
from pathlib import Path
from collections import defaultdict

from fixtures_modules.database_handler import (
    load_sheet_as_df,
    read_fixtures_sheet,
    write_fixtures_sheet
)
from fixtures_modules.tournament_logic import (
    build_group_stage_pairs,
    build_group_stage_matches,
    build_full_knockout_tree
)
from utils.ui_data import display_card
from fixtures_modules.constants import SPORT_LOGOS, SPORT_RULES, BONUS_CARDS, SEED_PATTERN

def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_sport_banner_and_rules(sport_name):

    load_global_styles()

    # image_path = "assets/fixtures_bg.png"
    # if os.path.exists(image_path):
    #     with open(image_path, "rb") as img_file:
    #         bg_img = base64.b64encode(img_file.read()).decode()

    #     st.markdown(
    #         f"""
    #         <style>
    #         .stApp {{
    #             background: url("data:image/jpg;base64,{bg_img}") no-repeat center center fixed !important;
    #             background-size: cover !important;
    #         }}
    #         </style>
    #         """,
    #         unsafe_allow_html=True,
    #     )

    """Render the banner, rules, and bonus cards for a sport."""

    # --- Banner ---
    logo_path = SPORT_LOGOS.get(sport_name)
    img_base64 = get_base64_image(logo_path) if logo_path else None

    if img_base64:
        st.markdown(
            f"""
            <div class="sport-banner">
                <img src="data:image/jpg;base64,{img_base64}" alt="{sport_name} banner">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"No banner image found for {sport_name}.")

    # --- Recursive Rules Renderer ---
    def render_rules_section(section, level=0):
        if isinstance(section, list):
            st.markdown(
                "<ul class='rules-list'>" + "".join([f"<li>{item}</li>" for item in section]) + "</ul>",
                unsafe_allow_html=True
            )
        elif isinstance(section, dict):
            for key, value in section.items():
                st.markdown(f"<div class='rule-section-title'>{key}</div>", unsafe_allow_html=True)
                render_rules_section(value, level + 1)

    # --- Rules Expander ---
    rules = SPORT_RULES.get(sport_name)
    if rules:
        with st.expander(f"📜 {sport_name} Rules"):
            st.markdown("<div class='rules-card'>", unsafe_allow_html=True)
            render_rules_section(rules)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No rules available for this sport.")


def render_bonus_cards(sport_name):
    """Render bonus cards for the given sport."""
    cards = BONUS_CARDS.get(sport_name, [])
    if cards:
        st.markdown("### 🎯 Bonus Cards")
        df = pd.DataFrame(cards)
        st.dataframe(df, use_container_width=True, hide_index=True)

# ---------- helpers ----------

def get_base64_image(image_path):
    img_bytes = Path(image_path).read_bytes()
    return base64.b64encode(img_bytes).decode()

def extract_team_and_players(team_str: str):
    """
    From "Team A\\nA & B" or "Winner Match 1\\nA & B / C & D" → ("Team A", ["A","B"...])
    Works for non-chess (pair-based) flows.
    """
    if not team_str or str(team_str).strip() == "":
        return "TBD", []
    parts = str(team_str).split("\n", 1)
    team_name = parts[0].strip()
    if len(parts) == 1:
        return team_name, []
    players_raw = parts[1].strip()
    if "/" in players_raw:
        all_players = []
        for pair in players_raw.split("/"):
            all_players.extend([p.strip() for p in pair.split("&")])
        return team_name, all_players
    else:
        return team_name, [p.strip() for p in players_raw.split("&")]

# ---------- generation ----------
def generate_and_store_fixtures(sport):

    # === Load & validate sheet ===
    df = load_sheet_as_df(sport)
    if df.empty:
        raise RuntimeError(f"Sheet for {sport} is empty or failed to load.")

    is_chess = sport.lower() == "chess"

    # === Normalize seeds ===
    df['seed'] = pd.to_numeric(df.get('seed', 0), errors='coerce').fillna(0).astype(int)

    if not is_chess:
        df['player_1'] = df.get('player_1', '').fillna('')
        df['player_2'] = df.get('player_2', '').fillna('')
        df['pair'] = df['player_1'] + " & " + df['player_2']

    # === Extract seeds ===
    seed1 = df[df['seed'] == 1]
    seed2 = df[df['seed'] == 2]
    seed3 = df[df['seed'] == 3]   # ✅ All seed3 go into group stage now

    seed3_winners = seed3
    target_pairs = 16 if is_chess else 8

    # === Build group stage ===
    group_pairs = build_group_stage_pairs(seed3_winners, is_chess, target_pairs)
    group_matches = build_group_stage_matches(group_pairs, df, sport, is_chess)
    n_group_matches = len(group_matches)

    # === Build knockout tree ===
    all_knockouts = build_full_knockout_tree(seed1, seed2, seed3, df, sport, is_chess)

    combined_fixtures = []

    # --- Group Stage ---
    for idx, m in enumerate(group_matches, start=1):
        if is_chess:
            player1 = df.loc[df["team_name"] == m[1], "player"].values[0] \
                if not df.loc[df["team_name"] == m[1]].empty else ""
            player2 = df.loc[df["team_name"] == m[2], "player"].values[0] \
                if not df.loc[df["team_name"] == m[2]].empty else ""

            combined_fixtures.extend([
                {"match_id": idx, "round": "Group Stage", "team": m["team 1"], "players": player1, "result": ""},
                {"match_id": idx, "round": "Group Stage", "team": m["team 2"], "players": player2, "result": ""}
            ])
        else:
            combined_fixtures.extend([
                {"match_id": idx, "round": "Group Stage", "team": m["team 1"], "players": " & ".join(m["players 1"]), "result": ""},
                {"match_id": idx, "round": "Group Stage", "team": m["team 2"], "players": " & ".join(m["players 2"]), "result": ""}
            ])

    # --- Knockouts ---
    start_id = n_group_matches + 1
    for round_name, matches in all_knockouts.items():
        for idx, m in enumerate(matches, start=start_id):

            # Helper: build team string with pairs
            def get_team_str(team_placeholder):
                team_rows = df[df['team_name'].str.strip().str.lower() == team_placeholder.strip().lower()]
                if not team_rows.empty and not is_chess:
                    pair = team_rows.iloc[0]['pair']
                    return f"{team_placeholder}\n{pair}"
                return team_placeholder

            # Apply SEED_PATTERN (swap sides if needed)
            seed_pattern = SEED_PATTERN.get(round_name, {})
            if idx in seed_pattern.get("Seed 1", []):
                # force seed1 to team1
                team1_str, team2_str = get_team_str(m[1]), get_team_str(m[2])
            elif idx in seed_pattern.get("Seed 2", []):
                # force seed2 to team1
                team1_str, team2_str = get_team_str(m[2]), get_team_str(m[1])
            else:
                # default order
                team1_str, team2_str = get_team_str(m[1]), get_team_str(m[2])


            if is_chess:
                player1 = df.loc[df["team_name"] == m[1], "player"].values[0] \
                    if not df.loc[df["team_name"] == m[1]].empty else ""
                player2 = df.loc[df["team_name"] == m[2], "player"].values[0] \
                    if not df.loc[df["team_name"] == m[2]].empty else ""

                combined_fixtures.extend([
                    {"match_id": idx, "round": round_name, "team": team1_str, "players": player1, "result": ""},
                    {"match_id": idx, "round": round_name, "team": team2_str, "players": player2, "result": ""}
                ])
            else:
                team1, players1_list = extract_team_and_players(team1_str)
                team2, players2_list = extract_team_and_players(team2_str)

                combined_fixtures.extend([
                    {"match_id": idx, "round": round_name, "team": team1, "players": " & ".join(players1_list), "result": ""},
                    {"match_id": idx, "round": round_name, "team": team2, "players": " & ".join(players2_list), "result": ""}
                ])

        start_id += len(matches)

    # === Save fixtures to sheet ===
    fixtures_df = pd.DataFrame(combined_fixtures)

    if is_chess:
        ROUND_ORDER = ["Group Stage", "Super 32", "Super 16", "Quarter Final", "Semi Final", "Final"]
    else:
        ROUND_ORDER = ["Group Stage", "Super 16", "Quarter Final", "Semi Final", "Final"]

    fixtures_df['round'] = pd.Categorical(fixtures_df['round'], categories=ROUND_ORDER, ordered=True)
    fixtures_df = fixtures_df.sort_values(['round', 'match_id']).reset_index(drop=True)

    write_fixtures_sheet(sport, fixtures_df)

    return df, group_matches, all_knockouts


def render_fixtures_for_sport(sport):
    
    st.markdown(
    f"""
    <h2 style="
        text-align:center;
        font-size:32px;
        margin: 16px 0;
        padding: 14px 22px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        font-weight: 900;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    ">
        <span style="
            font-size: 36px;
            margin-right: 8px;
            background: linear-gradient(45deg, #FFD700, #FFA500, #FF4500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        ">🏆</span>
        Fixtures for {sport}
    </h2>
    """,
    unsafe_allow_html=True
)


    st.markdown("----")

    # Read fresh data from sheet
    df = read_fixtures_sheet(sport)
    if df is None or df.empty:
        st.warning(f"⚠ Sheet for {sport} is missing or empty.")
        return

    # Detect if this is chess (single-player per row)
    is_chess = sport.lower() == "chess"

    # Group rows by (match_id, round)
    matches_grouped = defaultdict(list)
    for _, row in df.iterrows():
        matches_grouped[(row["match_id"], row["round"])].append(row)

    group_matches = []
    all_knockouts = defaultdict(list)

    for (match_id, round_name), rows in matches_grouped.items():
        # Ensure exactly 2 rows
        while len(rows) < 2:
            rows.append({
                "team": "TBD",
                "players": "" if not is_chess else "TBD",
                "result": "",
                "match_id": match_id,
                "round": round_name
            })

        row1, row2 = rows[0], rows[1]

        # Handle chess vs other sports
        if is_chess:
            players1 = [row1.get("players", row1.get("player", ""))]
            players2 = [row2.get("players", row2.get("player", ""))]
        else:
            players1 = row1.get("players", "").split(" & ") if row1.get("players") else []
            players2 = row2.get("players", "").split(" & ") if row2.get("players") else []

        match_data = {
            "team 1": row1.get("team", "TBD"),
            "players 1": players1,
            "result 1": row1.get("result", ""),
            "team 2": row2.get("team", "TBD"),
            "players 2": players2,
            "result 2": row2.get("result", ""),
            "match_id": int(match_id),
            "round": round_name
        }

        if "group" in round_name.lower():
            group_matches.append(match_data)
        else:
            all_knockouts[round_name].append(match_data)

    # --- Render Group Matches ---
    st.markdown(
    """
    <div style="
        text-align:left;
        display:inline-block;
        font-size:22px;
        margin: 12px 0;
        padding: 8px 16px;
        border-radius: 50px;
        background: rgba(0, 114, 255, 0.1);
        color: #0072ff;
        font-weight: 700;
        letter-spacing: 0.5px;
    ">
        📦 Group Stage Matches
    </div>
    """,
    unsafe_allow_html=True
)

    if not group_matches:
        st.info("No group matches available yet.")
    else:
        for i in range(0, len(group_matches), 2):
            cols = st.columns(2)
            with cols[0]:
                m = group_matches[i]
                display_card(
                    f"Match {m['match_id']}",
                    m["team 1"], m["players 1"],
                    m["team 2"], m["players 2"],
                    match_id=m["match_id"],
                    round_name=m["round"],
                    card_index=i,
                    result1=m.get("result 1", ""),
                    result2=m.get("result 2", "")
                )
            if i + 1 < len(group_matches):
                with cols[1]:
                    m = group_matches[i + 1]
                    display_card(
                        f"Match {m['match_id']}",
                        m["team 1"], m["players 1"],
                        m["team 2"], m["players 2"],
                        match_id=m["match_id"],
                        round_name=m["round"],
                        card_index=i + 1,
                        result1=m.get("result 1", ""),
                        result2=m.get("result 2", "")
                    )

    st.markdown("----")

    # --- Render Knockouts ---
    st.markdown(
    """
    <div style="
        text-align:left;
        display:inline-block;
        font-size:22px;
        margin: 12px 0;
        padding: 8px 16px;
        border-radius: 50px;
        background: rgba(0, 114, 255, 0.1);
        color: #0072ff;
        font-weight: 700;
        letter-spacing: 0.5px;
    ">
        👊 Knockout Matches
    </div>
    """,
    unsafe_allow_html=True
)
    for round_name, matches in all_knockouts.items():
        st.markdown("----")
        st.markdown(
    f"""
    <div style="
        text-align:center;
        font-size:28px;
        margin: 12px 0;
        padding: 10px 20px;
        border-radius: 50px;
        background: #111;
        color: #0ff;
        font-weight: 800;
        text-shadow: 0 0 10px #0ff, 0 0 20px #0ff;
        box-shadow: 0 0 15px #0ff;
    ">
        {round_name}
    </div>
    """,
    unsafe_allow_html=True,
)



        st.markdown("----")
        if not matches:
            st.info("No matches available yet.")
            continue

        for i in range(0, len(matches), 2):
            cols = st.columns(2)
            with cols[0]:
                m = matches[i]
                display_card(
                    f"Match {m['match_id']}",
                    m["team 1"], m["players 1"],
                    m["team 2"], m["players 2"],
                    match_id=m["match_id"],
                    round_name=round_name,
                    card_index=i,
                    result1=m.get("result 1", ""),
                    result2=m.get("result 2", "")
                )
            if i + 1 < len(matches):
                with cols[1]:
                    m = matches[i + 1]
                    display_card(
                        f"Match {m['match_id']}",
                        m["team 1"], m["players 1"],
                        m["team 2"], m["players 2"],
                        match_id=m["match_id"],
                        round_name=round_name,
                        card_index=i + 1,
                        result1=m.get("result 1", ""),
                        result2=m.get("result 2", "")
                    )
