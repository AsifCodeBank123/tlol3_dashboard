import streamlit as st
import os
from PIL import Image


import base64
from io import BytesIO

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def render():
    # Centered layout using Streamlit columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>🌟 Welcome to TLOL3!</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:18px;'>Get ready for the ultimate showdown of skills, spirit, and sportsmanship!</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        png_path = os.path.join("assets", "TLOL2.png")
        if os.path.exists(png_path):
            img = Image.open(png_path)

            # Display the image using HTML to preserve original size and center it
            st.markdown(
                f"""
                <div style='text-align:center;'>
                    <img src="data:image/png;base64,{image_to_base64(img)}" style="display:inline-block;" />
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Image not found. Please add 'TLOL2.png' to the assets folder.")
