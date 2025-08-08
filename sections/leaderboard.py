import streamlit as st
import pandas as pd
import os
import base64


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

    team_logos = {
    "Gully Gang": encode_image_to_base64("assets/gg_logo.png"),
    "Badshah Blasters": encode_image_to_base64("assets/bb_logo.png"),
    "Rockstar Rebels": encode_image_to_base64("assets/rr_logo.png"),
    "Dabangg Dynamos": encode_image_to_base64("assets/dd_logo.png")
}


    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.expander("🎯 Individual Leaderboard", expanded=True):
            for _, row in df_players.iterrows():
                rank = row['Rank']
                player = row['Player Name']
                team = row['Team Name']
                points = row['Total Points']
                top_player_points = df_players['Total Points'].max()
                delta = top_player_points - points
                delta_text = "Top!" if delta == 0 else f"▲ {delta}"

                # Apply different class for top 3
                if rank == 1:
                    card_class = "rank-glow-gold"
                elif rank == 2:
                    card_class = "rank-glow-silver"
                elif rank == 3:
                    card_class = "rank-glow-bronze"
                else:
                    card_class = "compact-leaderboard-card-lower"

                # Start of card HTML
                card = f"<div class='{card_class}'>"

                # Top-right delta badge
                if delta_text:
                    card += f"<div class='delta-badge'>{delta_text}</div>"

                # Rank badge
                card += f"<div class='compact-rank-badge'>#{rank}</div>"

                # Player and team info
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
                for sport in sport_columns:
                    sport_score = row.get(sport, 0)
                    part_col = participation_column_map.get(sport)
                    if part_col:
                        sport_score += row.get(part_col, 0)
                    card += f"<div class='mini-sport-block'>{sport}: {int(sport_score)}</div>"

                # Close containers
                card += "</div></div>"

                # Render card
                st.markdown(card, unsafe_allow_html=True)


    # Extra points to be added manually
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
            top_team_points = df_teams_grouped['Total Points'].max()
            delta = top_team_points - points
            delta_text = "Top!" if delta == 0 else f"1st Rank Delta: {delta}"

            # Add unsold and Bollywood trivia points
            points += unsold_points.get(team, 0)
            points += bollywood_trivia_points.get(team, 0)
            
            logo_base64 = team_logos.get(team, "")

            # Apply glow styles
            if rank == 1:
                card_class = "rank-glow-gold"
            elif rank == 2:
                card_class = "rank-glow-silver"
            elif rank == 3:
                card_class = "rank-glow-bronze"
            else:
                card_class = "compact-leaderboard-card-lower"

            card = f"<div class='{card_class}'>"

            # Delta Badge
            card += f"<div class='delta-badge'>{delta_text}</div>"
            card += f"<div class='compact-rank-badge'>#{rank}</div>"

            # Logo + Team Name
            if logo_base64:
                card += f"""
                    <div class='team-expander-header'>
                        <img src="data:image/png;base64,{logo_base64}" class="team-logo"/>
                        <span class='compact-player-name'>{team}</span>
                    </div>
                """
            else:
                card += f"<div class='compact-player-name'>{team}</div>"

            progress_percentage = int((points / top_team_points) * 100)

            card += f"""<div class='compact-points'>Total Points: {points}</div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: {progress_percentage}%"></div>
                </div>
                <div class='sport-block-container'>
            """

            team_rows = df_teams[df_teams['Team Name'] == team]
            for sport in sport_columns:
                sport_score = team_rows[sport].sum()
                part_col = participation_column_map.get(sport)
                if part_col:
                    sport_score += team_rows[part_col].sum()
                card += f"<div class='mini-sport-block'>{sport}: {int(sport_score)}</div>"

            # Add bonus points
            card += f"""
                </div>
                <div class="mini-sport-block bonus-highlight">Unsold Points: {unsold_points.get(team, 0)}</div>
                <div class="mini-sport-block bonus-highlight">Bollywood Trivia: {bollywood_trivia_points.get(team, 0)}</div>
            </div>
            """

            st.markdown(card, unsafe_allow_html=True)

            # 👥 View Contribution Expander (outside team card)
            with st.expander(f"👥 View Contribution - {team}"):
                team_players = df_players[df_players['Team Name'] == team][['Player Name', 'Total Points']]
                team_players = team_players.sort_values(by='Total Points', ascending=False)

                for _, player_row in team_players.iterrows():
                    st.markdown(f"""
                        <div class='player-contribution-row'>
                            <span class='player-name'>{player_row['Player Name']}</span>
                            <span class='player-points'>{int(player_row['Total Points'])} pts</span>
                        </div>
                    """, unsafe_allow_html=True)


def render():
    render_leaderboard()