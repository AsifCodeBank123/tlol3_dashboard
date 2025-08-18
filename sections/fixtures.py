import streamlit as st
import pandas as pd
import base64
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
from fixtures_modules.constants import SPORT_LOGOS, SPORT_RULES, BONUS_CARDS

def render_sport_banner_and_rules(sport_name):
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
    """
    Generate fixtures for `sport`, save to Google Sheet, and return
    (df, group_matches, all_knockouts) in multi-row-per-match format.
    Seeds 1 & 2 are placed directly in Super 16 with their players known.
    Placeholders for group winners are shown when unknown.
    """
    df = load_sheet_as_df(sport)
    if df.empty:
        raise RuntimeError(f"Sheet for {sport} is empty or failed to load.")

    is_chess = sport.lower() == "chess"

    # Normalize seeds and player names
    df['seed'] = pd.to_numeric(df.get('seed', 0), errors='coerce').fillna(0).astype(int)
    if not is_chess:
        df['player_1'] = df.get('player_1', '').fillna('')
        df['player_2'] = df.get('player_2', '').fillna('')
        df['pair'] = df['player_1'].astype(str) + " & " + df['player_2'].astype(str)

    # Extract seeds
    seed1 = df[df['seed'] == 1]
    seed2 = df[df['seed'] == 2]
    seed3 = df[df['seed'] == 3]

    if 'group_result' not in seed3.columns:
        seed3['group_result'] = ''  # create the column if missing

    seed3_winners = seed3[seed3['group_result'].astype(str).str.strip().str.lower().isin(['', 'w'])]

    target_pairs = 16 if is_chess else 8

    # Build group stage
    group_pairs = build_group_stage_pairs(seed3_winners, is_chess, target_pairs)
    group_matches = build_group_stage_matches(group_pairs, df, sport, is_chess)

    # Build full knockout tree
    all_knockouts = build_full_knockout_tree(seed1, seed2, seed3, df, sport, is_chess)

    # Flatten all matches into multi-row-per-match format
    combined_fixtures = []

    # --- Group Stage ---
    for idx, m in enumerate(group_matches, start=1):
        combined_fixtures.append({
            "match_id": idx,
            "round": "Group Stage",
            "team": m["team 1"],
            "players": " & ".join(m["players 1"]),
            "result": ""
        })
        combined_fixtures.append({
            "match_id": idx,
            "round": "Group Stage",
            "team": m["team 2"],
            "players": " & ".join(m["players 2"]),
            "result": ""
        })

    # --- Knockouts ---
   
    global_match_id = 0
    used_pairs = set()  # track (team_name, players_str) to prevent duplication

    for round_name, matches in all_knockouts.items():
        for idx, m in enumerate(matches, start=1):
            global_match_id += 1

            # Determine left/right as before
            seed_side = 1
            if round_name == "Super 16":
                seed1_pref = [1,4,7,8]
                seed2_pref = [2,3,5,6]
                if idx in seed1_pref:
                    seed_side = 1
                elif idx in seed2_pref:
                    seed_side = 2
            elif round_name == "Super 32":
                seed1_pref = [1,4,15,16]
                seed2_pref = [2,3,13,14]
                if idx in seed1_pref:
                    seed_side = 1
                elif idx in seed2_pref:
                    seed_side = 2

            # Safely get team string and players
            def get_team_str_safe(team_placeholder):
                if not team_placeholder or str(team_placeholder).strip().upper() in ["B","TBD"]:
                    return "BYE", []
                team_placeholder = str(team_placeholder).strip()
                team_row = df[df['team_name'].str.strip().str.lower() == team_placeholder.lower()]
                if not team_row.empty:
                    pair_str = team_row.iloc[0].get('pair', "")
                    return team_placeholder, [p.strip() for p in pair_str.split("&")]
                else:
                    return team_placeholder, []

            # Assign left/right
            if seed_side == 1:
                team1_name, players1_list = get_team_str_safe(m[1])
                team2_name, players2_list = get_team_str_safe(m[2])
            else:
                team1_name, players1_list = get_team_str_safe(m[2])
                team2_name, players2_list = get_team_str_safe(m[1])

            # Prevent duplicates
            for t_name, p_list in [(team1_name, players1_list), (team2_name, players2_list)]:
                key = (t_name, " & ".join(p_list))
                if key not in used_pairs:
                    combined_fixtures.append({
                        "match_id": global_match_id,
                        "round": round_name,
                        "team": t_name,
                        "players": " & ".join(p_list),
                        "result": ""
                    })
                    used_pairs.add(key)


    # Save to sheet
    fixtures_df = pd.DataFrame(combined_fixtures)
    ROUND_ORDER = ["Group Stage", "Super 16", "Quarter Final", "Semi Final", "Final"]
    fixtures_df['round'] = pd.Categorical(fixtures_df['round'], categories=ROUND_ORDER, ordered=True)
    fixtures_df = fixtures_df.sort_values(['round', 'match_id']).reset_index(drop=True)

    # ✅ Convert players lists to string for Google Sheets
    fixtures_df['players'] = fixtures_df['players'].astype(str)

    write_fixtures_sheet(sport, fixtures_df)

    return df, group_matches, all_knockouts


def render_fixtures_for_sport(sport):
    st.markdown(
        f"<h2 style='font-size:28px;color:#FFD700;text-shadow:2px 2px 4px rgba(0,0,0,0.5);margin-top:20px;margin-bottom:10px;font-weight:bold;'>🏆 Fixtures for {sport.title()}</h2>",
        unsafe_allow_html=True
    )
    st.markdown("----")

    cache_key = f"fixtures_{sport.lower()}"
    fixture_flag_key = f"fixtures_ready_{sport.lower()}"
    regenerate = st.session_state.get(fixture_flag_key, False)

    if cache_key in st.session_state and not regenerate:
        df, group_matches, all_knockouts = st.session_state[cache_key]
    else:
        fixtures_df = read_fixtures_sheet(sport)
        if fixtures_df.empty:
            st.info("No fixtures found. Generate them first!")
            return

        df = fixtures_df.copy()

        # Split group vs knockout
        group_matches = []
        all_knockouts = {}
        for match_id, group in fixtures_df.groupby("match_id"):
            rows = group.to_dict(orient="records")
            round_name = rows[0]["round"]
            if round_name.lower() == "group stage":
                group_matches.append({
                    "match_id": match_id,
                    "team 1": rows[0]["team"],
                    "players 1": [p.strip() for p in rows[0]["players"].split(" & ") if p.strip()],
                    "result 1": rows[0].get("result", ""),
                    "team 2": rows[1]["team"] if len(rows) > 1 else "",
                    "players 2": [p.strip() for p in rows[1]["players"].split(" & ") if p.strip()] if len(rows) > 1 else [],
                    "result 2": rows[1].get("result", "") if len(rows) > 1 else ""
                })
            else:
                if round_name not in all_knockouts:
                    all_knockouts[round_name] = []
                t1_label = f"{rows[0]['team']}\n{rows[0]['players']}"
                t2_label = f"{rows[1]['team']}\n{rows[1]['players']}" if len(rows) > 1 else ""
                t1_result = rows[0].get("result", "")
                t2_result = rows[1].get("result", "")
                all_knockouts[round_name].append((match_id, t1_label, t2_label, t1_result, t2_result))

        st.session_state[cache_key] = (df, group_matches, all_knockouts)
        st.session_state[fixture_flag_key] = False

    # === Render Group Stage ===
    st.subheader("📦 Group Stage Matches")
    if not group_matches:
        st.info("No group matches available.")
    else:
        for i in range(0, len(group_matches), 2):
            cols = st.columns(2)
            with cols[0]:
                m = group_matches[i]
                display_card(
                    f"Match {m['match_id']}", m["team 1"], m["players 1"],
                    m["team 2"], m["players 2"],
                    match_id=m["match_id"], round_name="Group Stage", card_index=i,
                    result1=m["result 1"], result2=m["result 2"]
                )
            if i + 1 < len(group_matches):
                with cols[1]:
                    m = group_matches[i+1]
                    display_card(
                        f"Match {m['match_id']}", m["team 1"], m["players 1"],
                        m["team 2"], m["players 2"],
                        match_id=m["match_id"], round_name="Group Stage", card_index=i+1,
                        result1=m["result 1"], result2=m["result 2"]
                    )

    # === Render Knockouts ===
    st.subheader("🔗 Knockout Fixtures")
    for round_name, matches in all_knockouts.items():
        st.markdown(f"**{round_name}**")
        if not matches:
            st.info("No matches available yet.")
            continue
        for i in range(0, len(matches), 2):
            cols = st.columns(2)
            for col_idx, idx in enumerate([i, i+1]):
                if idx >= len(matches):
                    continue
                m = matches[idx]
                t1, p1 = extract_team_and_players(m[1])
                t2, p2 = extract_team_and_players(m[2])
                with cols[col_idx]:
                    display_card(
                        f"Match {m[0]}", t1, p1, t2, p2,
                        match_id=m[0], round_name=round_name, card_index=idx,
                        result1=m[3], result2=m[4]  # ✅ pass results
                    )
