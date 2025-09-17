import streamlit as st
import pandas as pd
import itertools
import os

from fixtures_modules.database_handler import sheet_exists, load_sheet_as_df

# ----------------------
# Helpers
# ----------------------

def safe_val(v):
    """Replace NaN/None/empty with TBD."""
    if pd.isna(v) or str(v).strip().lower() in ["nan", "none", ""]:
        return "TBD"
    return v

def load_global_styles():
    """Load global CSS from assets."""
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_global_styles()

# ----------------------
# Config
# ----------------------

REPORTS_PATH = "reports/seeded_teams.xlsx"

FIXTURES_SHEET = "Fixtures_Table tennis"

GROUPS = {
    "A": ["GG1", "BB2", "DD3", "RR4", "GG5", "BB6"],
    "B": ["BB1", "DD2", "RR3", "GG4", "BB5", "RR7"],
    "C": ["DD1", "RR2", "GG3", "BB4", "DD5", "RR6"],
    "D": ["RR1", "GG2", "BB3", "DD4", "RR5", "DD6"]
}

TEAM_CODES = {
    "Gully Gang": "GG",
    "Badshah Blasters": "BB",
    "Dabangg Dynamos": "DD",
    "Rockstar Rebels": "RR"
}

# ----------------------
# Fixtures Generation
# ----------------------

def generate_round_robin(teams):
    """Round robin pairs for a group."""
    return list(itertools.combinations(teams, 2))

def build_group_fixtures(seed_df):
    """Generate fixtures for group stage with team & pair mapping."""
    fixtures = []

    for group, codes in GROUPS.items():
        match_id = 1   # reset per group
        for t1, t2 in generate_round_robin(codes):
            team1 = seed_df.loc[seed_df["code"] == t1, ["team_name", "pair"]].values[0]
            team2 = seed_df.loc[seed_df["code"] == t2, ["team_name", "pair"]].values[0]

            fixtures.append({
                "match_id": match_id,
                "round": "Group Stage",
                "group": group,
                "team1": team1[0], "pair1": team1[1],
                "team2": team2[0], "pair2": team2[1],
                "result": ""
            })
            match_id += 1
    return pd.DataFrame(fixtures)


def build_knockout_fixtures():
    """Quarter, Semi, Final placeholders with TBD pairs."""
    data = [
        {"round": "Quarter Final", "match_id": "QF1", "team1": "A1", "pair1": None, "team2": "D2", "pair2": None},
        {"round": "Quarter Final", "match_id": "QF2", "team1": "B2", "pair1": None, "team2": "C1", "pair2": None},
        {"round": "Quarter Final", "match_id": "QF3", "team1": "C2", "pair1": None, "team2": "D1", "pair2": None},
        {"round": "Quarter Final", "match_id": "QF4", "team1": "A2", "pair1": None, "team2": "B1", "pair2": None},
        {"round": "Semi Final", "match_id": "SF1", "team1": "Winner QF1", "pair1": None, "team2": "Winner QF2", "pair2": None},
        {"round": "Semi Final", "match_id": "SF2", "team1": "Winner QF3", "pair1": None, "team2": "Winner QF4", "pair2": None},
        {"round": "Final", "match_id": "F1", "team1": "Winner SF1", "pair1": None, "team2": "Winner SF2", "pair2": None}
    ]
    return pd.DataFrame(data)

def build_group_standings(fixtures_df):
    """Create pair-wise standings table from group stage fixtures only."""
    # ✅ filter only group-stage matches
    group_stage_df = fixtures_df[fixtures_df["round"] == "Group Stage"].copy()

    standings = []
    groups = group_stage_df["group"].unique() if "group" in group_stage_df.columns else ["All"]

    for group in groups:
        group_df = group_stage_df[group_stage_df["group"] == group]

        # collect unique pairs
        pairs = pd.concat([
            group_df[["pair1", "team1"]].rename(columns={"pair1": "pair", "team1": "team"}),
            group_df[["pair2", "team2"]].rename(columns={"pair2": "pair", "team2": "team"})
        ]).drop_duplicates()

        for _, row in pairs.iterrows():
            pair, team = row["pair"], row["team"]

            matches = group_df[
                ((group_df["pair1"] == pair) | (group_df["pair2"] == pair))
                & (group_df["result"].notna()) & (group_df["result"] != "")
            ]

            mp = len(matches)
            w = (((matches["pair1"] == pair) & (matches["result"] == "w")) |
                 ((matches["pair2"] == pair) & (matches["result"] == "l"))).sum()
            l = (((matches["pair1"] == pair) & (matches["result"] == "l")) |
                 ((matches["pair2"] == pair) & (matches["result"] == "w"))).sum()

            standings.append({
                "Group": group,
                "Pair": pair,
                "Team": team,
                "MP": int(mp),
                "W": int(w),
                "L": int(l),
                "PTS": int(w) * 3
            })

    return (
        pd.DataFrame(standings)
        .drop_duplicates(subset=["Group", "Pair"])   # avoid dup rows
        .sort_values(["Group", "PTS", "W"], ascending=[True, False, False])
        .reset_index(drop=True)
    )


# ----------------------
# Render in Streamlit
# ----------------------

def render_table_tennis_fixtures():
    """Render fixtures for Table Tennis in Streamlit."""

    sheet_name = "Fixtures_Table tennis"  # Exact match

    # ✅ Check if sheet exists
    if not sheet_exists(sheet_name):
        st.warning("⚠ No fixtures available for Table Tennis yet.")
        return

    # ✅ Read sheet using the correct name
    fixtures_df = load_sheet_as_df(sheet_name)

    # ✅ Validate data
    if fixtures_df is None or fixtures_df.empty:
        st.warning(f"⚠ Fixtures data is empty for '{sheet_name}'.")
        return
    
    st.subheader("📊 Group Stage Standings")

    standings_df = build_group_standings(fixtures_df)

    for group in GROUPS.keys():
        st.markdown(f"### Group {group} Standings")
        group_df = standings_df[standings_df["Pair"].isin(
            pd.concat([
                fixtures_df[fixtures_df["group"] == group]["pair1"],
                fixtures_df[fixtures_df["group"] == group]["pair2"]
            ])
        )]
        st.dataframe(group_df.reset_index(drop=True), use_container_width=True, hide_index=True)
    
    # --- Render only if fixtures exist ---
    st.subheader("📋 Group Stage Fixtures")
    group_df = fixtures_df[fixtures_df["round"] == "Group Stage"]

    for group in GROUPS.keys():
        with st.expander(f"Group {group} Fixtures"):
            group_matches = group_df[group_df["group"] == group].to_dict("records")

            rows, cols = 5, 3  # 5 rows × 3 columns grid
            for i in range(rows):
                col_list = st.columns(cols)
                for j in range(cols):
                    idx = i * cols + j
                    if idx < len(group_matches):
                        row = group_matches[idx]
                        with col_list[j]:
                            st.markdown(
                            f"""
                            <div class="fixture-card">
                                <div class="match-id">Match {row['match_id']}</div>
                                <div class="fixture-vs">
                                    <div class="fixture-side">
                                        <span class="player-name">{safe_val(row['pair1'])}</span>
                                        <div class="team-name">({safe_val(row['team1'])})</div>
                                    </div>
                                    <div class="vs-text">🆚</div>
                                    <div class="fixture-side">
                                        <span class="player-name">{safe_val(row['pair2'])}</span>
                                        <div class="team-name">({safe_val(row['team2'])})</div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                            

    st.subheader("🏆 Knockout Fixtures")

    knockout_df = fixtures_df[fixtures_df["round"].isin(["Quarter Final", "Semi Final", "Final"])]

    KNOCKOUT_STRUCTURE = {
        "Quarter Final": {"matches": 4, "label": "Quarter Finals"},
        "Semi Final": {"matches": 2, "label": "Semi Finals"},
        "Final": {"matches": 1, "label": "Final"},
    }

    for stage, meta in KNOCKOUT_STRUCTURE.items():
        st.markdown(f"### {meta['label']}")
        stage_df = knockout_df[knockout_df["round"] == stage].to_dict("records")

        cols = st.columns(meta["matches"])
        for i, col in enumerate(cols):
            if i < len(stage_df):
                row = stage_df[i]
                with col:
                    st.markdown(
                        f"""
                        <div class="knockout-card">
                            <div class="match-id">Match {row['match_id']}</div>
                            <div class="fixture-vs">
                                <div class="fixture-side">
                                    <span class="player-name">{safe_val(row['pair1'])}</span>
                                    <div class="team-name">({safe_val(row['team1'])})</div>
                                </div>
                                <div class="vs-text">🆚</div>
                                <div class="fixture-side">
                                    <span class="player-name">{safe_val(row['pair2'])}</span>
                                    <div class="team-name">({safe_val(row['team2'])})</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                )
