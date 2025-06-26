import streamlit as st
import plotly.express as px
import pandas as pd

from modules.data_loader import load_and_merge_scores
from modules.avatar_utils import get_avatar_url
from modules.tier_utils import assign_tiers
from modules.constants import TLOL_SPORTS

def render():
    
    # ---------- TABS ---------- #
    tab1, tab2, tab3 = st.tabs(["🏷️ Auction Preview", "📊 Raw Stats", "📈 Insights & Breakdown"])


    # ---------- LOAD & PROCESS DATA ---------- #
    with st.spinner("Loading player data..."):
        df_players = load_and_merge_scores("reports")
        df_players = assign_tiers(df_players)

    # ---------- TAB 1: AUCTION PREVIEW ---------- #
    with tab1:
        st.header("🎯 Auction Preview")

        # --- Filters ---
        col1, col2, col3 = st.columns(3)
        with col1:
            tier_filter = st.selectbox("🎖️ Tier", ["All", "Diamond", "Gold", "Silver", "Bronze"])
        with col2:
            sport_columns = [col for col in df_players.columns if col in TLOL_SPORTS]
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

        # --- Card UI (No sport-wise, fixed height) ---
        # --- Compact Player Card with Sport Bifurcation ---
        def player_card(player_row):
            avatar_url = get_avatar_url(player_row["Player"], player_row["Gender"])
            # Keep only actual sport scores (non-zero)
            sport_scores = {k: v for k, v in player_row.items()
                            if k in sport_columns and v > 0}
            # Create horizontal sport list (not too tall!)
            sport_line = " | ".join([f"{k}: {int(v)}" for k, v in sport_scores.items()])
            if len(sport_line) > 50:
                sport_line = sport_line[:47] + "..."

            html = f"""
            <div style="
                background-color:#f4f4f4;
                border-radius:12px;
                padding:10px;
                margin:5px;
                font-size:13px;
                color:#222;
                width: 100%;
                height: 260px;
                box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            ">
                <div>
                    <img src="{avatar_url}" width="60" style="border-radius:50%; margin-bottom:8px;" />
                    <div style="font-weight:bold; font-size:14px;">{player_row['Player']}</div>
                    <div>Tier: <code>{player_row['Tier']}</code></div>
                    <div>Total Points: <strong>{int(player_row['Total Score'])}</strong></div>
                </div>
                <div style="font-size:11px; color:#444; margin-top:5px;">{sport_line}</div>
                <div style="font-size:11px;">Gender: {player_row['Gender']}</div>
            </div>
            """
            return html


        # --- Grid Layout using st.columns ---
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

        # Only show selected columns: Player, Gender, Tier, Total Score + Official Sports
        base_cols = ['Player', 'Gender', 'Tier', 'Total Score']
        sport_columns = [col for col in df_players.columns if col in TLOL_SPORTS]
        display_cols = base_cols + sport_columns

        st.dataframe(df_players[display_cols], use_container_width=True, hide_index=True)

        # ---------- TAB 3: INSIGHTS & BREAKDOWN ---------- #
       
    with tab3:
        st.header("📈 Insights & Breakdown")
       

        # --- 1. Top 5 Overall Players --- #
        st.subheader("🏆 Top 5 Players (Total Score)")
        top5 = df_players[['Player', 'Total Score']].sort_values(by="Total Score", ascending=False).head(5)
        fig_top5 = px.bar(
            top5,
            x="Player",
            y="Total Score",
            color="Total Score",
            text="Total Score",
            title="Top 5 Players"
        )
        st.plotly_chart(fig_top5, use_container_width=True)

        # --- 2. Player-wise Sport Score Breakdown --- #
        st.subheader("🥧 Player Score Distribution by Sport")

        selected_player = st.selectbox("Select a player", df_players["Player"].unique())
        player_row = df_players[df_players["Player"] == selected_player].iloc[0]
        player_scores = {sport: player_row[sport] for sport in sport_columns if player_row[sport] > 0}

        if player_scores:
            df_player_sport = pd.DataFrame(player_scores.items(), columns=["Sport", "Score"])
            fig_player_pie = px.pie(
                df_player_sport,
                names="Sport",
                values="Score",
                title=f"{selected_player}'s Score Distribution by Sport",
                hole=0.3
            )
            st.plotly_chart(fig_player_pie, use_container_width=True)
        else:
            st.info(f"{selected_player} has no scored events.")

        # --- 3. Top 5 Players in Each Sport --- #
        st.subheader("🏅 Top 5 Players in Each Sport")

        for sport in sport_columns:
            st.markdown(f"#### 🏸 {sport}")
            top5_sport = df_players[["Player", sport]].sort_values(by=sport, ascending=False).head(5)
            top5_sport = top5_sport[top5_sport[sport] > 0]

            if not top5_sport.empty:
                fig_sport_bar = px.bar(
                    top5_sport,
                    x="Player",
                    y=sport,
                    color=sport,
                    text=sport,
                    title=f"Top 5 in {sport}"
                )
                st.plotly_chart(fig_sport_bar, use_container_width=True)
            else:
                st.write("No participants with non-zero scores in this sport.")
