import streamlit as st
import pandas as pd
import os
import base64

from fixtures_modules.database_handler import load_sheet_as_df
from fixtures_modules.constants import SPREADSHEET_ID2


def encode_image_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""


def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def normalize_col(col):
    """Convert a column name to lowercase with underscores, matching df_teams naming."""
    return col.strip().lower().replace(" ", "_")

def render_leaderboard():
    load_global_styles()

    # Load team data
    df_teams = load_sheet_as_df("points", spreadsheet_id=SPREADSHEET_ID2)
    df_teams.columns = df_teams.columns.str.strip().str.lower().str.replace(" ", "_")
    df_teams.fillna(0, inplace=True)

    #print("Columns in df_teams:", df_teams.columns.tolist())

    # Define sports and participation columns (pretty names for display)
    sport_columns_pretty = [
        'Table Tennis', 'Chess', 'Carrom', 'Foosball', 'Badminton', 'Cricket',
        'Bonus Card Point', 'Underdog Uprising Points', 'Olympics'
    ]
    participation_column_map_pretty = {
        'Foosball': 'Foosball Participation',
        'Table Tennis': 'Table Tennis Participation',
        'Carrom': 'Carrom Participation',
        'Badminton': 'Badminton Participation',
        'Chess': 'Chess Participation'
    }

    # Normalize mapping for actual DataFrame access
    sport_columns_norm = [normalize_col(s) for s in sport_columns_pretty]
    participation_column_map_norm = {
        normalize_col(sport): normalize_col(part_col)
        for sport, part_col in participation_column_map_pretty.items()
    }

    # Compute total points safely
    if "total_points" not in df_teams.columns:
        df_teams["total_points"] = 0

    for sport_col in sport_columns_norm:
        if sport_col in df_teams.columns:
            df_teams["total_points"] += pd.to_numeric(df_teams[sport_col], errors="coerce").fillna(0).astype(int)
        if sport_col in participation_column_map_norm:
            part_col = participation_column_map_norm[sport_col]
            if part_col in df_teams.columns:
                df_teams["total_points"] += pd.to_numeric(df_teams[part_col], errors="coerce").fillna(0).astype(int)

    # Player leaderboard
    display_cols = ['player_name', 'team_name', 'total_points'] + sport_columns_norm + list(participation_column_map_norm.values())
    df_players = df_teams[display_cols].copy()
    df_players.sort_values(by='total_points', ascending=False, inplace=True)
    df_players.reset_index(drop=True, inplace=True)
    df_players['rank'] = df_players.index + 1

    # Team leaderboard
    df_teams_grouped = df_teams.groupby('team_name')[['total_points']].sum().reset_index()
    df_teams_grouped.sort_values(by='total_points', ascending=False, inplace=True)
    df_teams_grouped.reset_index(drop=True, inplace=True)
    df_teams_grouped['rank'] = df_teams_grouped.index + 1

    team_logos = {
        "Gully Gang": encode_image_to_base64("assets/gg_logo.png"),
        "Badshah Blasters": encode_image_to_base64("assets/bb_logo.png"),
        "Rockstar Rebels": encode_image_to_base64("assets/rr_logo.png"),
        "Dabangg Dynamos": encode_image_to_base64("assets/dd_logo.png")
    }

    col1, col2 = st.columns(2, gap="large")

    # 🎯 Individual Leaderboard
    with col1:
        with st.expander("🎯 Individual Leaderboard", expanded=False):
            top_player_points = pd.to_numeric(df_players['total_points'], errors="coerce").max()
            for _, row in df_players.iterrows():
                rank = row['rank']
                player = row['player_name']
                team = row['team_name']
                points = pd.to_numeric(row['total_points'], errors="coerce")
                points = 0 if pd.isna(points) else int(points)

                delta = top_player_points - points
                delta_text = "Top!" if delta == 0 else f"▲ {delta}"

                if rank == 1:
                    card_class = "rank-glow-gold"
                elif rank == 2:
                    card_class = "rank-glow-silver"
                elif rank == 3:
                    card_class = "rank-glow-bronze"
                else:
                    card_class = "compact-leaderboard-card-lower"

                card = f"<div class='{card_class}'>"
                if delta_text:
                    card += f"<div class='delta-badge'>{delta_text}</div>"
                card += f"<div class='compact-rank-badge'>#{rank}</div>"

                progress_percentage = 0
                if pd.notna(points) and pd.notna(top_player_points) and top_player_points > 0:
                    progress_percentage = int((points / top_player_points) * 100)

                card += f"""
                    <div class="compact-player-name">{player}</div>
                    <div class="compact-team-name">{team}</div>
                    <div class="compact-points">Total Points: {points}</div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: {progress_percentage}%"></div>
                    </div>
                    <div class="sport-block-container">
                """

                # Sport-wise blocks
                for sport_pretty, sport_norm in zip(sport_columns_pretty, sport_columns_norm):
                    sport_score = pd.to_numeric(row.get(sport_norm, 0), errors="coerce")
                    sport_score = 0 if pd.isna(sport_score) else int(sport_score)

                    part_col = participation_column_map_norm.get(sport_norm)
                    if part_col:
                        part_score = pd.to_numeric(row.get(part_col, 0), errors="coerce")
                        sport_score += 0 if pd.isna(part_score) else int(part_score)

                    card += f"<div class='mini-sport-block'>{sport_pretty}: {sport_score}</div>"

                card += "</div></div>"
                st.markdown(card, unsafe_allow_html=True)

    # Bonus points
    unsold_points = {
        "Gully Gang": 150,
        "Rockstar Rebels": 150,
        "Dabangg Dynamos": 250,
        "Badshah Blasters": 150
    }
    bollywood_trivia_points = {
        "Gully Gang": 700,
        "Rockstar Rebels": 325,
        "Dabangg Dynamos": 625,
        "Badshah Blasters": 850
    }

    # 🏆 Team Leaderboard
    with col2:
        st.markdown("""
            <div class='leaderboard-title-section'>
                <div class='leaderboard-title'>🏆 Team Leaderboard</div>
            </div>
        """, unsafe_allow_html=True)

        top_team_points = pd.to_numeric(df_teams_grouped['total_points'], errors="coerce").max()
        for _, row in df_teams_grouped.iterrows():
            rank = row['rank']
            team = row['team_name']
            base_points = pd.to_numeric(row['total_points'], errors="coerce")
            base_points = 0 if pd.isna(base_points) else int(base_points)

            points = base_points + unsold_points.get(team, 0) + bollywood_trivia_points.get(team, 0)

            delta = top_team_points - points
            delta_text = "Top!" if delta == 0 else f"1st Rank Delta: {delta}"
            logo_base64 = team_logos.get(team, "")

            if rank == 1:
                card_class = "rank-glow-gold"
            elif rank == 2:
                card_class = "rank-glow-silver"
            elif rank == 3:
                card_class = "rank-glow-bronze"
            else:
                card_class = "compact-leaderboard-card-lower"

            card = f"<div class='{card_class}'>"
            card += f"<div class='delta-badge'>{delta_text}</div>"
            card += f"<div class='compact-rank-badge'>#{rank}</div>"

            if logo_base64:
                card += f"""
                    <div class='team-expander-header'>
                        <img src="data:image/png;base64,{logo_base64}" class="team-logo"/>
                        <span class='compact-player-name'>{team}</span>
                    </div>
                """
            else:
                card += f"<div class='compact-player-name'>{team}</div>"

            progress_percentage = 0
            if pd.notna(points) and pd.notna(top_team_points) and top_team_points > 0:
                progress_percentage = int((points / top_team_points) * 100)

            card += f"""<div class='compact-points'>Total Points: {points}</div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: {progress_percentage}%"></div>
                </div>
                <div class='sport-block-container'>
            """

            team_rows = df_teams[df_teams['team_name'] == team]
            for sport_pretty, sport_norm in zip(sport_columns_pretty, sport_columns_norm):
                sport_score = pd.to_numeric(team_rows[sport_norm].sum() if sport_norm in team_rows.columns else 0, errors="coerce")
                sport_score = 0 if pd.isna(sport_score) else int(sport_score)

                part_col = participation_column_map_norm.get(sport_norm)
                if part_col and part_col in team_rows.columns:
                    part_score = pd.to_numeric(team_rows[part_col].sum(), errors="coerce")
                    sport_score += 0 if pd.isna(part_score) else int(part_score)

                card += f"<div class='mini-sport-block'>{sport_pretty}: {sport_score}</div>"

            card += f"""
                </div>
                <div class="mini-sport-block bonus-highlight">Unsold Points: {unsold_points.get(team, 0)}</div>
                <div class="mini-sport-block bonus-highlight">Bollywood Trivia: {bollywood_trivia_points.get(team, 0)}</div>
            </div>
            """
            st.markdown(card, unsafe_allow_html=True)

            # Contribution expander
            with st.expander(f"👥 View Contribution - {team}"):
                team_players = df_players[df_players['team_name'] == team][['player_name', 'total_points']]
                team_players['total_points'] = pd.to_numeric(team_players['total_points'], errors="coerce").fillna(0).astype(int)
                team_players = team_players.sort_values(by='total_points', ascending=False)
                for _, player_row in team_players.iterrows():
                    st.markdown(f"""
                        <div class='player-contribution-row'>
                            <span class='player-name'>{player_row['player_name']}</span>
                            <span class='player-points'>{player_row['total_points']} pts</span>
                        </div>
                    """, unsafe_allow_html=True)

def render():
    render_leaderboard()