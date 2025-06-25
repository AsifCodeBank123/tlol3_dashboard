# TLOL_Dash/app.py

import streamlit as st

from modules.constants import TLOL_SPORTS
from sections import auction, tlol3, home  # add more as you create
import os
from PIL import Image

# ---------- PAGE CONFIG ---------- #
st.set_page_config(page_title="TLOL3 Auction Hub", layout="wide")

# Load banner image
banner_path = os.path.join("assets", "banner.png")
if os.path.exists(banner_path):
    banner = Image.open(banner_path)
    st.image(banner, use_container_width=True)
else:
    st.warning("⚠️ Banner image not found. Make sure it's in the 'assets' folder.")


st.sidebar.title("🏆 TLOL3 Dashboard")
section = st.sidebar.radio("Go to section:", ["Home", "Auction", "TLOL3"])

if section == "Home":
    home.render()
elif section == "Auction":
    auction.render()
elif section == "TLOL3":
    tlol3.render()