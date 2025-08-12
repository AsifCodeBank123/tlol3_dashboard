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

@st.cache_data(ttl=300)  # Cache for 5 mins
def load_sheet_as_df(sheet_name, spreadsheet_id=SPREADSHEET_ID):
    """Load a specific sheet from a given spreadsheet."""
    try:
        client = get_gsheet_connection()
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Match sheet name ignoring case/whitespace
        worksheet = next(
            (ws for ws in spreadsheet.worksheets()
             if ws.title.strip().lower() == sheet_name.strip().lower()),
            None
        )
        if not worksheet:
            raise gspread.exceptions.WorksheetNotFound(sheet_name)

        data = worksheet.get_all_records()
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
        st.error(f"❌ Could not load sheet '{sheet_name}' from spreadsheet '{spreadsheet_id}': {e}")
        return pd.DataFrame()

# ✅ Match number update logic
def update_match_number(sheet_name, id_col, identifier, match_col, match_no,
                        worksheet=None, data_cache=None, headers_cache=None):
    try:
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
                    time.sleep(0.1)
                    worksheet.update_cell(r_idx + 2, match_index + 1, str(match_no))
                return

        # not found, append
        # new_row = [''] * len(headers)
        # new_row[id_index] = identifier
        # new_row[match_index] = str(match_no)
        # time.sleep(0.1)
        # #worksheet.append_row(new_row)

    except gspread.exceptions.APIError as e:
        if "429" in str(e):
            time.sleep(2)
            return update_match_number(sheet_name, id_col, identifier, match_col, match_no,
                                       worksheet, data_cache, headers_cache)
        else:
            st.error(f"[ERROR] Could not update {identifier}: {e}")
    except Exception as e:
        st.error(f"[ERROR] Match update for {identifier}: {e}")

# ✅ Save DataFrame to sheet (with auto-create if not exists)
def overwrite_sheet(sheet_name, df):
    try:
        client = get_gsheet_connection()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")

        worksheet.clear()
        worksheet.update([df.columns.tolist()] + df.values.tolist())
        st.success(f"✅ Sheet '{sheet_name}' overwritten successfully.")
    except Exception as e:
        st.error(f"❌ Failed to overwrite sheet: {e}")

# ✅ Read fixtures for a sport
def read_fixtures_sheet(sport):
    sheet_name = f"Fixtures_{sport.lower()}"
    try:
        client = get_gsheet_connection()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except gspread.exceptions.WorksheetNotFound:
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error reading sheet '{sheet_name}': {e}")
        return pd.DataFrame()

# ✅ Write fixtures permanently
def write_fixtures_sheet(sport, matches_df):
    try:
        sheet_name = f"Fixtures_{sport.lower()}"
        overwrite_sheet(sheet_name, matches_df)
    except Exception as e:
        st.error(f"❌ Failed to save fixtures for {sport}: {e}")

# =========================
# TEAMS & POINTS FUNCTIONS
# =========================
@st.cache_data(ttl=300)  # 5 min cache
def read_teams_points(sheet_name="teams"):
    """Read teams/points data from the separate Teams Google Sheet."""
    try:
        client = get_gsheet_connection()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"❌ Sheet '{sheet_name}' not found in Teams spreadsheet.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error reading Teams sheet: {e}")
        return pd.DataFrame()
