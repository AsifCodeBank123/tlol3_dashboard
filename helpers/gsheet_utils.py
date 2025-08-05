import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import time

# Setup Google Sheets Access
@st.cache_resource(ttl=300)  # Cache for 5 minutes
def get_gsheet_connection():
    try:
        creds = Credentials.from_service_account_file("data/gcp_service_account.json", scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ])
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

SPREADSHEET_ID = "1854rtEWHjp1-akVlSIzjdR_PxUW1hdKxnU2hOp5KPTw"

def update_match_number(sheet_name, id_col_name, identifier, match_col, match_no):
    """
    Update match number in Google Sheet:
    - If identifier exists: update match_col only if empty
    - If identifier doesn't exist: append a new row with identifier and match_no
    """
    try:
        client = get_gsheet_connection()
        if client is None:
            st.error("❌ Failed to connect to Google Sheets")
            return False

        worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
        data = worksheet.get_all_records()
        headers = worksheet.row_values(1)

        # Ensure column exists
        if match_col not in headers:
            st.error(f"❌ Column '{match_col}' not found in sheet '{sheet_name}'")
            return False

        if id_col_name not in headers:
            st.error(f"❌ Column '{id_col_name}' not found in sheet '{sheet_name}'")
            return False

        id_index = headers.index(id_col_name)
        match_index = headers.index(match_col)
        updated = False

        # Normalize and match
        norm = lambda x: str(x).strip().lower()
        norm_identifier = norm(identifier)

        for r_idx, row in enumerate(data):
            sheet_id_val = norm(row.get(id_col_name, ""))
            if sheet_id_val == norm_identifier:
                existing = row.get(match_col, "")
                if not str(existing).strip():  # only update if empty
                    worksheet.update_cell(r_idx + 2, match_index + 1, str(match_no))
                    st.success(f"✅ Updated {identifier} with {match_col} = {match_no}")
                else:
                    st.info(f"ℹ️ {identifier} already has {match_col} = {existing}, not overwritten")
                updated = True
                break

        # Append new row if not found
        if not updated:
            new_row = [''] * len(headers)
            new_row[id_index] = identifier
            new_row[match_index] = str(match_no)
            worksheet.append_row(new_row)
            st.success(f"✅ Added new row for {identifier} with {match_col} = {match_no}")

        return True

    except Exception as e:
        st.error(f"[ERROR] Match update for {identifier}: {e}")
        return False


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_all_match_numbers(sheet_name, match_col):
    """
    Get all match numbers from a specific column in a sheet
    """
    try:
        client = get_gsheet_connection()
        if client is None:
            return []
            
        worksheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
        data = worksheet.get_all_records()
        headers = worksheet.row_values(1)
        
        if match_col not in headers:
            st.error(f"Column '{match_col}' not found in sheet '{sheet_name}'")
            return []
            
        col_index = headers.index(match_col)
        match_numbers = []
        
        for row in data:
            match_no = row.get(match_col, "")
            if match_no and str(match_no).strip():
                try:
                    match_numbers.append(int(match_no))
                except ValueError:
                    pass
                    
        return match_numbers
    except Exception as e:
        st.error(f"Error getting match numbers: {e}")
        return []