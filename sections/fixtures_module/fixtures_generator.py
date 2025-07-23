import pandas as pd
import streamlit as st
import os
from sections.fixtures_module.match_pairing import avoid_same_team_pairing
from sections.fixtures_module.utils import extract_pair

def generate_knockout(matches, round_names):
    knockout_structure = {r: [] for r in round_names}
    match_id = 1
    curr_round = [f"Winner Match {i+1}" for i in range(len(matches))]
    for r in round_names:
        next_round = []
        for i in range(0, len(curr_round), 2):
            p1 = curr_round[i]
            p2 = curr_round[i+1] if i+1 < len(curr_round) else "BYE"
            knockout_structure[r].append((match_id, p1, p2))
            next_round.append(f"Winner Match {match_id}")
            match_id += 1
        curr_round = next_round
    return knockout_structure

def generate_fixtures_for_sport(sport, seeded_df):
    sport_lower = sport.lower()
    if seeded_df.empty:
        return [], {}

    output_path = "reports/seeded_teams.xlsx"
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

    # Ensure required columns exist
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

    # Get seeded participants
    seed1 = df[df['seed'] == 1].copy()
    seed2 = df[df['seed'] == 2].copy()
    seed3 = df[df['seed'] == 3].copy()

    # Group candidates (w or undecided only)
    seed3_winners = [
        row for _, row in seed3.iterrows()
        if str(row['group_result']).strip().lower() in ['w', '']
    ]
    if len(seed3_winners) < 2:
        st.warning("Not enough seed 3 participants for group stage.")
        return [], {}

    seed3_winners = pd.DataFrame(seed3_winners)

    # Generate Group Matches
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
        result_col = match_stage.lower().replace(" ", "_") + "_result"


        # Assign group match number once
        for p in [p1, p2]:
            id_col = 'player' if is_chess else 'pair'
            identifier = p[id_col]
            # Only assign match_no if not already present (preserve existing)
            existing = df.loc[df[id_col] == identifier, match_no_col].iloc[0]
            if pd.isna(existing) or str(existing).strip() == '':
                df.loc[df[id_col] == identifier, match_no_col] = match_no


    # Build Super 16 or Super 32 structure
    match_stage = "Super 16" if not is_chess else "Super 32"
    match_range = 8 if not is_chess else 16
    super_matches = {i: [None, None] for i in range(1, match_range + 1)}

    # Place Seed 1 in LEFT (slot 0), Seed 2 in RIGHT (slot 1)
    for _, row in seed1.iterrows():
        match_no = row.get("super_16_match_no") if not is_chess else row.get("super_32_match_no")
        if pd.notnull(match_no):
            label = f"{row['team name']}\n({row['player'] if is_chess else row['pair']})"
            super_matches[int(match_no)][0] = label

    for _, row in seed2.iterrows():
        match_no = row.get("super_16_match_no") if not is_chess else row.get("super_32_match_no")
        if pd.notnull(match_no):
            label = f"{row['team name']}\n({row['player'] if is_chess else row['pair']})"
            super_matches[int(match_no)][1] = label

    # Create group winner labels or placeholders
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

    # Fill remaining open slots starting from group winner labels
    gwi = 0
    for match_no in super_matches:
        for slot in [0, 1]:
            if super_matches[match_no][slot] is None and gwi < len(group_winner_labels):
                super_matches[match_no][slot] = group_winner_labels[gwi]
                gwi += 1

    next_matches = []
    for match_no in range(1, match_range + 1):
        left, right = super_matches[match_no]
        next_matches.append((match_no, left, right))

    # Update df with Super match numbers and results
    match_no_col = match_stage.lower().replace(" ", "_") + "_match_no"
    result_col = match_stage.lower().replace(" ", "_") + "_result"
    for match_no, team1, team2 in next_matches:
        for label in [team1, team2]:
            pair = extract_pair(label)
            id_col = 'player' if is_chess else 'pair'
            mask = df[id_col] == pair
            if not df.loc[mask, match_no_col].astype(str).str.strip().any():
                df.loc[mask, match_no_col] = match_no
            if result_col in df.columns:
                df.loc[mask, result_col] = df[result_col].fillna('')

    # Generate KO structure
    knockout = generate_knockout(
        next_matches,
        ["Quarter Finals", "Semi Finals", "Final"] if not is_chess else
        ["Super 16", "Quarter Finals", "Semi Finals", "Final"]
    )

    # Save updated df (unique records only)
    final_df = df.drop_duplicates(
        subset=['team name', 'pair'] if not is_chess else ['team name', 'player'],
        keep='first'
    )
    with pd.ExcelWriter(output_path, engine='openpyxl', mode='a' if os.path.exists(output_path) else 'w',
                        if_sheet_exists='replace') as writer:
        final_df.to_excel(writer, sheet_name=sport.capitalize(), index=False)

    return group_stage_matches, {match_stage: next_matches, **knockout}
