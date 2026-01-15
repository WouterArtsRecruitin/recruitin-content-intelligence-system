#!/usr/bin/env python3
"""
Import all CSV data to Recruitin Intelligence Hub Google Spreadsheet
Uses Google Sheets API to properly import CSV data with correct column separation
"""

import os
import csv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SPREADSHEET_ID = "14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Sheet mappings: CSV file -> Sheet name and range
SHEET_MAPPINGS = [
    ("market_trends_data.csv", "Market Trends", "A2"),
    ("icp_activity_data.csv", "ICP Activity", "A2"),
    ("ghosting_patterns_data.csv", "Ghosting Patterns", "A2"),
    ("sector_news_data.csv", "Sector News", "A2"),
    ("concurrent_activity_data.csv", "Concurrent Activity", "A2"),
    ("newsletter_monthly_data.csv", "Newsletter Monthly Data", "A2"),
    ("dashboard_data.csv", "Dashboard", "A2"),
]


def read_csv_as_values(csv_file):
    """Read CSV and return as 2D array for Sheets API"""
    values = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row (already in sheets)
        for row in reader:
            values.append(row)
    return values


def import_csv_to_sheet(service, spreadsheet_id, csv_file, sheet_name, start_cell):
    """Import CSV data to specific sheet"""
    print(f"\n📥 Importing {csv_file} to '{sheet_name}'...")

    # Read CSV data
    values = read_csv_as_values(csv_file)

    if not values:
        print(f"  ⚠️  No data found in {csv_file}")
        return False

    # Prepare range
    range_name = f"'{sheet_name}'!{start_cell}"

    # Update the sheet
    body = {
        'values': values
    }

    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',  # Parse formulas
            body=body
        ).execute()

        updated_cells = result.get('updatedCells', 0)
        updated_rows = result.get('updatedRows', 0)
        print(f"  ✅ Imported {updated_rows} rows ({updated_cells} cells)")
        return True

    except HttpError as error:
        print(f"  ❌ Error: {error}")
        return False


def main():
    """Main import function"""
    print("🚀 RECRUITIN INTELLIGENCE HUB - CSV IMPORT")
    print("=" * 60)

    # Load credentials
    creds = None
    token_path = os.path.expanduser('~/.credentials/google-sheets-token.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        print("❌ Google Sheets credentials not found!")
        print(f"   Expected: {token_path}")
        print("\n   Run authentication first:")
        print("   python3 setup_google_auth.py")
        return

    # Build service
    try:
        service = build('sheets', 'v4', credentials=creds)
        print(f"✅ Connected to Google Sheets API\n")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return

    # Import all CSV files
    success_count = 0
    total_count = len(SHEET_MAPPINGS)

    for csv_file, sheet_name, start_cell in SHEET_MAPPINGS:
        if os.path.exists(csv_file):
            if import_csv_to_sheet(service, SPREADSHEET_ID, csv_file, sheet_name, start_cell):
                success_count += 1
        else:
            print(f"\n⚠️  File not found: {csv_file}")

    # Summary
    print("\n" + "=" * 60)
    print(f"✅ COMPLETE: {success_count}/{total_count} sheets imported successfully")
    print("\n📊 Spreadsheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")


if __name__ == "__main__":
    main()
