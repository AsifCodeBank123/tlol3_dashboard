import streamlit as st
import pandas as pd
import os

def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_leaderboard():
    load_global_styles()

    # Load team data
    df_teams = pd.read_csv("reports/teams.csv")
    df_teams.columns = df_teams.columns.str.strip()
    df_teams.fillna(0, inplace=True)

    # Define sports and participation columns
    sport_columns = [
        'Table Tennis', 'Chess', 'Carrom', 'Foosball', 'Badminton', 'Cricket',
        'Bonus Card Point', 'Underdog Uprising Points'
    ]
    participation_column_map = {
        'Foosball': 'Foosball Participation',
        'Table Tennis': 'Table Tennis Participation',
        'Carrom': 'Carrom Participation',
        'Badminton': 'Badminton Participation',
        'Chess': 'Chess Participation'
    }

    # Compute total points for each player
    df_teams['Total Points'] = 0
    for sport in sport_columns:
        df_teams['Total Points'] += df_teams[sport].astype(int)
        if sport in participation_column_map:
            df_teams['Total Points'] += df_teams[participation_column_map[sport]].astype(int)

    # Player leaderboard
    df_players = df_teams[['Player Name', 'Team Name', 'Total Points'] + sport_columns + list(participation_column_map.values())].copy()
    df_players.sort_values(by='Total Points', ascending=False, inplace=True)
    df_players.reset_index(drop=True, inplace=True)
    df_players['Rank'] = df_players.index + 1

    # Team leaderboard
    df_teams_grouped = df_teams.groupby('Team Name')[['Total Points']].sum().reset_index()
    df_teams_grouped.sort_values(by='Total Points', ascending=False, inplace=True)
    df_teams_grouped.reset_index(drop=True, inplace=True)
    df_teams_grouped['Rank'] = df_teams_grouped.index + 1

    col1, col2 = st.columns(2, border=True)

    with col1:
        st.markdown("""
            <div class='leaderboard-title-section'>
                <div class='leaderboard-title'>🎯 Individual Leaderboard</div>
            </div>
        """, unsafe_allow_html=True)

        for _, row in df_players.iterrows():
            rank = row['Rank']
            player = row['Player Name']
            team = row['Team Name']
            points = row['Total Points']

            card_class = "compact-leaderboard-card" if rank <= 3 else "compact-leaderboard-card-lower"
            badge_html = f"<div class='compact-rank-badge'>#{rank}</div>" if rank <= 3 else ""

            card = f"<div class='{card_class}'>"
            if badge_html:
                card += badge_html

            card += f"""
                <div class="compact-player-name">{player}</div>
                <div class="compact-team-name">{team}</div>
                <div class="compact-points">Total Points: {points}</div>
                <div class="sport-block-container">
            """

            for sport in sport_columns:
                sport_score = row.get(sport, 0)
                part_col = participation_column_map.get(sport)
                if part_col:
                    sport_score += row.get(part_col, 0)
                card += f"<div class='mini-sport-block'>{sport}: {int(sport_score)}</div>"

            card += "</div></div>"
            st.markdown(card, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class='leaderboard-title-section'>
                <div class='leaderboard-title'>🏆 Team Leaderboard</div>
            </div>
        """, unsafe_allow_html=True)

        for _, row in df_teams_grouped.iterrows():
            rank = row['Rank']
            team = row['Team Name']
            points = row['Total Points']

            card_class = "compact-leaderboard-card" if rank <= 3 else "compact-leaderboard-card-lower"
            badge_html = f"<div class='compact-rank-badge'>#{rank}</div>" if rank <= 3 else ""

            card = f"<div class='{card_class}'>"
            if badge_html:
                card += badge_html

            card += f"""
                <div class="compact-player-name">{team}</div>
                <div class="compact-points">Total Points: {points}</div>
                <div class="sport-block-container">
            """

            team_rows = df_teams[df_teams['Team Name'] == team]
            for sport in sport_columns:
                sport_score = team_rows[sport].sum()
                part_col = participation_column_map.get(sport)
                if part_col:
                    sport_score += team_rows[part_col].sum()
                card += f"<div class='mini-sport-block'>{sport}: {int(sport_score)}</div>"

            card += "</div></div>"
            st.markdown(card, unsafe_allow_html=True)

def render():
    render_leaderboard()