import streamlit as st
import pandas as pd
from fixtures_modules.database_handler import load_sheet_as_df
from fixtures_modules.tournament_logic import (
    generate_group_stage_pairs,
    build_group_stage_matches,
    build_knockout_round
)
from fixtures_modules.constants import TOURNAMENT_STRUCTURE
from utils.ui_data import display_card

# === Helper ===
def extract_team_and_players(label):
    if "\n" in label:
        team, players = label.split("\n", 1)
        return team.strip(), players.strip().split(" & ")
    return label.strip(), []

def render_fixtures_for_sport(sport):
    st.header(f"🏆 Fixtures for {sport.title()}")

    # 🔁 Check cache
    if "fixture_cache" not in st.session_state:
        st.session_state.fixture_cache = {}

    refresh_key = f"refresh_{sport.lower()}"
    if st.button(f"🔁 Refresh Fixture Data for {sport}", key=refresh_key):
        st.session_state.fixture_cache.pop(sport, None)
        st.success("✅ Refreshed from Google Sheets")

    if sport in st.session_state.fixture_cache:
        df, group_matches, all_knockouts = st.session_state.fixture_cache[sport]
    else:
        df = load_sheet_as_df(sport)
        if df.empty:
            st.warning(f"Sheet for {sport} is empty or failed to load.")
            return

        is_chess = sport.lower() == "chess"
        df['seed'] = pd.to_numeric(df['seed'], errors='coerce').fillna(0).astype(int)
        seed1 = df[df['seed'] == 1]
        seed2 = df[df['seed'] == 2]
        seed3 = df[df['seed'] == 3]

        if not is_chess:
            df['player_1'] = df['player_1'].fillna('')
            df['player_2'] = df['player_2'].fillna('')
            df['pair'] = df['player_1'] + " & " + df['player_2']

        seed3_winners = seed3[
            seed3['group_result'].astype(str).str.strip().str.lower().isin(['', 'w'])
        ]

        group_pairs = generate_group_stage_pairs(seed3_winners, is_chess)
        group_matches = build_group_stage_matches(group_pairs, df, sport, is_chess)
        all_knockouts = build_knockout_round(seed1, seed2, group_pairs, df, sport, is_chess)

        st.session_state.fixture_cache[sport] = (df, group_matches, all_knockouts)

    # --- Group Stage ---
    with st.expander("📦 Group Stage Matches", expanded=True):
        if not group_matches:
            st.info("No group matches could be formed.")
        else:
            for i in range(0, len(group_matches), 2):
                cols = st.columns(2)
                with cols[0]:
                    m = group_matches[i]
                    display_card(
                        f"Match {i+1}", m["team 1"], m["players 1"],
                        m["team 2"], m["players 2"],
                        match_id=i+1, round_name="Group Stage", card_index=i
                    )
                if i + 1 < len(group_matches):
                    with cols[1]:
                        m = group_matches[i+1]
                        display_card(
                            f"Match {i+2}", m["team 1"], m["players 1"],
                            m["team 2"], m["players 2"],
                            match_id=i+2, round_name="Group Stage", card_index=i+1
                        )

    # --- Knockouts ---
    for round_name, matches in all_knockouts.items():
        with st.expander(f"🔗 {round_name} Fixtures", expanded=(round_name.lower() == "final")):
            if not matches:
                st.info("No matches available yet.")
            elif round_name.lower() == "final":
                m = matches[0]
                team1, players1 = extract_team_and_players(m[1])
                team2, players2 = extract_team_and_players(m[2])
                display_card(
                    f"Match {m[0]}",
                    team1=team1, players1=players1,
                    team2=team2, players2=players2,
                    match_id=m[0], round_name=round_name
                )
            else:
                for i in range(0, len(matches), 2):
                    cols = st.columns(2)
                    with cols[0]:
                        m = matches[i]
                        team1, players1 = extract_team_and_players(m[1])
                        team2, players2 = extract_team_and_players(m[2])
                        display_card(
                            f"Match {m[0]}",
                            team1=team1, players1=players1,
                            team2=team2, players2=players2,
                            match_id=m[0], round_name=round_name, card_index=i
                        )
                    if i + 1 < len(matches):
                        with cols[1]:
                            m = matches[i+1]
                            team1, players1 = extract_team_and_players(m[1])
                            team2, players2 = extract_team_and_players(m[2])
                            display_card(
                                f"Match {m[0]}",
                                team1=team1, players1=players1,
                                team2=team2, players2=players2,
                                match_id=m[0], round_name=round_name, card_index=i+1
                            )
