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

@st.cache_data(show_spinner=False)
def get_base64_image_cached(image_path: str):
    """Return base64 string for an image path. Cached across reruns."""
    if not image_path or not os.path.exists(image_path):
        return None
    return base64.b64encode(Path(image_path).read_bytes()).decode()

def build_rules_html(section) -> str:
    """Return HTML string for rules structure (list / dict)."""
    def _render_section(s):
        if isinstance(s, list):
            items = "".join(f"<li>{item}</li>" for item in s)
            return f"<ul class='rules-list'>{items}</ul>"
        elif isinstance(s, dict):
            out = ""
            for key, value in s.items():
                out += f"<div class='rule-section-title'>{key}</div>"
                out += _render_section(value)
            return out
        else:
            return f"<div>{str(s)}</div>"
    return _render_section(section)

def clear_fixtures_ui_cache(sport_name: str = None):
    """
    Developer helper to clear cached HTML/DF in session state.
    If sport_name is None, clears all fixtures UI cached keys.
    """
    keys = list(st.session_state.keys())
    for k in keys:
        if k.startswith("banner_html_") or k.startswith("rules_html_") or k.startswith("bonus_df_"):
            if sport_name:
                if k.endswith(f"_{sport_name.lower()}"):
                    del st.session_state[k]
            else:
                del st.session_state[k]

def render_sport_banner_and_rules(sport_name):
    """Render banner + rules, but generate HTML once and reuse via st.session_state cache."""

    load_global_styles()  # keep your global css loader

    banner_key = f"banner_html_{sport_name.lower()}"
    rules_key = f"rules_html_{sport_name.lower()}"

    # If both banner+rules are cached, render quickly and return
    if banner_key in st.session_state and rules_key in st.session_state:
        st.markdown(st.session_state[banner_key], unsafe_allow_html=True)
        # keep using st.expander for collapsible UI (cheap to call)
        with st.expander(f"📜 {sport_name} Rules"):
            st.markdown(st.session_state[rules_key], unsafe_allow_html=True)
        return

    # --- build banner HTML (cached base64 fetch) ---
    logo_path = SPORT_LOGOS.get(sport_name)
    img_base64 = get_base64_image_cached(logo_path) if logo_path else None

    if img_base64:
        banner_html = (
            f"""
            <div class="sport-banner">
                <img src="data:image/jpg;base64,{img_base64}" alt="{sport_name} banner" style="max-width:100%; border-radius:8px;">
            </div>
            """
        )
    else:
        banner_html = f"<div style='padding:8px;color:#ffc107;font-weight:700;'>No banner image found for {sport_name}.</div>"

    # --- build rules HTML (string) ---
    rules = SPORT_RULES.get(sport_name)
    if rules:
        rules_html = "<div class='rules-card'>" + build_rules_html(rules) + "</div>"
    else:
        rules_html = "<div class='rules-card'><em>No rules available for this sport.</em></div>"

    # persist in session_state so future reruns are instant
    st.session_state[banner_key] = banner_html
    st.session_state[rules_key] = rules_html

    # render once
    st.markdown(banner_html, unsafe_allow_html=True)
    with st.expander(f"📜 {sport_name} Rules"):
        st.markdown(rules_html, unsafe_allow_html=True)


def render_bonus_cards(sport_name):
    """Render bonus cards table; cache the DataFrame in session_state to avoid rebuilds."""
    cards = BONUS_CARDS.get(sport_name, [])

    if not cards:
        # keep behavior consistent
        return

    st.markdown("### 🎯 Bonus Cards")
    df_key = f"bonus_df_{sport_name.lower()}"

    # If cached df exists, use it (avoids reconstructing / expensive conversions)
    if df_key in st.session_state:
        st.dataframe(st.session_state[df_key], use_container_width=True, hide_index=True)
        return

    # Build DataFrame and cache it
    try:
        df = pd.DataFrame(cards)
    except Exception:
        # fallback — small safe render
        df = pd.DataFrame.from_records(cards)

    st.session_state[df_key] = df
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
