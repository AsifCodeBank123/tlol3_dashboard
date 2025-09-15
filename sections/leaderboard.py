import streamlit as st
import pandas as pd
import os
import base64

from fixtures_modules.database_handler import load_sheet_as_df
from fixtures_modules.constants import SPREADSHEET_ID2
from utils.constants import player_avatars


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

# --- Global Points Table Section ---
def render_points_info():
    # --- Points Table ---
    st.markdown("<div class='shared-section-title'>🏅 Tournament Points System</div>", unsafe_allow_html=True)
    with st.expander("View", expanded=False):

        points_data = {
            "Type": ["Participation", "Quarter Finals", "Semi Finals", "Runner Up", "Winner/Champion"],
            "Points": ["50 Points", "250 Points", "500 Points", "750 Points", "1000 Points"]
        }
        points_df = pd.DataFrame(points_data)
    
        st.dataframe(points_df, use_container_width=True, hide_index=True)

    # Detailed info inside an Expander
    with st.expander("ℹ️ How Points Are Calculated (Click to Expand)"):
        st.markdown("""
        -Every Star Participating (Playing the event) will earn 50 points, in case of doubles event if a partner not attending the event, the attending player will earn 50 points

-As the Star/s (Singles/Doubles Event) progresses through the event, He would earn 100 points in total(50 each if doubles) if he reached Quarters and if he loses (4th)

-As the Star/s (Singles/Doubles Event) progresses through the event, He would earn 250 points if he reached semi-Finals and if he loses (3rd )

-Winners and Runners up (Singles/Doubles Event) would earn 1000 and 500 points

-Winners and Runners up (Doubles Event) would earn 1000 (500 each if doubles) and 500 points (250 each if doubles)

-These points are important for the Star as well as the Team of Stars for the Final Prizes (End Game)

-Participation points are only awarded for Singles and Doubles event formats.

**Note:**  
Tournament events follow this system. One-time events may give smaller points (e.g., <500 for winners).
        """, unsafe_allow_html=True)

    # --- Power Cards Section in Expander ---
    with st.expander("🎴 Power Cards Details", expanded=False):
        power_cards_data = [
            {
                "Sr": 1,
                "Event": "Overall",
                "Card": "Underdog Uprising",
                "Description": "Underdogs (unsold players) will win 2x points if reached quarterfinal and above. Player Points will be 2x.",
                "When it should be called": "Automatically after the Auction",
            },
            {
                "Sr": 2,
                "Event": "Overall",
                "Card": "Double-e-Risk",
                "Description": "Doubles the points of a selected event. The event points are multiplied by a factor (2x). If the event is lost then it will be -500.",
                "When it should be called": "Before the Event Starts",
            },
            {
                "Sr": 3,
                "Event": "Overall",
                "Card": "Jodi Breakers",
                "Description": "Swap two members between teams for one event (Before Rosters when Participation list is finalized). If the swapped player helps the new team win, the playing team gets 200 points and the team who has used the card gets -200 Points. If the swapped player underperforms, the Team who has used the card gets 200 points.",
                "When it should be called": "After the rosters are done",
            },
            {
                "Sr": 4,
                "Event": "Overall",
                "Card": "Shakti Bonus",
                "Description": "Female Pairing (Excluding chess) reaching Quarters and Above would get 2x points.",
                "When it should be called": "Automatically after the Auction",
            },
        ]

        df_power_cards = pd.DataFrame(power_cards_data)
        st.dataframe(df_power_cards, use_container_width=True, hide_index=True)


def render_leaderboard():
    load_global_styles()

    # Background
    image_path = "assets/lead_bg.jpg"
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            bg_img = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""<style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{bg_img}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>""",
            unsafe_allow_html=True,
        )

    # Load team data
    df_teams = load_sheet_as_df("points", spreadsheet_id=SPREADSHEET_ID2)
    df_teams.columns = df_teams.columns.map(str).str.strip().str.lower().str.replace(" ", "_")

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
        st.markdown("""
            <style>
            .leaderboard-title {
                color: #FFD700; /* gold */
                font-size: 2rem;
                font-weight: bold;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            }
            </style>
            <div class='leaderboard-title-section'>
                <div class='leaderboard-title'>🎯 Individual Leaderboard</div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("View", expanded=False):
            # Sort players by total_points (descending) and assign rank with ties
            df_players['rank'] = (
                df_players['total_points']
                .rank(method='min', ascending=False)  # same score gets same rank
                .astype(int)
            )

            # Then loop
            top_player_points = pd.to_numeric(df_players['total_points'], errors="coerce").max()
            for _, row in df_players.sort_values(by=['rank', 'player_name']).iterrows():
                rank = row['rank']
                player = row['player_name']
                team = row['team_name']
                points = int(row['total_points']) if pd.notna(row['total_points']) else 0

                avatar_url = player_avatars.get(player, "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

                
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
                    <div class="leaderboard-avatar">
                        <img src="{avatar_url}" alt="{player} avatar"/>
                    </div>
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
        <style>
        .leaderboard-title {
            color: #FFD700; /* gold */
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        </style>
        <div class='leaderboard-title-section'>
            <div class='leaderboard-title'>🏆 Team Leaderboard</div>
        </div>
    """, unsafe_allow_html=True)


        # Calculate adjusted points for all teams first
        df_teams_grouped["adjusted_points"] = (
            pd.to_numeric(df_teams_grouped["total_points"], errors="coerce").fillna(0).astype(int)
            + df_teams_grouped["team_name"].map(unsold_points).fillna(0).astype(int)
            + df_teams_grouped["team_name"].map(bollywood_trivia_points).fillna(0).astype(int)
        )

        # Sort teams by adjusted_points and assign rank with ties
        df_teams_grouped['rank'] = (
            df_teams_grouped['adjusted_points']
            .rank(method='min', ascending=False)
            .astype(int)
        )

        top_team_points = df_teams_grouped["adjusted_points"].max()
        for _, row in df_teams_grouped.sort_values(by=['rank', 'team_name']).iterrows():
            rank = row['rank']
            team = row['team_name']
            points = row["adjusted_points"]

            delta = top_team_points - points
            delta_text = "Top!" if delta == 0 else f"1st Rank Delta: {delta}"

  

            logo_base64 = team_logos.get(row["team_name"], "")

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
                sport_score = (
                   pd.to_numeric(team_rows[sport_norm], errors="coerce").fillna(0).sum()
                   if sport_norm in team_rows.columns else 0
                )
                
                
                sport_score = 0 if pd.isna(sport_score) else int(sport_score)

                part_col = participation_column_map_norm.get(sport_norm)
                if part_col and part_col in team_rows.columns:
                    part_score = pd.to_numeric(team_rows[part_col], errors="coerce").fillna(0).sum()
            
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
