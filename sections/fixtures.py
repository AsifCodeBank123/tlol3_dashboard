import streamlit as st
import pandas as pd

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
import base64
from pathlib import Path

def get_base64_image(image_path):
    """Convert image file to base64 string."""
    img_bytes = Path(image_path).read_bytes()
    return base64.b64encode(img_bytes).decode()

def render_sport_banner_and_rules(sport_name):
    # Banner
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

    # Recursive Renderer with HTML wrappers
    def render_rules_section(section, level=0):
        if isinstance(section, list):
            st.markdown(
                "<ul class='rules-list'>" + 
                "".join([f"<li>{item}</li>" for item in section]) + 
                "</ul>",
                unsafe_allow_html=True
            )
        elif isinstance(section, dict):
            for key, value in section.items():
                st.markdown(f"<div class='rule-section-title'>{key}</div>", unsafe_allow_html=True)
                render_rules_section(value, level + 1)

    # Rules Expander
    rules = SPORT_RULES.get(sport_name)
    if rules:
        with st.expander(f"📜 {sport_name} Rules"):
            st.markdown("<div class='rules-card'>", unsafe_allow_html=True)
            render_rules_section(rules)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No rules available for this sport.")

def render_bonus_cards(sport_name):
    cards = BONUS_CARDS.get(sport_name, [])
    if cards:
        st.markdown("### 🎯 Bonus Cards")
        df = pd.DataFrame(cards)
        st.dataframe(df, use_container_width=True, hide_index=True)


# Ensure all fixture-ready flags are preserved
for sport in ["Foosball", "Carrom", "Table tennis", "Badminton", "Chess"]:
    key = f"fixtures_ready_{sport.lower()}"
    if key not in st.session_state:
        st.session_state[key] = False

# === Helper ===
def extract_team_and_players(label):
    if "\n" in label:
        team, players = label.split("\n", 1)
        return team.strip(), players.strip().split(" & ")
    return label.strip(), []


def render_fixtures_for_sport(sport):
    
    st.markdown(f"<h2 style='font-size:28px;color:#FFD700;text-shadow:2px 2px 4px rgba(0,0,0,0.5);margin-top:20px;margin-bottom:10px;font-weight:bold;'>🏆 Fixtures for {sport.title()}</h2>", unsafe_allow_html=True)
    st.markdown("----")

    cache_key = f"fixtures_{sport.lower()}"
    fixture_flag_key = f"fixtures_ready_{sport.lower()}"
    regenerate = st.session_state.get(fixture_flag_key, False)

    # === If cached and no regeneration requested, use cache ===
    if cache_key in st.session_state and not regenerate:
        df, group_matches, all_knockouts = st.session_state[cache_key]

    else:
        # === Load fixtures from sheet ===
        fixture_df = read_fixtures_sheet(sport)

        if not fixture_df.empty and not regenerate:
            # Parse group matches and knockout matches from saved fixture sheet using actual match numbers
            df = load_sheet_as_df(sport)
            group_matches = []
            all_knockouts = {}

            for _, row in fixture_df.iterrows():
                match = {
                    "team 1": row["team_1"],
                    "players 1": str(row["players_1"]).split(" & "),
                    "team 2": row["team_2"],
                    "players 2": str(row["players_2"]).split(" & "),
                    "match_id": int(row["match_id"]),
                    "round": row["round"]
                }

                if row["round"].lower() == "group stage":
                    group_matches.append(match)
                else:
                    round_name = row["round"]
                    if round_name not in all_knockouts:
                        all_knockouts[round_name] = []
                    all_knockouts[round_name].append((
                        int(row["match_id"]),
                        f"{match['team 1']}\n{' & '.join(match['players 1'])}",
                        f"{match['team 2']}\n{' & '.join(match['players 2'])}"
                    ))

            st.session_state[cache_key] = (df, group_matches, all_knockouts)
            st.session_state[fixture_flag_key] = False  # reset regenerate flag

        else:
            # === Generate fresh fixtures ===
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

            seed3_winners = seed3[seed3['group_result'].astype(str).str.strip().str.lower().isin(['', 'w'])]

            target_pairs = 16 if is_chess else 8
            group_pairs = build_group_stage_pairs(seed3_winners, is_chess, target_pairs)
            group_matches = build_group_stage_matches(group_pairs, df, sport, is_chess)
            all_knockouts = build_full_knockout_tree(seed1, seed2, seed3, df, sport, is_chess)

            combined_fixtures = []
            for m in group_matches:
                combined_fixtures.append({
                    "match_id": m.get("match_id") or len(combined_fixtures) + 1,
                    "round": "Group Stage",
                    "team_1": m["team 1"],
                    "players_1": " & ".join(m["players 1"]),
                    "team_2": m["team 2"],
                    "players_2": " & ".join(m["players 2"]),
                })

            for round_name, matches in all_knockouts.items():
                for m in matches:
                    team1, players1 = extract_team_and_players(m[1])
                    team2, players2 = extract_team_and_players(m[2])
                    combined_fixtures.append({
                        "match_id": m[0],
                        "round": round_name,
                        "team_1": team1,
                        "players_1": " & ".join(players1),
                        "team_2": team2,
                        "players_2": " & ".join(players2),
                    })

            fixtures_df = pd.DataFrame(combined_fixtures)
            write_fixtures_sheet(sport, fixtures_df)

            st.session_state[cache_key] = (df, group_matches, all_knockouts)
            st.session_state[fixture_flag_key] = False

    # === Now render using cached stable matches ===
    st.subheader("📦 Group Stage Matches")
    try:
        if not group_matches:
            st.info("No group matches could be formed.")
        else:
            for i in range(0, len(group_matches), 2):
                cols = st.columns(2)
                with cols[0]:
                    m = group_matches[i]
                    display_card(
                        f"Match {m['match_id']}", m["team 1"], m["players 1"],
                        m["team 2"], m["players 2"],
                        match_id=m["match_id"], round_name="Group Stage", card_index=i
                    )
                if i + 1 < len(group_matches):
                    with cols[1]:
                        m = group_matches[i+1]
                        display_card(
                            f"Match {m['match_id']}", m["team 1"], m["players 1"],
                            m["team 2"], m["players 2"],
                            match_id=m["match_id"], round_name="Group Stage", card_index=i+1
                        )
    except Exception as e:
        import traceback
        st.error("❌ Error displaying Group Stage Matches")
        st.code(traceback.format_exc())

    st.subheader("🔗 Knockout Fixtures")
    for round_name, matches in all_knockouts.items():
        st.markdown(f"**{round_name}**")
        if not matches:
            st.info("No matches available yet.")
        elif round_name.lower() == "final":
            m = matches[0]
            team1, players1 = extract_team_and_players(m[1])
            team2, players2 = extract_team_and_players(m[2])
            display_card(f"Match {m[0]}", team1, players1, team2, players2, match_id=m[0], round_name=round_name)
        else:
            for i in range(0, len(matches), 2):
                cols = st.columns(2)
                with cols[0]:
                    m = matches[i]
                    team1, players1 = extract_team_and_players(m[1])
                    team2, players2 = extract_team_and_players(m[2])
                    display_card(f"Match {m[0]}", team1, players1, team2, players2, match_id=m[0], round_name=round_name, card_index=i)
                if i + 1 < len(matches):
                    with cols[1]:
                        m = matches[i+1]
                        team1, players1 = extract_team_and_players(m[1])
                        team2, players2 = extract_team_and_players(m[2])
                        display_card(f"Match {m[0]}", team1, players1, team2, players2, match_id=m[0], round_name=round_name, card_index=i+1)
