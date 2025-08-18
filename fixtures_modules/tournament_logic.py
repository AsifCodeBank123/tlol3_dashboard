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


# ==============================
# Utility Functions
# ==============================

def normalize_identifier(row, is_chess: bool) -> str:
    """Return identifier: player for chess, pair for others."""
    return row["player"].strip() if is_chess else row["pair"].strip()


def label_with_result(row, is_chess: bool, round_name: str) -> str:
    """Return display label for one player/team with W/L emoji."""
    if row is None:
        return "TBD"

    team_name = row["team_name"]
    result_col = ROUND_RESULT_COLS[round_name]
    result = str(row.get(result_col, "")).strip().lower()

    if result == "w":
        team_name += WINNER_EMOJI
    elif result == "l":
        team_name += LOSER_EMOJI

    return team_name


# ==============================
# Group Stage
# ==============================

def build_group_stage_pairs(seed3_df, is_chess: bool, target_pairs: int):
    """Create group stage pairs ensuring no same-team pairing."""
    entries = seed3_df.to_dict("records")
    random.shuffle(entries)

    pairs, used = [], set()

    for i, j in combinations(range(len(entries)), 2):
        team1 = entries[i]["team_name"]
        team2 = entries[j]["team_name"]

        id1 = normalize_identifier(entries[i], is_chess)
        id2 = normalize_identifier(entries[j], is_chess)

        if team1 != team2 and id1 not in used and id2 not in used:
            pairs.append((entries[i], entries[j]))
            used.add(id1)
            used.add(id2)

            if len(pairs) >= target_pairs:
                break

    return pairs


def build_group_stage_matches(group_pairs, df, sheet_name: str, is_chess: bool):
    """Create group stage match data with W/L icons, update sheet if match_no missing."""
    group_stage = []
    id_col = "player" if is_chess else "pair"
    match_col = "group_match_no"

    for i, (p1, p2) in enumerate(group_pairs):
        match_id = i + 1

        # update missing match numbers in sheet
        for p in [p1, p2]:
            identifier = normalize_identifier(p, is_chess)
            existing = (
                df.loc[df[id_col] == identifier, match_col].iloc[0]
                if match_col in df.columns and not df[df[id_col] == identifier].empty
                else ""
            )
            if not str(existing).strip():
                update_match_number(sheet_name, id_col, identifier, match_col, match_id)

        # format labels and players
        team1_label = label_with_result(p1, is_chess, "Group Stage")
        team2_label = label_with_result(p2, is_chess, "Group Stage")

        players1 = [p1["player"]] if is_chess else [p1["player_1"], p1["player_2"]]
        players2 = [p2["player"]] if is_chess else [p2["player_1"], p2["player_2"]]

        group_stage.append({
            "match_id": match_id,
            "team 1": team1_label,
            "players 1": players1,
            "team 2": team2_label,
            "players 2": players2,
        })

    return group_stage


# ==============================
# Knockout Stage
# ==============================

def build_initial_knockout(seed1_df, seed2_df, group_winners, df, sheet_name, is_chess, round_name):
    """
    Place Seed-1 and Seed-2 into fixed match numbers by round, then fill the rest with group winners.
    Slot convention: slot 0 = left/top, slot 1 = right/bottom.
    """
    match_col = ROUND_MATCH_COLS[round_name]
    id_col = "player" if is_chess else "pair"
    total_matches = ROUND_SIZE[round_name]
    knockout_matches = {i: [None, None] for i in range(1, total_matches + 1)}

    # --- Preferred match numbers for seeds (by round) ---
    if round_name == "Super 16":
        seed1_pref = [1, 4, 5, 8]
        seed2_pref = [7, 6, 3, 2]
    elif round_name == "Super 32":
        seed1_pref = [1, 4, 15, 16]
        seed2_pref = [2, 3, 13, 14]
    else:
        # No special pattern for other rounds (shouldn't be called for them anyway)
        seed1_pref = []
        seed2_pref = []

    # Track already-used match numbers coming from the sheet (if any)
    used_match_numbers = set()
    for _, row in pd.concat([seed1_df, seed2_df]).iterrows():
        m = str(row.get(match_col, "")).strip()
        if m.isdigit():
            used_match_numbers.add(int(m))

    # Helper: choose a match number for a seed from preferred list (then fallback)
    def choose_match_no_for_seed(slot_index: int, preferred_list: list[int]) -> int | None:
        # first try preferred slots
        for m in preferred_list:
            if 1 <= m <= total_matches and knockout_matches[m][slot_index] is None:
                if m not in used_match_numbers:
                    return m
        # fallback: first free slot anywhere
        for m in range(1, total_matches + 1):
            if knockout_matches[m][slot_index] is None and m not in used_match_numbers:
                return m
        # as a last resort, allow reuse if the slot is free (handles prefilled other slot)
        for m in range(1, total_matches + 1):
            if knockout_matches[m][slot_index] is None:
                return m
        return None

    # --- Place Seed-1 (slot 0) following preferred positions ---
    for _, row in seed1_df.iterrows():
        match_no = row.get(match_col)
        identifier = row[id_col]
        if pd.isna(match_no) or not str(match_no).strip().isdigit():
            chosen = choose_match_no_for_seed(0, seed1_pref)
            if chosen is not None:
                update_match_number(sheet_name, id_col, identifier, match_col, chosen)
                match_no = chosen
            else:
                continue  # no room; should not happen
        match_no = int(match_no)
        knockout_matches[match_no][0] = row
        used_match_numbers.add(match_no)

    # --- Place Seed-2 (slot 1) following preferred positions ---
    for _, row in seed2_df.iterrows():
        match_no = row.get(match_col)
        identifier = row[id_col]
        if pd.isna(match_no) or not str(match_no).strip().isdigit():
            chosen = choose_match_no_for_seed(1, seed2_pref)
            if chosen is not None:
                update_match_number(sheet_name, id_col, identifier, match_col, chosen)
                match_no = chosen
            else:
                continue
        match_no = int(match_no)
        knockout_matches[match_no][1] = row
        used_match_numbers.add(match_no)

    # --- Fill remaining empty slots with group winners ---
    for winner in group_winners:
        placed = False
        for match_no in range(1, total_matches + 1):
            # try slot 0 then slot 1
            for slot in [0, 1]:
                if knockout_matches[match_no][slot] is None:
                    knockout_matches[match_no][slot] = winner
                    # if this winner is a real player/pair (not a placeholder), write match_no back
                    if not str(winner[id_col]).startswith("W"):
                        existing = df.loc[df[id_col] == winner[id_col], match_col]
                        if existing.empty or not str(existing.iloc[0]).strip():
                            update_match_number(sheet_name, id_col, winner[id_col], match_col, match_no)
                    placed = True
                    break
            if placed:
                break

    # Return [(match_no, left_row, right_row)]
    return [(k, v[0], v[1]) for k, v in knockout_matches.items()]



def generate_next_round(prev_matches, df, sheet_name: str, is_chess: bool, prev_round: str, current_round: str):
    """Generate next knockout round based on previous match results."""
    if not current_round:
        return []

    id_col = "player" if is_chess else "pair"
    match_col = ROUND_MATCH_COLS[current_round]
    result_col = ROUND_RESULT_COLS[prev_round]

    winners = []
    for match_no, p1_row, p2_row in prev_matches:
        winner_row = None
        for row in [p1_row, p2_row]:
            if row is None or str(row[id_col]).startswith("W"):
                continue
            if str(row.get(result_col, "")).strip().lower() == "w":
                winner_row = row
                break

        if winner_row is None:
            winners.append({"team_name": f"Winner Match {match_no}", id_col: f"W{match_no}"})
        else:
            winners.append(winner_row)

    knockout_matches = []
    for i in range(0, len(winners), 2):
        if i + 1 < len(winners):
            p1, p2 = winners[i], winners[i + 1]
            match_no = i // 2 + 1

            # update missing match numbers
            for p in [p1, p2]:
                if not str(p[id_col]).startswith("W"):
                    existing = df.loc[df[id_col] == p[id_col], match_col]
                    if existing.empty or not str(existing.iloc[0]).strip():
                        update_match_number(sheet_name, id_col, p[id_col], match_col, match_no)

            knockout_matches.append((match_no, p1, p2))

    return knockout_matches


def build_full_knockout_tree(seed1_df, seed2_df, seed3_df, df, sheet_name: str, is_chess: bool):
    """Generate complete knockout tree from group stage → finals."""
    target_pairs = ROUND_SIZE.get("Super 32" if is_chess else "Super 16", 8)
    group_pairs = build_group_stage_pairs(seed3_df, is_chess, target_pairs)

    id_col = "player" if is_chess else "pair"
    group_winners = []

    for i, (p1, p2) in enumerate(group_pairs):
        r1 = str(p1.get("group_result", "")).strip().lower()
        r2 = str(p2.get("group_result", "")).strip().lower()

        if r1 == "w":
            group_winners.append(p1)
        elif r2 == "w":
            group_winners.append(p2)
        else:
            group_winners.append({
                "team_name": f"Winner Match {i+1}",
                id_col: f"{p1[id_col]} / {p2[id_col]}"
            })

    rounds = {}
    current_round = "Super 16" if not is_chess else "Super 32"

    # initial knockout setup
    current_matches = build_initial_knockout(
        seed1_df, seed2_df, group_winners, df, sheet_name, is_chess, current_round
    )

    # progress through rounds
    while current_round:
        rounds[current_round] = [
            (m_no,
             label_with_result(p1, is_chess, current_round),
             label_with_result(p2, is_chess, current_round))
            for m_no, p1, p2 in current_matches
        ]

        next_round = TOURNAMENT_STRUCTURE.get(current_round, {}).get("next")
        current_matches = generate_next_round(
            current_matches, df, sheet_name, is_chess, current_round, next_round
        )
        current_round = next_round

    return rounds
