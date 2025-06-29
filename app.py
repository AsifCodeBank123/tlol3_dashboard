# TLOL_Dash/app.py

import streamlit as st
# ---------- PAGE CONFIG ---------- #
st.set_page_config(page_title="TLOL3 Auction Tool", layout="wide")


from sections import players_stats
from sections import tlol3, home , auction_live # add more as you create
import os
from PIL import Image

# Load banner image
banner_path = os.path.join("assets", "banner2.png")

if os.path.exists(banner_path):
    img = Image.open(banner_path)
    st.image(img, use_container_width=True, output_format="PNG", caption="", clamp=True)
    st.markdown(
        """
        <style>
        img {
            height: auto !important;
            max-height: 140px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Banner not found. Please add 'banner.png' to the assets folder.")


# Load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Initialize default section
if "active_section" not in st.session_state:
    st.session_state.active_section = "Home"

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("### 🏆 TLOL3 Dashboard")

    if st.button("🏠 Home"):
        st.session_state.active_section = "Home"

    # if st.button("📅 TLOL3 Arena"):
    #     st.session_state.active_section = "TLOL3"

    if st.button("🎯 Players Stats"):
        st.session_state.active_section = "Players Stats"

    if st.button("💰 Live Auction"):
        st.session_state.active_section = "Live Auction"

# --- Main Area Renderer ---
if st.session_state.active_section == "Home":
    home.render()
# elif st.session_state.active_section == "TLOL3":
#     tlol3.render()
elif st.session_state.active_section == "Players Stats":
    players_stats.render()
elif st.session_state.active_section == "Live Auction":
    auction_live.render()

