#!/usr/bin/env node
/**
 * Complete Intelligence Hub Setup
 * Adds all data validation, conditional formatting, and header formatting
 */

const { google } = require('googleapis');
const fs = require('fs');

const SPREADSHEET_ID = '14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c';

// Load configuration
const config = JSON.parse(fs.readFileSync('intelligence_hub_config.json', 'utf-8'));

async function setupDataValidation(sheets) {
  console.log('\n📋 Adding Data Validation...');

  const requests = [];

  // Market Trends - Functiegroep dropdown (C2:C1000)
  requests.push({
    setDataValidation: {
      range: { sheetId: 670695312, startRowIndex: 1, endRowIndex: 1000, startColumnIndex: 2, endColumnIndex: 3 },
      rule: {
        condition: { type: 'ONE_OF_LIST', values: [
          {userEnteredValue: 'Werkvoorbereider Elektro'}, {userEnteredValue: 'Werkvoorbereider Bouw'},
          {userEnteredValue: 'Calculator Bouw'}, {userEnteredValue: 'Constructeur'},
          {userEnteredValue: 'Servicemonteur'}, {userEnteredValue: 'Monteur Elektro'},
          {userEnteredValue: 'PLC Programmeur'}, {userEnteredValue: 'Projectleider Elektro'},
          {userEnteredValue: 'Projectleider Installatie'}, {userEnteredValue: 'Allround Monteur'},
          {userEnteredValue: 'Mechatronicus'}, {userEnteredValue: 'Tekenaar Constructeur'}
        ]},
        showCustomUi: true
      }
    }
  });

  // Market Trends - Region dropdown (D2:D1000)
  requests.push({
    setDataValidation: {
      range: { sheetId: 670695312, startRowIndex: 1, endRowIndex: 1000, startColumnIndex: 3, endColumnIndex: 4 },
      rule: {
        condition: { type: 'ONE_OF_LIST', values: [
          {userEnteredValue: 'Gelderland'}, {userEnteredValue: 'Overijssel'},
          {userEnteredValue: 'Noord-Brabant'}, {userEnteredValue: 'Utrecht'},
          {userEnteredValue: 'Limburg'}, {userEnteredValue: 'Flevoland'}
        ]},
        showCustomUi: true
      }
    }
  });

  await sheets.spreadsheets.batchUpdate({
    spreadsheetId: SPREADSHEET_ID,
    resource: { requests }
  });

  console.log('  ✅ Data validation added');
}

async function setupConditionalFormatting(sheets) {
  console.log('\n🎨 Adding Conditional Formatting...');

  const requests = [];

  // Market Trends - Priority colors (N2:N1000)
  requests.push({
    addConditionalFormatRule: {
      rule: {
        ranges: [{ sheetId: 670695312, startRowIndex: 1, endRowIndex: 1000, startColumnIndex: 13, endColumnIndex: 14 }],
        booleanRule: {
          condition: { type: 'TEXT_EQ', values: [{ userEnteredValue: 'HIGH' }] },
          format: { backgroundColor: { red: 1, green: 0.42, blue: 0.42 } }
        }
      },
      index: 0
    }
  });

  requests.push({
    addConditionalFormatRule: {
      rule: {
        ranges: [{ sheetId: 670695312, startRowIndex: 1, endRowIndex: 1000, startColumnIndex: 13, endColumnIndex: 14 }],
        booleanRule: {
          condition: { type: 'TEXT_EQ', values: [{ userEnteredValue: 'MEDIUM' }] },
          format: { backgroundColor: { red: 1, green: 0.65, blue: 0 } }
        }
      },
      index: 1
    }
  });

  requests.push({
    addConditionalFormatRule: {
      rule: {
        ranges: [{ sheetId: 670695312, startRowIndex: 1, endRowIndex: 1000, startColumnIndex: 13, endColumnIndex: 14 }],
        booleanRule: {
          condition: { type: 'TEXT_EQ', values: [{ userEnteredValue: 'LOW' }] },
          format: { backgroundColor: { red: 0.56, green: 0.93, blue: 0.56 } }
        }
      },
      index: 2
    }
  });

  await sheets.spreadsheets.batchUpdate({
    spreadsheetId: SPREADSHEET_ID,
    resource: { requests }
  });

  console.log('  ✅ Conditional formatting added');
}

async function setupHeaderFormatting(sheets) {
  console.log('\n🎨 Formatting Headers...');

  const requests = [];

  // All sheets - Blue background, white text, bold, freeze row 1
  const sheetIds = [670695312, 708415054, 658042795, 1150728346, 2010870672, 1377813384, 495924025, 418295498];

  for (const sheetId of sheetIds) {
    // Format header row
    requests.push({
      repeatCell: {
        range: { sheetId, startRowIndex: 0, endRowIndex: 1 },
        cell: {
          userEnteredFormat: {
            backgroundColor: { red: 0, green: 0.4, blue: 0.8 },
            textFormat: { foregroundColor: { red: 1, green: 1, blue: 1 }, bold: true }
          }
        },
        fields: 'userEnteredFormat(backgroundColor,textFormat)'
      }
    });

    // Freeze row 1
    requests.push({
      updateSheetProperties: {
        properties: { sheetId, gridProperties: { frozenRowCount: 1 } },
        fields: 'gridProperties.frozenRowCount'
      }
    });
  }

  await sheets.spreadsheets.batchUpdate({
    spreadsheetId: SPREADSHEET_ID,
    resource: { requests }
  });

  console.log('  ✅ Headers formatted (blue/white/bold/freeze)');
}

async function main() {
  console.log('🚀 RECRUITIN INTELLIGENCE HUB - COMPLETE SETUP');
  console.log('='.repeat(60));

  try {
    const auth = new google.auth.GoogleAuth({
      keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });

    const sheets = google.sheets({ version: 'v4', auth });

    await setupDataValidation(sheets);
    await setupConditionalFormatting(sheets);
    await setupHeaderFormatting(sheets);

    console.log('\n' + '='.repeat(60));
    console.log('✅ SETUP COMPLETE!');
    console.log(`\n📊 Spreadsheet: https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/edit`);

  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

main();
