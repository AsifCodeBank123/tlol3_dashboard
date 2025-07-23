import pandas as pd
import streamlit as st
import os

@st.cache_data(show_spinner=False)
def load_excel_once():
    return pd.read_excel("reports/seeded_teams.xlsx", sheet_name=None)

def get_excel_mtime():
    return os.path.getmtime("reports/seeded_teams.xlsx")

def load_seeded_pairs(sport):
    all_sheets = load_excel_once()
    df = all_sheets.get(sport)
    if df is None:
        st.error(f"Sheet for sport '{sport}' not found in 'seeded_teams.xlsx'.")
        return pd.DataFrame()
    df.columns = df.columns.str.strip().str.lower()
    return df
