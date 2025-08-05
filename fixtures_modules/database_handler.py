# database_handler.py/fixtures_modules

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from fixtures_modules.constants import SPREADSHEET_ID
import time

# ✅ Google Sheets auth
@st.cache_resource(ttl=300)
def get_gsheet_connection():
    try:
        creds = Credentials.from_service_account_file(
            "data/gcp_service_account.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"❌ Error connecting to Google Sheets: {e}")
        return None

def load_sheet_as_df(sheet_name):
    try:
        client = get_gsheet_connection()
        # if client is None:
        #     st.error("🚫 GSheet client is None (connection failed)")
        #     return pd.DataFrame()
        # else:
        #     st.info("✅ GSheet client connected")

        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        #st.info(f"✅ Opened spreadsheet: {spreadsheet.title}")

        worksheet = spreadsheet.worksheet(sheet_name)
        #st.info(f"✅ Loaded worksheet: {sheet_name}")

        data = worksheet.get_all_records()
        #st.info(f"📦 Rows fetched: {len(data)}")

        if not data:
            st.warning("⚠️ No data found in sheet. It may be empty or have bad headers.")

        df = pd.DataFrame(data)

        # Normalize headers
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r'[\n\r\t\s]+', '_', regex=True)
            .str.replace(r'[^a-z0-9_]', '', regex=True)
        )

        return df

    except Exception as e:
        import traceback
        st.error(f"❌ Could not load sheet '{sheet_name}': {e}")
        with st.expander("📄 Debug Info"):
            st.text(traceback.format_exc())
        return pd.DataFrame()


def update_match_number(sheet_name, id_col, identifier, match_col, match_no,
                        worksheet=None, data_cache=None, headers_cache=None):
    try:
        from fixtures_modules.constants import SPREADSHEET_ID
        from fixtures_modules.database_handler import get_gsheet_connection

        if worksheet is None:
            client = get_gsheet_connection()
            worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)

        headers = headers_cache or worksheet.row_values(1)
        data = data_cache or worksheet.get_all_records()

        headers = [h.strip().lower().replace(" ", "_") for h in headers]
        id_index = headers.index(id_col)
        match_index = headers.index(match_col)

        norm = lambda x: str(x).strip().lower()
        norm_identifier = norm(identifier)

        for r_idx, row in enumerate(data):
            if norm(row.get(id_col, "")) == norm_identifier:
                existing = row.get(match_col, "")
                if not str(existing).strip():
                    time.sleep(0.1)  # throttle writes
                    worksheet.update_cell(r_idx + 2, match_index + 1, str(match_no))
                return

        # not found, append
        new_row = [''] * len(headers)
        new_row[id_index] = identifier
        new_row[match_index] = str(match_no)
        time.sleep(0.1)
        worksheet.append_row(new_row)

    except gspread.exceptions.APIError as e:
        if "429" in str(e):
            time.sleep(2)
            return update_match_number(sheet_name, id_col, identifier, match_col, match_no,
                                       worksheet, data_cache, headers_cache)
        else:
            st.error(f"[ERROR] Could not update {identifier}: {e}")
    except Exception as e:
        st.error(f"[ERROR] Match update for {identifier}: {e}")

# ✅ Save DataFrame back to sheet (optional helper)
def overwrite_sheet(sheet_name, df):
    try:
        client = get_gsheet_connection()
        worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)

        worksheet.clear()
        worksheet.update([df.columns.tolist()] + df.values.tolist())
        st.success(f"✅ Sheet '{sheet_name}' overwritten successfully.")
    except Exception as e:
        st.error(f"❌ Failed to overwrite sheet: {e}")
