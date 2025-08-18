import streamlit as st
st.set_page_config(page_title="TLOL3 Dashboard", layout="wide")
from sections import players_stats
from sections.fixtures import render_fixtures_for_sport, render_sport_banner_and_rules ,render_bonus_cards, generate_and_store_fixtures
from fixtures_modules.database_handler import load_sheet_as_df, sheet_exists, read_fixtures_sheet

from sections import home, auction_live, leaderboard
import os
import traceback
import random, time


def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Initialize default section
if "active_section" not in st.session_state:
    st.session_state.active_section = "Ghar Ho To Aisa"


# --- Sidebar Navigation ---
with st.sidebar:
    # Logo
    st.image("assets/TLOL3_logo.png", use_container_width=True)
    
    if st.button("🏠 Ghar Ho To Aisa (Home)"):
        st.session_state.active_section = "Ghar Ho To Aisa"
    if st.button("🏋️‍♂️ Kismein Kitna Hai Dum (Leaderboard)"):
        st.session_state.active_section = "Kismein Kitna Hai Dum (Leaderboard)"
    if st.button("👫 Rab Ne Bana Di Jodi (Fixtures)"):
        st.session_state.active_section = "Rab Ne Bana Di Jodi"
    if st.button("🎯 Khatron Ke Khiladi (Player Stats)"):
        st.session_state.active_section = "Khatron Ke Khiladi (Player Stats)"
    # if st.button("💰 Live Auction"):
    #     st.session_state.active_section = "Live Auction"

# --- Main Area Renderer ---
try:
    if st.session_state.active_section == "Ghar Ho To Aisa":
        home.render()

    elif st.session_state.active_section == "Kismein Kitna Hai Dum (Leaderboard)":
        st.title("🏋️‍♂️ Kismein Kitna Hai Dum (Leaderboard)")
        leaderboard.render()

    elif st.session_state.active_section == "Rab Ne Bana Di Jodi":
        st.title("👫 Rab Ne Bana Di Jodi — Fixtures")

        # Ensure fixture cache exists
        if "fixture_cache" not in st.session_state:
            st.session_state.fixture_cache = {}

        # === Admin Controls ===
        with st.expander("🛠️ Admin Controls", expanded=True):
            if "admin_verified" not in st.session_state:
                st.session_state.admin_verified = False  # default locked

            if not st.session_state.admin_verified:
                password = st.text_input("Enter Admin Password:", type="password")
                if st.button("✅ Verify"):
                    if password == "tlol3":
                        st.session_state.admin_verified = True
                        st.success("✅ Admin access granted!")
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password. Try again.")
            else:
                # Only visible after login
                selected_sport = st.selectbox(
                    "🎯 Choose a Sport to Manage Fixtures",
                    ["Foosball", "Carrom", "Table tennis", "Badminton", "Chess"],
                    key="sport_selector"
                )

                try:
                    st.session_state.fixture_cache[selected_sport] = read_fixtures_sheet(selected_sport)
                    #st.success(f"📥 Fixtures loaded for {selected_sport}")
                except Exception as e:
                    st.error(f"⚠️ Could not load fixtures for {selected_sport}: {e}")

                col1, col2 = st.columns(2)
                fun_messages = [
                    "Sabr Karo, Abhi Karke Deta Hoo.. ⏳",
                    "Generating magic… ✨",
                    "Shuffling teams… 🌀",
                    "Crunching numbers… 🤓",
                    "Almost there… 🏃‍♂️💨"
                ]

                with col1:
                    if st.button("🚀 Generate Fixtures"):
                        cache_key = f"fixtures_{selected_sport.lower()}"

                        # Only generate if not cached
                        if cache_key not in st.session_state.fixture_cache:
                            try:
                                with st.spinner(random.choice(fun_messages)):
                                    df, group_matches, all_knockouts = generate_and_store_fixtures(selected_sport)

                                    # Save to cache
                                    st.session_state.fixture_cache[cache_key] = {
                                        "df": df,
                                        "group_matches": group_matches,
                                        "all_knockouts": all_knockouts
                                    }
                                    st.session_state[f"fixtures_ready_{selected_sport.lower()}"] = True

                                st.success(f"✅ Fixtures successfully generated and saved for {selected_sport}!")
                                st.rerun()

                            except Exception as e:
                                st.error(f"❌ An error occurred during fixture generation: {e}")
                        else:
                            st.info("⚠ Fixtures already generated. Refresh page to regenerate.")

                if st.button("🔒 Logout Admin"):
                    st.session_state.admin_verified = False
                    st.rerun()


        # === Public Fixture Tabs ===
        sport_tabs = ["Foosball", "Carrom", "Table tennis", "Badminton", "Chess"]
        tab_objects = st.tabs(sport_tabs)

        for tab, sport in zip(tab_objects, sport_tabs):
            with tab:
                render_sport_banner_and_rules(sport)
                render_bonus_cards(sport)

                cache_key = f"fixtures_{sport.lower()}"
                fixture_flag_key = f"fixtures_ready_{sport.lower()}"
                regenerate = st.session_state.get(fixture_flag_key, False)

                # Render from cache if available
                if cache_key in st.session_state.fixture_cache and not regenerate:
                    render_fixtures_for_sport(sport)
                else:
                    # Check sheet existence first
                    sheet_name = f"Fixtures_{sport.lower()}"
                    if sheet_exists(sheet_name):  # <-- implement sheet_exists() to return True/False
                        df = load_sheet_as_df(sheet_name)
                        if not df.empty:
                            st.session_state.fixture_cache[cache_key] = {"df": df}
                            st.session_state[fixture_flag_key] = True
                            render_fixtures_for_sport(sport)
                        else:
                            st.info(f"⚠ Fixtures sheet '{sheet_name}' exists but is empty.")
                    else:
                        st.info(f"⚠ Fixtures sheet '{sheet_name}' does not exist yet.")






    elif st.session_state.active_section == "Khatron Ke Khiladi (Player Stats)":
        players_stats.render()
    elif st.session_state.active_section == "Live Auction":
        auction_live.render()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.error("Please refresh the page and try again.")
    # Log the full traceback for debugging
    with st.expander("Error Details"):
        st.text(traceback.format_exc())
    