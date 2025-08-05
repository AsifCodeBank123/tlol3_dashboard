# constants.py/fixtures_modules

# ✅ Tournament structure per sport
TOURNAMENT_STRUCTURE = {
    "chess": ["Super 32", "Super 16", "Quarter Finals", "Semi Finals", "Final"],
    "default": ["Super 16", "Quarter Finals", "Semi Finals", "Final"]
}

# ✅ Match number column name for each round
ROUND_MATCH_COLS = {
    "Super 32": "super_32_match_no",
    "Super 16": "super_16_match_no",
    "Quarter Finals": "quarter_match_no",
    "Semi Finals": "semi_match_no",
    "Final": "final_match_no"
}

# ✅ Match result column name for each round
ROUND_RESULT_COLS = {
    "Super 32": "super_32_result",
    "Super 16": "super_16_result",
    "Quarter Finals": "quarter_result",
    "Semi Finals": "semi_result",
    "Final": "final_result"
}

# ✅ Emoji tags for display (optional)
WINNER_EMOJI = " 🏆"
LOSER_EMOJI = " 🦆"

# ✅ Sheet ID (can be overridden from env or passed)
SPREADSHEET_ID = "1854rtEWHjp1-akVlSIzjdR_PxUW1hdKxnU2hOp5KPTw"

# ✅ Round size config
ROUND_SIZE = {
    "Super 32": 16,
    "Super 16": 8,
    "Quarter Finals": 4,
    "Semi Finals": 2,
    "Final": 1
}
