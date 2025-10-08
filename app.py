import streamlit as st
st.set_page_config(page_title="TLOL3 Arena", layout="wide",initial_sidebar_state="expanded")
from sections import players_stats
from sections.fixtures import render_fixtures_for_sport, render_sport_banner_and_rules ,render_bonus_cards
from fixtures_modules.database_handler import load_sheet_as_df, sheet_exists
from sections.tt_fixtures import render_table_tennis_fixtures
from sections.olympics_fixtures import render_olympics_fixtures

from sections import home, auction_live, leaderboard
from sections.leaderboard import render_points_info
import os
import traceback


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
        render_points_info()
        st.markdown("<hr style='border-color:#ffcc00;'>", unsafe_allow_html=True)
        # st.title("🏋️‍♂️ Kismein Kitna Hai Dum (Leaderboard)")
        leaderboard.render()

    elif st.session_state.active_section == "Rab Ne Bana Di Jodi":
        st.title("👫 Rab Ne Bana Di Jodi — Fixtures")

        # Ensure fixture cache exists
        if "fixture_cache" not in st.session_state:
            st.session_state.fixture_cache = {}

        # === Public Fixture Tabs ===
        sport_tabs = ["Olympics", "Cricket"]
        tab_objects = st.tabs(sport_tabs)

        for tab, sport in zip(tab_objects, sport_tabs):
            with tab:
                render_sport_banner_and_rules(sport)
                render_bonus_cards(sport)

                is_table_tennis = (sport.lower() == "table tennis")
                is_olympics = (sport.lower() == "olympics")
                cache_key = f"fixtures_{sport.lower()}"
                fixture_flag_key = f"fixtures_ready_{sport.lower()}"
                regenerate = st.session_state.get(fixture_flag_key, False)

                # ---- Olympics: render purely from function (no sheet checks) ----
                if is_olympics:
                    # if you want lightweight caching to avoid re-rendering heavy UI, you can keep a flag
                    if cache_key in st.session_state.fixture_cache and not regenerate:
                        render_olympics_fixtures()
                    else:
                        # always render from the function; avoid any sheet access or "sheet missing" messages
                        render_olympics_fixtures()
                        st.session_state.fixture_cache[cache_key] = {"source": "function"}
                        st.session_state[fixture_flag_key] = True
                    continue

                # ---- Non-Olympics sports: existing sheet-backed flow ----
                # If cached and not regenerating → just render
                if cache_key in st.session_state.fixture_cache and not regenerate:
                    if is_table_tennis:
                        render_table_tennis_fixtures()
                    else:
                        render_fixtures_for_sport(sport)
                    continue

                # Common Google Sheet name for non-Olympics sports
                sheet_name = f"Fixtures_{sport.lower()}"

                try:
                    if sheet_exists(sheet_name):
                        df = load_sheet_as_df(sheet_name)

                        if not df.empty:
                            # Cache fixtures for current sport
                            st.session_state.fixture_cache[cache_key] = {"df": df}
                            st.session_state[fixture_flag_key] = True

                            # Render based on sport type
                            if is_table_tennis:
                                render_table_tennis_fixtures()
                            else:
                                render_fixtures_for_sport(sport)
                        else:
                            st.info(f"⚠ Fixtures sheet '{sheet_name}' exists but is empty.")
                    else:
                        # For non-Olympics sports only: keep the existing info behavior
                        st.info(f"⚠ Fixtures sheet '{sheet_name}' does not exist yet.")
                except Exception as e:
                    st.error(f"⚠ Error rendering fixtures for {sport}: {e}")




    elif st.session_state.active_section == "Khatron Ke Khiladi (Player Stats)":
        players_stats.render()
    elif st.session_state.active_section == "Live Auction":
        auction_live.render()
except Exception as e:
    #st.error(f"An error occurred: {e}")
    st.error("Please refresh the page and try again.")
    # Log the full traceback for debugging
    with st.expander("Error Details"):
         st.text(traceback.format_exc())
    