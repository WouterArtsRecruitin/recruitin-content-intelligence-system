#!/usr/bin/env node
const { Client } = require('@notionhq/client');
const fs = require('fs');

const notion = new Client({ auth: 'ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3' });
const PAGE_ID = '27c2252cbb1581a5bbfcef3736d7c14e';

// Demo deals data
const deals = [
  { title: 'Siemens Enschede - Senior Automation', org: 'Siemens Nederland', contact: 'Jan de Vries', value: 28000, stage: 'Stage 2', datum: '2025-12-22', dagen: 21 },
  { title: 'ASML Veldhoven - Lead Control Systems', org: 'ASML Netherlands', contact: 'Peter Jansen', value: 24000, stage: 'Stage 3', datum: '2026-01-02', dagen: 12 },
  { title: 'Shell Rotterdam - SCADA Specialist', org: 'Shell Nederland', contact: 'Sarah van Dam', value: 22000, stage: 'Stage 2', datum: '2026-01-04', dagen: 8 },
  { title: 'Dow Terneuzen - Instrumentation', org: 'Dow Benelux', contact: 'Mark Peters', value: 19000, stage: 'Stage 3', datum: '2026-01-07', dagen: 5 },
  { title: 'Nouryon Deventer - Process Automation', org: 'Nouryon Chemicals', contact: 'Lisa de Jong', value: 18000, stage: 'Stage 2', datum: '2025-12-28', dagen: 15 },
  { title: 'Vanderlande Veghel - Automation', org: 'Vanderlande Industries', contact: 'Tom Bakker', value: 16000, stage: 'Stage 2', datum: '2025-12-25', dagen: 18 },
  { title: 'Gasunie Groningen - SCADA', org: 'Gasunie Nederland', contact: 'Anna Smit', value: 15000, stage: 'Stage 2', datum: '2025-12-27', dagen: 16 },
  { title: 'TechCorp Arnhem - Medior Automation', org: 'TechCorp Automation', contact: 'Piet Visser', value: 14000, stage: 'Stage 2', datum: '2025-12-29', dagen: 14 }
];

async function uploadDealsTab() {
  console.log('📤 Creating "Openstaande Deals" tab in Notion...\n');

  try {
    // Add main heading
    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        object: 'block',
        type: 'divider',
        divider: {}
      }]
    });

    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        object: 'block',
        type: 'heading_1',
        heading_1: {
          rich_text: [{ text: { content: '📋 OPENSTAANDE DEALS' } }],
          color: 'green_background'
        }
      }]
    });

    // Summary
    const totalValue = deals.reduce((sum, d) => sum + d.value, 0);
    const stuckCount = deals.filter(d => d.dagen > 14).length;

    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        object: 'block',
        type: 'callout',
        callout: {
          rich_text: [{
            text: { content: `${deals.length} deals | €${totalValue.toLocaleString()} pipeline | 🚨 ${stuckCount} stuck >14d` }
          }],
          icon: { emoji: '💰' },
          color: 'green_background'
        }
      }]
    });

    console.log('✅ Header added\n');

    // Table header
    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        object: 'block',
        type: 'heading_2',
        heading_2: {
          rich_text: [{ text: { content: 'Top 8 Deals (Demo Data)' } }]
        }
      }]
    });

    // Add each deal as toggle (collapsible)
    for (let i = 0; i < deals.length; i++) {
      const deal = deals[i];
      const stuckEmoji = deal.dagen > 14 ? '🚨 ' : (deal.dagen > 10 ? '⚠️ ' : '');

      // Deal heading
      await notion.blocks.children.append({
        block_id: PAGE_ID,
        children: [{
          object: 'block',
          type: 'toggle',
          toggle: {
            rich_text: [{
              text: { 
                content: `${i+1}. ${stuckEmoji}${deal.title} - €${deal.value.toLocaleString()}`,
                annotations: { bold: deal.dagen > 14 }
              }
            }],
            children: [
              {
                object: 'block',
                type: 'bulleted_list_item',
                bulleted_list_item: {
                  rich_text: [{ text: { content: `Organisatie: ${deal.org}` } }]
                }
              },
              {
                object: 'block',
                type: 'bulleted_list_item',
                bulleted_list_item: {
                  rich_text: [{ text: { content: `Contact: ${deal.contact}` } }]
                }
              },
              {
                object: 'block',
                type: 'bulleted_list_item',
                bulleted_list_item: {
                  rich_text: [{ text: { content: `Stage: ${deal.stage}` } }]
                }
              },
              {
                object: 'block',
                type: 'bulleted_list_item',
                bulleted_list_item: {
                  rich_text: [{ text: { content: `Datum: ${deal.datum}` } }]
                }
              },
              {
                object: 'block',
                type: 'bulleted_list_item',
                bulleted_list_item: {
                  rich_text: [{
                    text: { 
                      content: `Dagen in stage: ${deal.dagen}d`,
                      annotations: { bold: deal.dagen > 14, color: deal.dagen > 14 ? 'red' : 'default' }
                    }
                  }]
                }
              }
            ]
          }
        }]
      });

      console.log(`✅ ${i+1}. ${deal.title}`);
    }

    // Quick actions section
    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        object: 'block',
        type: 'heading_2',
        heading_2: {
          rich_text: [{ text: { content: '🎯 Quick Commands' } }]
        }
      }]
    });

    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        object: 'block',
        type: 'code',
        code: {
          rich_text: [{
            text: { content: `# Export deals list
python3 pipedrive-open-deals-export.py -o deals.md

# Excel export
python3 pipedrive-open-deals-export.py --excel

# Live data (met API key)
export PIPEDRIVE_API_KEY=your_key
python3 pipedrive-open-deals-export.py` }
          }],
          language: 'bash'
        }
      }]
    });

    console.log('\n✅ OPENSTAANDE DEALS TAB CREATED IN NOTION!');
    console.log(`📄 View: https://notion.so/${PAGE_ID.replace(/-/g, '')}\n`);

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

uploadDealsTab();
