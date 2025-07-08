# TLOL_Dash/sections/fixtures.py

import streamlit as st
import pandas as pd
import random
import os
import base64
from itertools import combinations

# Constants
SPORTS = ["Foosball", "Carrom", "Chess"]

ROUND_EMOJIS = {
    "Super 32": "🔶",
    "Super 16": "🔵",
    "Quarter Finals": "🏐",
    "Semi Finals": "🥈",
    "Final": "🏆"
}


def load_seeded_pairs(sport):
    df = pd.read_excel("reports/seeded_teams.xlsx", sheet_name=sport)
    df.columns = df.columns.str.strip().str.lower()
    return df

def avoid_same_team_pairing(entities, total_required_pairs=None):
    valid_pairs = [
        (i, j)
        for i, j in combinations(range(len(entities)), 2)
        if entities[i]['team name'] != entities[j]['team name']
    ]
    random.shuffle(valid_pairs)

    used = set()
    result = []
    for i, j in valid_pairs:
        if i not in used and j not in used:
            result.append((entities[i], entities[j]))
            used.add(i)
            used.add(j)

    # Fallback: fill remaining pairs randomly if needed
    if total_required_pairs and len(result) < total_required_pairs:
        remaining = [e for idx, e in enumerate(entities) if idx not in used]
        random.shuffle(remaining)
        while len(result) < total_required_pairs and len(remaining) >= 2:
            result.append((remaining.pop(), remaining.pop()))

    return result



def generate_knockout(matches, round_names):
    knockout_structure = {round_name: [] for round_name in round_names}
    match_counter = 1
    current_round = [f"Winner Match {i + 1}" if isinstance(m, dict) else f"Winner Match {m[0]}" for i, m in enumerate(matches)]

    for round_name in round_names:
        next_round = []
        for i in range(0, len(current_round), 2):
            m1 = current_round[i]
            m2 = current_round[i + 1] if i + 1 < len(current_round) else "BYE"
            knockout_structure[round_name].append((match_counter, m1, m2))
            next_round.append(f"Winner Match {match_counter}")
            match_counter += 1
        current_round = next_round

    return knockout_structure


def generate_fixtures_for_sport(sport, seeded_df):
    sport = sport.lower()

    if sport == "chess":
        players = seeded_df[['player', 'team name', 'seed']].dropna().to_dict('records')
        seed1 = [p for p in players if p['seed'] == 1]
        seed2 = [p for p in players if p['seed'] == 2]
        seed3 = [p for p in players if p['seed'] == 3]

        if len(seed3) < 32:
            st.error("At least 32 seed 3 players are required for group stage in Chess.")
            return [], {}

        group_pairs = avoid_same_team_pairing(seed3[:32], total_required_pairs=16)
        group_stage_matches = []
        for i, (p1, p2) in enumerate(group_pairs):
            group_stage_matches.append({
                'team 1': p1['team name'], 'players 1': (p1['player'],),
                'team 2': p2['team name'], 'players 2': (p2['player'],)
            })

        qualified = seed1 + seed2
        random.shuffle(qualified)
        group_winner_labels = [f"Winner Match {i + 1} (Seed 3)" for i in range(len(group_pairs))]

        super32_raw = [
            {'team name': q['team name'], 'player': q['player'], 'label': f"{q['team name']} (Seed {q['seed']})\n({q['player']})"}
            for q in qualified[:len(group_pairs)]
        ]

        super32_pairs = avoid_same_team_pairing([
            {'team name': label, 'player': label} for label in group_winner_labels + [p['label'] for p in super32_raw]
        ])

        super32_matches = [(i + 1, pair[0]['team name'], pair[1]['team name']) for i, pair in enumerate(super32_pairs)]

        knockout = generate_knockout(super32_matches, ["Super 16", "Quarter Finals", "Semi Finals", "Final"])
        return group_stage_matches, {"Super 32": super32_matches, **knockout}

    elif sport in ["foosball", "carrom"]:
        df = seeded_df.copy()
        df['pair'] = list(zip(df['player 1'], df['player 2']))
        seed1 = df[df['seed'] == 1]
        seed2 = df[df['seed'] == 2]
        seed3 = df[df['seed'] == 3]

        if len(seed3) < 16:
            st.warning(f"Not enough Seed 3 pairs for group stage ({len(seed3)} found).")
            return [], {}

        group_stage_candidates = seed3.sample(n=16, random_state=42).reset_index(drop=True).to_dict('records')
        group_pairs = avoid_same_team_pairing(group_stage_candidates, total_required_pairs=8)

        group_stage_matches = []
        for i, (p1, p2) in enumerate(group_pairs):
            group_stage_matches.append({
                'team 1': p1['team name'], 'players 1': (p1['player 1'], p1['player 2']),
                'team 2': p2['team name'], 'players 2': (p2['player 1'], p2['player 2'])
            })

        winners = [f"Winner Match {i + 1} (Seed 3)" for i in range(len(group_pairs))]
        qualified = pd.concat([seed1, seed2]).sample(n=len(group_pairs)).reset_index(drop=True)
        qualified_labels = [
            f"{row['team name']} (Seed {row['seed']})\n({row['player 1']} & {row['player 2']})"
            for _, row in qualified.iterrows()
        ]

        combined = [{'team name': a} for a in winners + qualified_labels]
        super16_pairs = avoid_same_team_pairing(combined)

        super16_matches = [(i + 1, p1['team name'], p2['team name']) for i, (p1, p2) in enumerate(super16_pairs)]

        knockout = generate_knockout(super16_matches, ["Quarter Finals", "Semi Finals", "Final"])
        return group_stage_matches, {"Super 16": super16_matches, **knockout}

    return [], {}

def reset_fixtures():
    for sport in SPORTS:
        st.session_state.pop(f"fixtures_{sport}_matches", None)
        st.session_state.pop(f"fixtures_{sport}_knockouts", None)

@st.cache_data
def generate_fixtures_globally(sport):
    seeded_df = load_seeded_pairs()
    return generate_fixtures_for_sport(sport, seeded_df)

def render_sport_fixtures(sport):
    seeded_df = load_seeded_pairs(sport)

    if f"fixtures_{sport}_matches" not in st.session_state:
        matches, knockouts = generate_fixtures_globally(sport)
        st.session_state[f"fixtures_{sport}_matches"] = matches
        st.session_state[f"fixtures_{sport}_knockouts"] = knockouts

    matches = st.session_state[f"fixtures_{sport}_matches"]
    knockouts = st.session_state[f"fixtures_{sport}_knockouts"]

    def display_card(title, team1, players1, team2, players2):
        p1 = " & ".join(players1)
        p2 = " & ".join(players2)
        return f"""
        <div style='background: linear-gradient(135deg, #fceabb 0%, #f8b500 100%); padding: 18px; border-radius: 15px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #000; height: 160px; display: flex; flex-direction: column; justify-content: space-between;'>
            <div style='font-size: 18px; font-weight: bold; text-align: center;'>{title}</div>
            <div style='display: flex; justify-content: space-around; align-items: center;'>
                <div style='flex: 1; text-align: center;'>
                    <div style='font-weight: bold;'>{team1}</div>
                    <div style='font-size: 13px; color: #333;'>({p1})</div>
                </div>
                <div style='flex: 0.2; text-align: center;'>
                    <span style='font-size: 24px;'>⚔️</span>
                </div>
                <div style='flex: 1; text-align: center;'>
                    <div style='font-weight: bold;'>{team2}</div>
                    <div style='font-size: 13px; color: #333;'>({p2})</div>
                </div>
            </div>
        </div>
        """


    # Sport-specific image as full section background
    image_filename = f"assets/{sport.lower()}.jpg"
    if os.path.exists(image_filename):
        with open(image_filename, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(f"""
            <div style='background-image: url("data:image/jpeg;base64,{encoded}"); background-size: cover; background-position: center; padding: 40px 20px;'>
            """, unsafe_allow_html=True)

    with st.expander("🟡 Group Stage"):
        for i in range(0, len(matches), 3):
            cols = st.columns(3)
            for j, m in enumerate(matches[i:i + 3]):
                with cols[j]:
                    st.markdown(display_card(f"Match {i + j + 1}", m['team 1'], m['players 1'], m['team 2'], m['players 2']), unsafe_allow_html=True)

    for round_name, round_matches in knockouts.items():
        emoji = ROUND_EMOJIS.get(round_name, "")
        with st.expander(f"{emoji} {round_name}"):
            for i in range(0, len(round_matches), 2):
                cols = st.columns(2)
                for j, match in enumerate(round_matches[i:i + 2]):
                    with cols[j]:
                        if isinstance(match, dict):
                            st.markdown(display_card(
                                f"Match {i + j + 1}",
                                match['team 1'], match['players 1'],
                                match['team 2'], match['players 2']
                            ), unsafe_allow_html=True)
                        elif isinstance(match, tuple):
                            mid, t1, t2 = match
                            st.markdown(display_card(f"Match {mid}", t1, ("",), t2, ("",)), unsafe_allow_html=True)

    if os.path.exists(image_filename):
        st.markdown("</div>", unsafe_allow_html=True)



def render():
    st.title("🎬 TLOL3 Sports Fixtures")

    with st.expander("🔐 Admin Controls"):
        admin_code = st.text_input("Enter Secret Code", type="password")
        if st.button("🔄 Reset Fixtures") and admin_code == "tlol-access":
            reset_fixtures()
            st.success("Fixtures reset.")

    tabs = st.tabs(SPORTS)
    for i, sport in enumerate(SPORTS):
        with tabs[i]:
            render_sport_fixtures(sport)
