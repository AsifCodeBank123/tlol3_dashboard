import streamlit as st
import random
import pandas as pd
from itertools import combinations
from fixtures_modules.constants import (
    TOURNAMENT_STRUCTURE,
    ROUND_MATCH_COLS,
    ROUND_RESULT_COLS,
    WINNER_EMOJI,
    LOSER_EMOJI,
    ROUND_SIZE
)
from fixtures_modules.database_handler import update_match_number


def normalize_identifier(row, is_chess):
    return row["player"].strip() if is_chess else row["pair"].strip()


# ✅ Create group stage pairs without same-team conflicts
def generate_group_stage_pairs(seed3_df, is_chess):
    entries = seed3_df.to_dict("records")
    random.shuffle(entries)

    pairs = []
    used = set()

    for i, j in combinations(range(len(entries)), 2):
        team1 = entries[i]["team_name"]
        team2 = entries[j]["team_name"]
        id1 = normalize_identifier(entries[i], is_chess)
        id2 = normalize_identifier(entries[j], is_chess)

        if team1 != team2 and id1 not in used and id2 not in used:
            pairs.append((entries[i], entries[j]))
            used.add(id1)
            used.add(id2)

        if len(pairs) >= 8:
            break

    return pairs


# ✅ Build group match records and update Google Sheet with match numbers
def build_group_stage_matches(group_pairs, df, sheet_name, is_chess):
    group_stage = []
    id_col = "player" if is_chess else "pair"
    match_col = "group_match_no"

    for i, (p1, p2) in enumerate(group_pairs):
        match_no = i + 1

        for p in [p1, p2]:
            identifier = normalize_identifier(p, is_chess)
            existing = df.loc[df[id_col] == identifier, match_col].iloc[0] if match_col in df.columns and not df[df[id_col] == identifier].empty else ""
            if not str(existing).strip():
                update_match_number(sheet_name, id_col, identifier, match_col, match_no)

        team1 = p1["team_name"]
        team2 = p2["team_name"]

        result1 = str(p1.get("group_result", "")).strip().lower()
        result2 = str(p2.get("group_result", "")).strip().lower()

        if result1 == "w":
            team1 += WINNER_EMOJI
            team2 += LOSER_EMOJI
        elif result2 == "w":
            team2 += WINNER_EMOJI
            team1 += LOSER_EMOJI

        players1 = (p1["player"],) if is_chess else (p1["player_1"], p1["player_2"])
        players2 = (p2["player"],) if is_chess else (p2["player_1"], p2["player_2"])

        group_stage.append({
            "team 1": team1,
            "players 1": players1,
            "team 2": team2,
            "players 2": players2
        })

    return group_stage


# ✅ Build knockout bracket
def build_knockout_round(seed1_df, seed2_df, group_pairs, df, sheet_name, is_chess):
    match_stage = "Super 32" if is_chess else "Super 16"
    match_col = ROUND_MATCH_COLS[match_stage]
    result_col = ROUND_RESULT_COLS[match_stage]
    id_col = "player" if is_chess else "pair"
    first_round = match_stage

    total_matches = ROUND_SIZE[match_stage]
    knockout_matches = {i: [None, None] for i in range(1, total_matches + 1)}

    def label(row):
        team_name = row['team_name']
        result = str(row.get(result_col, "")).strip().lower()
        if result == "w":
            team_name += WINNER_EMOJI
        elif result == "l":
            team_name += LOSER_EMOJI
        return f"{team_name}\n({row[id_col]})"

    used_match_numbers = set()
    for _, row in pd.concat([seed1_df, seed2_df]).iterrows():
        match_no = str(row.get(match_col, "")).strip()
        if match_no.isdigit():
            used_match_numbers.add(int(match_no))

    available_match_nos = [i for i in range(1, total_matches + 1) if i not in used_match_numbers]

    for df_group, slot in [(seed1_df, 0), (seed2_df, 1)]:
        for _, row in df_group.iterrows():
            match_no = row.get(match_col)
            identifier = row[id_col]

            if pd.isna(match_no) or not str(match_no).strip().isdigit():
                if available_match_nos:
                    match_no = available_match_nos.pop(0)
                    update_match_number(sheet_name, id_col, identifier, match_col, match_no)
                else:
                    continue

            match_no = int(match_no)
            knockout_matches[match_no][slot] = label(row)

    winners = []
    for i, (p1, p2) in enumerate(group_pairs):
        r1 = str(p1.get("group_result", "")).strip().lower()
        r2 = str(p2.get("group_result", "")).strip().lower()

        if r1 == "w":
            winners.append(p1)
        elif r2 == "w":
            winners.append(p2)
        else:
            winners.append({
                "team_name": f"Winner Match {i+1}",
                id_col: f"{p1[id_col]} / {p2[id_col]}"
            })

    win_index = 0
    for match_no in sorted(knockout_matches.keys()):
        for slot in [0, 1]:
            if knockout_matches[match_no][slot] is None and win_index < len(winners):
                winner = winners[win_index]
                knockout_matches[match_no][slot] = label(winner)

                identifier = winner[id_col]
                existing = ""
                if match_col in df.columns:
                    filtered = df.loc[df[id_col] == identifier, match_col]
                    if not filtered.empty:
                        existing = filtered.iloc[0]

                if not str(existing).strip():
                    update_match_number(sheet_name, id_col, identifier, match_col, match_no)

                win_index += 1

    return {
        first_round: [(k, *v) for k, v in knockout_matches.items() if v[0] and v[1]]
    }
