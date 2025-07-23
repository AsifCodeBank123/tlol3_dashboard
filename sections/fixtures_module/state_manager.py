import streamlit as st
from sections.fixtures_module.fixtures_loader import load_seeded_pairs
from sections.fixtures_module.fixtures_generator import generate_fixtures_for_sport
from modules.constants import TLOL_SPORTS  # if defined

@st.cache_data
def generate_fixtures_globally(sport):
    seeded_df = load_seeded_pairs(sport)
    if seeded_df.empty:
        return [], {}
    return generate_fixtures_for_sport(sport, seeded_df)

def reset_fixtures():
    for sport in TLOL_SPORTS:
        st.session_state.pop(f"fixtures_{sport}_matches", None)
        st.session_state.pop(f"fixtures_{sport}_knockouts", None)
