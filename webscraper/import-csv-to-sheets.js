#!/usr/bin/env node
/**
 * Import all CSV data to Recruitin Intelligence Hub
 * Properly handles CSV parsing and Google Sheets API upload
 */

const fs = require('fs');
const { google } = require('googleapis');
const path = require('path');

// Configuration
const SPREADSHEET_ID = '14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c';

// Sheet mappings
const SHEET_MAPPINGS = [
  { csv: 'market_trends_data.csv', sheet: 'Market Trends', range: 'A2' },
  { csv: 'icp_activity_data.csv', sheet: 'ICP Activity', range: 'A2' },
  { csv: 'ghosting_patterns_data.csv', sheet: 'Ghosting Patterns', range: 'A2' },
  { csv: 'sector_news_data.csv', sheet: 'Sector News', range: 'A2' },
  { csv: 'concurrent_activity_data.csv', sheet: 'Concurrent Activity', range: 'A2' },
  { csv: 'newsletter_monthly_data.csv', sheet: 'Newsletter Monthly Data', range: 'A2' },
  { csv: 'dashboard_data.csv', sheet: 'Dashboard', range: 'A2' }
];

/**
 * Parse CSV file into 2D array
 */
function parseCSV(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.trim().split('\n');

  // Skip header (first line)
  const dataLines = lines.slice(1);

  // Parse each line, handling quoted values
  return dataLines.map(line => {
    const values = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];

      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }

    // Add last value
    values.push(current.trim());

    return values;
  });
}

/**
 * Import single CSV to sheet
 */
async function importCSVToSheet(sheets, mapping) {
  console.log(`\n📥 Importing ${mapping.csv} to "${mapping.sheet}"...`);

  try {
    // Read and parse CSV
    const values = parseCSV(mapping.csv);

    if (values.length === 0) {
      console.log(`  ⚠️  No data in ${mapping.csv}`);
      return false;
    }

    // Update sheet
    const range = `'${mapping.sheet}'!${mapping.range}`;
    const response = await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: range,
      valueInputOption: 'USER_ENTERED',
      resource: { values }
    });

    const { updatedCells, updatedRows } = response.data;
    console.log(`  ✅ Imported ${updatedRows} rows (${updatedCells} cells)`);
    return true;

  } catch (error) {
    console.error(`  ❌ Error: ${error.message}`);
    return false;
  }
}

/**
 * Main function
 */
async function main() {
  console.log('🚀 RECRUITIN INTELLIGENCE HUB - CSV IMPORT');
  console.log('='.repeat(60));

  try {
    // Initialize Google Sheets API
    const auth = new google.auth.GoogleAuth({
      keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });

    const sheets = google.sheets({ version: 'v4', auth });
    console.log('✅ Connected to Google Sheets API\n');

    // Import all CSVs
    let successCount = 0;

    for (const mapping of SHEET_MAPPINGS) {
      if (fs.existsSync(mapping.csv)) {
        const success = await importCSVToSheet(sheets, mapping);
        if (success) successCount++;
      } else {
        console.log(`\n⚠️  File not found: ${mapping.csv}`);
      }
    }

    // Summary
    console.log('\n' + '='.repeat(60));
    console.log(`✅ COMPLETE: ${successCount}/${SHEET_MAPPINGS.length} sheets imported`);
    console.log(`\n📊 Spreadsheet: https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/edit`);

  } catch (error) {
    console.error('❌ Fatal error:', error.message);
    console.log('\n💡 Tip: Make sure GOOGLE_APPLICATION_CREDENTIALS is set');
    console.log('   export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json');
  }
}

main();
