import streamlit as st
import pandas as pd
import os

def render():
    st.subheader("🛡️ TLOL3 Superhero Teams")

    try:
        df = pd.read_csv(os.path.join("reports", "teams.csv"))
    except FileNotFoundError:
        st.error("teams.csv not found in reports folder.")
        return

    # Drop the first column ("Team Name", "Player 1", etc.)
    df = df.iloc[:, 1:]

    # Extract team names from header row
    team_names = df.columns.tolist()

    # Get captains from first row
    captains = df.iloc[0].to_dict()

    # Remove captain row to only keep players
    df_players = df.iloc[1:].reset_index(drop=True)

    # Assign default colors (customize as needed)
    team_colors = {
        "Team Captain": "#ff5733",
        "Team Thor": "#3385ff",
        "Team Stark": "#33cc99",
        "Team Panther": "#b2eb18",
    }

    # Create columns
    team_cols = st.columns(len(team_names))

    for idx, team in enumerate(team_names):
        with team_cols[idx]:
            color = team_colors.get(team, "#555")
            captain = captains.get(team, "Unknown")

            st.markdown(f"""
                <div style='background-color:{color}; padding:16px; border-radius:12px;
                            margin-bottom:10px; text-align:center; color:black;
                            box-shadow:1px 1px 8px rgba(0,0,0,0.1);'>
                    <h4>{team}</h4>
                    <p style='font-size:14px;'><strong>👑 Captain:</strong> {captain}</p>
                    <ul style='list-style:none; padding-left:0; font-size:13px;'>
            """, unsafe_allow_html=True)

            # Add players for the team
            players = df_players[team].dropna().tolist()
            for p in players:
                st.markdown(f"<li>🧍 {p}</li>", unsafe_allow_html=True)

            st.markdown("</ul></div>", unsafe_allow_html=True)
