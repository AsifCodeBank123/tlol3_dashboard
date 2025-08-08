import streamlit as st
st.set_page_config(page_title="TLOL Fixtures", layout="wide")
from sections import players_stats
from sections.fixtures import render_fixtures_for_sport

from sections import home, auction_live, leaderboard
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
        st.title("🏋️‍♂️ Kismein Kitna Hai Dum (Leaderboard)")
        leaderboard.render()
    elif st.session_state.active_section == "Rab Ne Bana Di Jodi":
        st.title("👫 Rab Ne Bana Di Jodi — Fixtures")

        # Admin Panel to trigger generation
        with st.expander("🛠️ Admin Controls", expanded=True):
            if "admin_verified" not in st.session_state:
                st.session_state.admin_verified = False

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
                selected_sport = st.selectbox(
                    "🎯 Choose a Sport to Generate Fixtures",
                    ["Foosball", "Carrom", "Table tennis", "Badminton", "Chess"],
                    key="sport_selector"
                )
                if st.button("🚀 Generate Fixtures"):
                    st.session_state[f"fixtures_ready_{selected_sport.lower()}"] = True
                if st.button("🔒 Logout Admin"):
                    st.session_state.admin_verified = False
                    st.rerun()


            # Tabs for all sports
            sport_tabs = ["Foosball", "Carrom", "Table tennis", "Badminton", "Chess"]
            tab_objects = st.tabs(sport_tabs)

            for tab, sport in zip(tab_objects, sport_tabs):
                with tab:
                    key = f"fixtures_ready_{sport.lower()}"
                    if st.session_state.get(key):
                        render_fixtures_for_sport(sport)
                    else:
                        st.info(f"⚙️ Fixtures not generated yet for {sport}. Use admin controls above.")


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