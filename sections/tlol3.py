import streamlit as st
from sections import tlol3_teams

def render():
    st.header("🎮 TLOL3 Tournament Overview")

    tab1, tab2, tab3, tab4 = st.tabs(["Teams", "Schedules", "Leaderboard", "Rules"])

    with tab1:
        #st.subheader("📋 Teams")
        tlol3_teams.render()

    with tab2:
        st.subheader("🗓️ Schedules")
        st.info("Coming soon: Match schedules for all games.")

    with tab3:
        st.subheader("🏅 Leaderboards")
        st.info("Coming soon: Team-wise and individual player scores.")

    with tab4:
        st.subheader("📘 Tournament Rules & Bonus Cards")

        subtab1, subtab2 = st.tabs(["Points System", "Bonus Cards"])

        with subtab1:
            st.markdown("### 🏅 Points Allocation")

            st.markdown("""
    | Type                  | Points       |
    |-----------------------|--------------|
    | Participation         | 50 Points    |
    | Quarter Finals        | 100 Points   |
    | Semi Finals           | 250 Points   |
    | Runner Up             | 500 Points   |
    | Winner / Champion     | 1000 Points  |

    - Legends participating in singles/doubles earn **50 points**.
    - If a doubles partner is absent, the attending player still earns **50 points**.
    - Quarter Final loss (4th place): **100 points** total (50 each if doubles).
    - Semi Final loss (3rd place): **250 points** (125 each if doubles).
    - Winners / Runners:
    - Singles: **1000 / 500 points**
    - Doubles: **500 each / 250 each**

    📝 **Note:** Participation points apply only for Singles & Doubles events.

    ⚠️ One-time events may have lower winning points (e.g., <500).
            """)

        with subtab2:
            st.markdown("### 🎴 Bonus Rules & Cards")

            st.markdown("""
    #### 🔥 Underdog Uprising
    - **Description:** Unsold players get **2x points** if they reach Quarterfinal or beyond
    - **Usage:** All sports **except Cricket**
    - **Outcome:** Player’s points are doubled

    ---

    #### 🎲 Mystery Multiplier *(Use on 18th Sep)*
    - **Description:** Doubles (2x) or triples (3x) points of a selected event
    - **Usage:** Must be played **before event starts**, after rosters
    - **Outcome:**
    - Win with 2x/3x → get 2x/3x points
    - **Lose**:
        - 2x → **-400 points**
        - 3x → **-800 points**

    ---

    #### 🔄 Pairing Swap *(Use between 16–17 Sep)*
    - **Description:** Swap two members between teams for one event (before final roster)
    - **Usage:** Must be used **before participation list is finalized**
    - **Outcome:**
    - If swap helps new team **win**:
        - Playing team: **+200**
        - Team who used card: **-200**
    - If **underperformance**:
        - Team who used card: **+200**
            """)

