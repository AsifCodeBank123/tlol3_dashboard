import streamlit as st
import plotly.express as px
import pandas as pd

from modules.data_loader import load_and_merge_scores
from modules.avatar_utils import get_avatar_url
from modules.constants import TLOL_SPORTS

def render():

    st.markdown("""
    <style>
    .player-card {
        background: linear-gradient(135deg, #f0f0f3, #dce0e6);
        border-radius: 16px;
        padding: 16px;
        margin: 8px;
        font-size: 13px;
        color: #333;
        width: 100%;
        height: 290px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.1), -3px -3px 10px rgba(255,255,255,0.5);
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .player-card:hover {
        transform: scale(1.015);
        box-shadow: 6px 6px 12px rgba(0,0,0,0.15), -4px -4px 12px rgba(255,255,255,0.6);
    }
    .player-card img {
        border-radius: 50%;
        margin-bottom: 10px;
        border: 2px solid #f3d250;
    }
    .player-card hr {
        margin: 8px 0;
        border-top: 1px solid #f3d250;
    }
    .player-card .score-line {
        font-size: 12px;
        color: #444;
    }
    </style>
""", unsafe_allow_html=True)

    # ---------- TABS ---------- #
    tab1, tab2, tab3 = st.tabs(["🏷️ Auction Preview", "📊 Raw Stats", "📈 Insights & Breakdown"])

    # ---------- LOAD & PROCESS DATA ---------- #
    with st.spinner("Loading player data..."):
        df_players = load_and_merge_scores("reports")

        # Normalize column names to remove leading/trailing whitespace
        df_players.columns = df_players.columns.str.strip()

        
        # Map new column to Tier
        if "TLOL Auction Player Type" in df_players.columns:
            df_players["Tier"] = df_players["TLOL Auction Player Type"].astype(str).str.strip().str.lower().map({
    "icon": "Icon",
    "lead": "Lead",
    "rest": "Rest"
}).fillna("Rest")
            df_players["Tier"] = df_players["Tier"].where(df_players["Tier"].isin(["Icon", "Lead", "Rest"]), "Rest")
        else:
            df_players["Tier"] = "Rest"

        # Normalize availability column
        if "TLOL Availability" in df_players.columns:
            df_players["Availability"] = df_players["TLOL Availability"].astype(str).str.strip().str.lower()
        else:
            df_players["Availability"] = ""

        # Compute total score from all sport columns
        sport_columns = [col for col in df_players.columns if col in TLOL_SPORTS]
        df_players["Total Score"] = df_players[sport_columns].sum(axis=1)

    # ---------- TAB 1: AUCTION PREVIEW ---------- #
    with tab1:
        st.header("🎯 Auction Preview")

        # --- Filters ---
        col1, col2, col3 = st.columns(3)
        with col1:
            tier_filter = st.selectbox("🎖️ Player Type", ["All", "Icon", "Lead", "Rest"])
        with col2:
            sport_filter = st.selectbox("🏅 Sport", ["All"] + TLOL_SPORTS)
        with col3:
            gender_filter = st.selectbox("🧍 Gender", ["All", "M", "F"])

        # --- Apply Filters ---
        filtered = df_players.copy()
        if tier_filter != "All":
            filtered = filtered[filtered["Tier"] == tier_filter]
        if sport_filter != "All":
            filtered = filtered[filtered[sport_filter] > 0]
        if gender_filter != "All":
            filtered = filtered[filtered["Gender"] == gender_filter]

        st.markdown(f"### Showing {len(filtered)} players")

        # --- Player Card UI --- #
        def player_card(player_row):
            avatar_url = get_avatar_url(player_row["Player"], player_row["Gender"])
            sport_scores = {k: v for k, v in player_row.items() if k in sport_columns and v > 0}
            items = [f"{k}: {int(v)}" for k, v in sport_scores.items()]
            score_lines = [" | ".join(items[i:i+3]) for i in range(0, len(items), 3)]
            sport_line = "<br>".join(score_lines)

            # Availability dot
            availability = player_row.get("Availability", "")
            if "tentative" in availability:
                dot = "🟡"
            elif "available" in availability:
                dot = "🟢"
            else:
                dot = "⚪"

            html = f"""
            <div class="player-card">
                <div>
                    <img src="{avatar_url}" width="64" />
                    <div style="font-weight:bold; font-size:15px; margin-bottom:4px;">{player_row['Player']}</div>
                    <div style="font-size:13px; color:#555;">🏷️ <strong>{player_row['Tier']}</strong></div>
                    <div style="font-size:13px; margin-top:4px;">🧍 {player_row['Gender']} | {dot}</div>
                    <div style="margin-top:4px; font-size:13px;">🔢 Total Points: <strong>{int(player_row['Total Score'])}</strong></div>
                </div>
                <hr />
                <div class="score-line">{sport_line}</div>
            </div>
            """
            return html

        # --- Grid Layout ---
        num_cols = 3
        rows = [filtered[i:i + num_cols] for i in range(0, len(filtered), num_cols)]
        for row in rows:
            cols = st.columns(num_cols)
            for i, (_, player_row) in enumerate(row.iterrows()):
                with cols[i]:
                    st.markdown(player_card(player_row), unsafe_allow_html=True)

    # ---------- TAB 2: RAW STATS ---------- #
    with tab2:
        st.header("📊 Full Player Score Table")
        base_cols = ['Player', 'Gender', 'Tier', 'Total Score']
        display_cols = base_cols + sport_columns
        st.dataframe(df_players[display_cols], use_container_width=True, hide_index=True)

    # ---------- TAB 3: INSIGHTS & BREAKDOWN ---------- #
    with tab3:
        sub1, sub2, sub3 = st.tabs(["🏆 Top Players", "🧍 Player Breakdown", "📊 Aggregated Stats"])

        with sub1:
            st.subheader("🔥 Top 5 Players (Total Score)")
            top5 = df_players[['Player', 'Total Score']].sort_values(by="Total Score", ascending=False).head(5)
            fig_top5 = px.bar(top5, x="Player", y="Total Score", color="Total Score", text="Total Score")
            st.plotly_chart(fig_top5, use_container_width=True)

            st.subheader("🏅 Top 5 Players in Each Sport")
            for sport in sport_columns:
                top5_sport = df_players[["Player", sport]].sort_values(by=sport, ascending=False).head(5)
                top5_sport = top5_sport[top5_sport[sport] > 0]
                if not top5_sport.empty:
                    st.markdown(f"#### {sport}")
                    fig = px.bar(top5_sport, x="Player", y=sport, color=sport, text=sport)
                    st.plotly_chart(fig, use_container_width=True)

        with sub2:
            st.subheader("🎯 Player Score Distribution by Sport")
            selected_player = st.selectbox("Select a player", df_players["Player"].unique())
            player_row = df_players[df_players["Player"] == selected_player].iloc[0]
            player_scores = {sport: player_row[sport] for sport in sport_columns if player_row[sport] > 0}
            if player_scores:
                df_player_sport = pd.DataFrame(player_scores.items(), columns=["Sport", "Score"])
                fig_pie = px.pie(df_player_sport, names="Sport", values="Score", title=f"{selected_player}'s Score Split by Sport", hole=0.3)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info(f"{selected_player} has no points in any sport.")

        with sub3:
            st.subheader("🧍 Gender Distribution")
            gender_dist = df_players["Gender"].value_counts().reset_index()
            gender_dist.columns = ["Gender", "Count"]
            fig_gender = px.pie(gender_dist, names="Gender", values="Count", hole=0.4)
            st.plotly_chart(fig_gender, use_container_width=True)

            st.subheader("🎮 Sport Participation Count")
            sport_participation = (df_players[sport_columns] > 0).sum().reset_index()
            sport_participation.columns = ["Sport", "Participants"]
            fig_sport_part = px.bar(sport_participation, x="Sport", y="Participants", color="Sport", text="Participants")
            st.plotly_chart(fig_sport_part, use_container_width=True)
