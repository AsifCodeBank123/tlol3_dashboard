# TLOL_Dash/app.py

import streamlit as st
# ---------- PAGE CONFIG ---------- #
st.set_page_config(page_title="TLOL3 Fixtures and Leaderboards", layout="wide")


from sections import players_stats, fixtures
from sections import home , auction_live # add more as you create
import os

def load_global_styles():
    style_path = "assets/style.css"
    if os.path.exists(style_path):
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Initialize default section
if "active_section" not in st.session_state:
    st.session_state.active_section = "Ghar Ho To Aisa"

# --- Sidebar Navigation ---
with st.sidebar:

    # Logo
    st.image("assets/TLOL3_logo.png", use_container_width=True)

    #st.markdown("### 🏆 TLOL3 Dashboard")

    if st.button("🏠 Ghar Ho To Aisa (Home)"):
        st.session_state.active_section = "Ghar Ho To Aisa"

    # if st.button("📅 TLOL3 Arena"):
    #     st.session_state.active_section = "TLOL3"

    if st.button("👫 Rab Ne Bana Di Jodi (Fixtures)"):
        st.session_state.active_section = "Rab Ne Bana Di Jodi"

    if st.button("🎯 Khatron Ke Khiladi (Player Stats)"):
        st.session_state.active_section = "Khatron Ke Khiladi (Player Stats)"

    # if st.button("💰 Live Auction"):
    #     st.session_state.active_section = "Live Auction"

# --- Main Area Renderer ---
if st.session_state.active_section == "Ghar Ho To Aisa":
    home.render()
# elif st.session_state.active_section == "TLOL3":
#     tlol3.render()
elif st.session_state.active_section == "Rab Ne Bana Di Jodi":
    fixtures.render()
elif st.session_state.active_section == "Khatron Ke Khiladi (Player Stats)":
    players_stats.render()
elif st.session_state.active_section == "Live Auction":
    auction_live.render()

