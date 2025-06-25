import streamlit as st
import os

def render():
    # Centered layout using Streamlit columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>🌟 Welcome to TLOL3!</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:18px;'>Get ready for the ultimate showdown of skills, spirit, and sportsmanship!</p>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        png_path = os.path.join("assets", "TLOL2.png")
        if os.path.exists(png_path):
            st.image(png_path, width=700)
        else:
            st.warning("Image not found. Please add 'TLOL2.png' to the assets folder.")

