# TLOL_Dash/sections/fixtures.py

import streamlit as st
import pandas as pd
import random
import os, time
import base64
from itertools import combinations
from sections.ui_data import display_card
#from openpyxl import load_workbook
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse



def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Constants
SPORTS = ["Foosball", "Carrom", "Chess", "Table tennis" ,"Badminton"]

ROUND_EMOJIS = {
    "Super 32": "🔶",
    "Super 16": "🔵",
    "Quarter Finals": "🏐",
    "Semi Finals": "🥈",
    "Final": "🏆"
}


# Setup Google Sheets Access
#@st.cache_resource()
def get_gsheet_connection():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("data/gcp_service_account.json", scopes=scope)
    return gspread.authorize(creds)

GOOGLE_SHEET_ID = "1854rtEWHjp1-akVlSIzjdR_PxUW1hdKxnU2hOp5KPTw"

def load_google_sheet_tab(sheet_name):
    SHEET_ID = "1854rtEWHjp1-akVlSIzjdR_PxUW1hdKxnU2hOp5KPTw"
    encoded_sheet_name = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower()
    return df

#@st.cache_data
def load_seeded_pairs(sport):
    try:
        return load_google_sheet_tab(sport)
    except Exception as e:
        st.error(f"❌ Could not load sheet '{sport}': {e}")
        return pd.DataFrame()

def avoid_same_team_pairing(entities, total_required_pairs=None):
    valid_pairs = [
        (i, j) for i, j in combinations(range(len(entities)), 2)
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
    if total_required_pairs and len(result) < total_required_pairs:
        remaining = [e for idx, e in enumerate(entities) if idx not in used]
        random.shuffle(remaining)
        while len(result) < total_required_pairs and len(remaining) >= 2:
            result.append((remaining.pop(), remaining.pop()))
    return result

def strict_fair_pairing(group_winners, qualified):
    random.shuffle(group_winners)
    random.shuffle(qualified)
    pairs = []
    used_q = set()
    for gw in group_winners:
        for q in qualified:
            if q['team name'] != gw['team name'] and q['label'] not in used_q:
                pairs.append((gw, q))
                used_q.add(q['label'])
                break
    remaining = [q for q in qualified if q['label'] not in used_q]
    while len(pairs) < len(group_winners) and remaining:
        if len(pairs) < len(group_winners):
            pairs.append((group_winners[len(pairs)], remaining.pop()))
        else:
            break
    return pairs

def interleave_seeds(seed1, seed2, group_labels):
    random.shuffle(seed1)
    random.shuffle(seed2)
    interleaved = []
    s1_idx = s2_idx = 0
    while len(interleaved) < len(group_labels) and (s1_idx < len(seed1) or s2_idx < len(seed2)):
        if s1_idx < len(seed1):
            interleaved.append(seed1[s1_idx])
            s1_idx += 1
        if len(interleaved) < len(group_labels) and s2_idx < len(seed2):
            interleaved.append(seed2[s2_idx])
            s2_idx += 1
    qualified = interleaved
    half = len(qualified) // 2
    return qualified[:half], qualified[half:]

def generate_knockout(matches, round_names):
    knockout_structure = {round_name: [] for round_name in round_names}
    match_counter = 1
    current_round_participants = [
        f"Winner Match {i + 1}" if isinstance(m, dict) else f"Winner Match {m[0]}"
        for i, m in enumerate(matches)
    ]
    for round_name in round_names:
        if not current_round_participants:
            break
        next_round_participants = []
        for i in range(0, len(current_round_participants), 2):
            m1 = current_round_participants[i]
            m2 = current_round_participants[i + 1] if i + 1 < len(current_round_participants) else "BYE"
            knockout_structure[round_name].append((match_counter, m1, m2))
            next_round_participants.append(f"Winner Match {match_counter}")
            match_counter += 1
        current_round_participants = next_round_participants
    return knockout_structure

def extract_pair(label):
    try:
        return label.split('\n')[1].strip('()')
    except (IndexError, AttributeError):
        return ''

def generate_fixtures_for_sport(sport, seeded_df):
    from helpers.gsheet_utils import update_match_number

    sport_lower = sport.lower()
    if seeded_df.empty:
        return [], {}

    group_stage_matches = []
    knockout = {}
    is_chess = sport_lower == "chess"

    df = seeded_df.copy()
    df['seed'] = df['seed'].astype(int)
    df['group_result'] = df['group_result'].fillna('')

    if is_chess:
        df['pair'] = df['player']
    else:
        df['player 1'] = df['player 1'].fillna('')
        df['player 2'] = df['player 2'].fillna('')
        df['pair'] = df['player 1'] + " & " + df['player 2']

    base_columns = [
        "group_match_no", "group_result",
        "super_16_match_no", "super_16_result",
        "quarter_match_no", "quarter_result",
        "semi_match_no", "semi_result",
        "final_match_no", "final_result"
    ]
    if is_chess:
        base_columns = ["super_32_match_no", "super_32_result"] + base_columns

    for col in base_columns:
        if col not in df.columns:
            df[col] = ''

    # Split by seed
    seed1 = df[df['seed'] == 1].copy()
    seed2 = df[df['seed'] == 2].copy()
    seed3 = df[df['seed'] == 3].copy()

    # Filter eligible seed 3 players
    seed3_winners = [
        row for _, row in seed3.iterrows()
        if str(row['group_result']).strip().lower() in ['w', '']
    ]
    if len(seed3_winners) < 2:
        st.warning("Not enough Seed 3 participants for group stage.")
        return [], {}

    seed3_winners = pd.DataFrame(seed3_winners)
    records = seed3_winners.to_dict('records')
    group_pairs = avoid_same_team_pairing(records, total_required_pairs=min(8, len(records) // 2))

    group_labels = []
    for i, (p1, p2) in enumerate(group_pairs):
        match_no = i + 1
        group_labels.append(f"Winner Match {match_no} (Seed 3)")

        players1 = (p1['player'],) if is_chess else (p1['player 1'], p1['player 2'])
        players2 = (p2['player'],) if is_chess else (p2['player 1'], p2['player 2'])
        team1, team2 = p1['team name'], p2['team name']

        result1 = str(p1.get("group_result", "")).strip().lower()
        result2 = str(p2.get("group_result", "")).strip().lower()

        if result1 == 'w':
            team1 += " 🏆"
            team2 += " 🦆"
        elif result2 == 'w':
            team2 += " 🏆"
            team1 += " 🦆"

        group_stage_matches.append({
            'team 1': team1, 'players 1': players1,
            'team 2': team2, 'players 2': players2
        })

        match_stage = "Super 16" if not is_chess else "Super 32"
        match_no_col = match_stage.lower().replace(" ", "_") + "_match_no"

        for p in [p1, p2]:
            id_col = 'player' if is_chess else 'pair'
            identifier = p[id_col]
            existing_val = df.loc[df[id_col] == identifier, match_no_col].iloc[0]
            if pd.isna(existing_val) or str(existing_val).strip() == '':
                update_match_number(
                    sheet_name=sport,
                    id_col_name=id_col,
                    identifier=identifier,
                    match_col=match_no_col,
                    match_no=match_no
                )

    # Build Knockout rounds (Super 16/32)
    match_stage = "Super 16" if not is_chess else "Super 32"
    match_range = 8 if not is_chess else 16
    super_matches = {i: [None, None] for i in range(1, match_range + 1)}

    for _, row in seed1.iterrows():
        match_no = row.get("super_16_match_no" if not is_chess else "super_32_match_no")
        if pd.notnull(match_no):
            label = f"{row['team name']}\n({row['player'] if is_chess else row['pair']})"
            super_matches[int(match_no)][0] = label

    for _, row in seed2.iterrows():
        match_no = row.get("super_16_match_no" if not is_chess else "super_32_match_no")
        if pd.notnull(match_no):
            label = f"{row['team name']}\n({row['player'] if is_chess else row['pair']})"
            super_matches[int(match_no)][1] = label

    group_winner_labels = []
    for i, (p1, p2) in enumerate(group_pairs):
        match_no = i + 1
        result1 = str(p1.get("group_result", "")).strip().lower()
        result2 = str(p2.get("group_result", "")).strip().lower()

        if result1 == 'w':
            label = f"{p1['team name']}\n({p1['player'] if is_chess else p1['pair']})"
        elif result2 == 'w':
            label = f"{p2['team name']}\n({p2['player'] if is_chess else p2['pair']})"
        else:
            label = f"Winner Match {match_no} (Seed 3)"

        group_winner_labels.append(label)

    gwi = 0
    for match_no in super_matches:
        for slot in [0, 1]:
            if super_matches[match_no][slot] is None and gwi < len(group_winner_labels):
                super_matches[match_no][slot] = group_winner_labels[gwi]
                gwi += 1

    next_matches = []
    for match_no in range(1, match_range + 1):
        next_matches.append((match_no, *super_matches[match_no]))

    # Optional: you can write back these Super 16/32 match numbers too

    knockout = generate_knockout(
        next_matches,
        ["Quarter Finals", "Semi Finals", "Final"] if not is_chess else
        ["Super 16", "Quarter Finals", "Semi Finals", "Final"]
    )

    return group_stage_matches, {match_stage: next_matches, **knockout}



def reset_fixtures():
    for sport in SPORTS:
        st.session_state.pop(f"fixtures_{sport}_matches", None)
        st.session_state.pop(f"fixtures_{sport}_knockouts", None)

@st.cache_data
def generate_fixtures_globally(sport):
    seeded_df = load_seeded_pairs(sport)
    if seeded_df.empty: # Add check for empty dataframe from load_seeded_pairs
        return [], {}
    return generate_fixtures_for_sport(sport, seeded_df)

def render_sport_fixtures(sport):
    if f"fixtures_{sport}_matches" not in st.session_state:
        matches, knockouts = generate_fixtures_globally(sport)
        st.session_state[f"fixtures_{sport}_matches"] = matches
        st.session_state[f"fixtures_{sport}_knockouts"] = knockouts

    matches = st.session_state[f"fixtures_{sport}_matches"]
    knockouts = st.session_state[f"fixtures_{sport}_knockouts"]

    # Sport-specific background image
    image_filename = f"assets/{sport.lower()}.jpg"
    if os.path.exists(image_filename):
        with open(image_filename, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(f"""
                <div style='background-image: url("data:image/jpeg;base64,{encoded}"); background-size: cover; background-position: center; padding: 40px 20px;'>
            """, unsafe_allow_html=True)

    # Group Stage
    with st.expander("🟡 Group Stage", expanded=True):
        if not matches:
            st.info("No group stage matches generated for this sport yet.")
        for i in range(0, len(matches), 3):
            cols = st.columns(3)
            for j, match in enumerate(matches[i:i + 3]):
                index = i + j  # unique card index
                with cols[j]:
                    match_id = f"{sport.lower()}_group_stage_match_{index}"
                    display_card(
                        title=f"Match {index + 1}",
                        team1=match["team 1"],
                        players1=match["players 1"],
                        team2=match["team 2"],
                        players2=match["players 2"],
                        match_id=match_id,
                        round_name="Group Stage",
                        card_index=index
                    )

    # Knockout Rounds
    for round_name, round_matches in knockouts.items():
        emoji = ROUND_EMOJIS.get(round_name, "")
        with st.expander(f"{emoji} {round_name}", expanded=True):
            if not round_matches:
                st.info(f"No {round_name} matches generated for this sport yet.")
                continue

            for i in range(0, len(round_matches), 2):
                cols = st.columns(2)
                for j, match in enumerate(round_matches[i:i + 2]):
                    match_index = i + j
                    match_num = match_index + 1
                    with cols[j]:
                        match_id = f"{sport.lower()}_{round_name.lower().replace(' ', '_')}_match_{match_num}"
                        match_title = f"Match {match_num}"

                        team1, team2 = "TBD", "TBD"
                        players1, players2 = ("TBD",), ("TBD",)
                        team1_result = team2_result = ""

                        if isinstance(match, dict):
                            team1 = match.get('team 1', 'TBD')
                            players1 = match.get('players 1', ('TBD',))
                            team2 = match.get('team 2', 'TBD')
                            players2 = match.get('players 2', ('TBD',))
                            team1_result = str(match.get('p1_dict', {}).get(f"{round_name.lower().replace(' ', '_')}_result", "")).strip().lower()
                            team2_result = str(match.get('p2_dict', {}).get(f"{round_name.lower().replace(' ', '_')}_result", "")).strip().lower()

                        elif isinstance(match, tuple):
                            mid, t1_data, t2_data = match
                            match_title = f"Match {mid}"

                            def parse_team(side):
                                if isinstance(side, dict):
                                    name = side.get("team name", "TBD")
                                    result = str(side.get(f"{round_name.lower().replace(' ', '_')}_result", "")).strip().lower()
                                    if "player" in side:
                                        players = (side["player"],)
                                    else:
                                        players = (
                                            side.get("player 1", ""),
                                            side.get("player 2", "")
                                        )
                                elif isinstance(side, str):
                                    parts = side.split("\n")
                                    name = parts[0].split("(")[0].strip() if parts else "TBD"
                                    players = tuple(parts[1].strip("()").split(" & ")) if len(parts) > 1 else ("TBD",)
                                    result = ""
                                else:
                                    name, players, result = "TBD", ("TBD",), ""
                                return name, players, result

                            team1, players1, team1_result = parse_team(t1_data)
                            team2, players2, team2_result = parse_team(t2_data)

                        # Cleanup missing players
                        players1 = tuple(p for p in players1 if p) or ("TBD",)
                        players2 = tuple(p for p in players2 if p) or ("TBD",)

                        # Mark winners/eliminated
                        if team1_result == "w":
                            team1 += " 🏆"
                            team2 += " 🦆"
                        elif team2_result == "w":
                            team2 += " 🏆"
                            team1 += " 🦆"

                        # Display card
                        display_card(
                            title=match_title,
                            team1=team1,
                            players1=players1,
                            team2=team2,
                            players2=players2,
                            match_id=match_id,
                            round_name=round_name,
                            card_index=match_index
                        )

            # ▶ Add a "Regenerate" button for updating fixtures
            if round_name != "Final":
                regen_key = f"regen_{sport}_{round_name}"
                if st.button(f"🔄 Regenerate {round_name} for {sport}", key=regen_key):
                    st.session_state.pop(f"fixtures_{sport}_matches", None)
                    st.session_state.pop(f"fixtures_{sport}_knockouts", None)
                    st.rerun()

    # if os.path.exists(image_filename):
    #     st.markdown("</div>", unsafe_allow_html=True)


def render():
    load_global_styles()
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

