#!/usr/bin/env node
const { Client } = require('@notionhq/client');

const notion = new Client({ auth: 'ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3' });
const PAGE_ID = '27c2252cbb1581a5bbfcef3736d7c14e';

const deals = [
  { title: 'Siemens Enschede - Senior Automation', org: 'Siemens Nederland', contact: 'Jan de Vries', value: 28000, stage: 'Stage 2', dagen: 21 },
  { title: 'ASML Veldhoven - Lead Control Systems', org: 'ASML Netherlands', contact: 'Peter Jansen', value: 24000, stage: 'Stage 3', dagen: 12 },
  { title: 'Shell Rotterdam - SCADA Specialist', org: 'Shell Nederland', contact: 'Sarah van Dam', value: 22000, stage: 'Stage 2', dagen: 8 },
  { title: 'Dow Terneuzen - Instrumentation', org: 'Dow Benelux', contact: 'Mark Peters', value: 19000, stage: 'Stage 3', dagen: 5 },
  { title: 'Nouryon Deventer - Process Automation', org: 'Nouryon Chemicals', contact: 'Lisa de Jong', value: 18000, stage: 'Stage 2', dagen: 15 },
  { title: 'Vanderlande Veghel - Automation', org: 'Vanderlande Industries', contact: 'Tom Bakker', value: 16000, stage: 'Stage 2', dagen: 18 },
  { title: 'Gasunie Groningen - SCADA', org: 'Gasunie Nederland', contact: 'Anna Smit', value: 15000, stage: 'Stage 2', dagen: 16 },
  { title: 'TechCorp Arnhem - Medior Automation', org: 'TechCorp Automation', contact: 'Piet Visser', value: 14000, stage: 'Stage 2', dagen: 14 }
];

async function upload() {
  console.log('📤 Uploading deals to Notion...\n');

  // Header
  await notion.blocks.children.append({
    block_id: PAGE_ID,
    children: [
      { object: 'block', type: 'divider', divider: {} },
      {
        object: 'block',
        type: 'heading_1',
        heading_1: {
          rich_text: [{ text: { content: '📋 OPENSTAANDE DEALS' } }],
          color: 'green_background'
        }
      },
      {
        object: 'block',
        type: 'callout',
        callout: {
          rich_text: [{ text: { content: `8 deals | €${deals.reduce((s,d)=>s+d.value,0).toLocaleString()} | Update: ${new Date().toLocaleDateString('nl-NL')}` } }],
          icon: { emoji: '💰' },
          color: 'green_background'
        }
      }
    ]
  });
  console.log('✅ Header');

  // Deals list
  for (const deal of deals) {
    const emoji = deal.dagen > 14 ? '🚨' : (deal.dagen > 10 ? '⚠️' : '✅');

    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        object: 'block',
        type: 'paragraph',
        paragraph: {
          rich_text: [{
            text: { content: `${emoji} ${deal.title} - €${deal.value.toLocaleString()}` },
            annotations: { bold: true }
          }]
        }
      }]
    });

    await notion.blocks.children.append({
      block_id: PAGE_ID,
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
            rich_text: [{ text: { content: `Stage: ${deal.stage} | ${deal.dagen} dagen` } }]
          }
        }
      ]
    });

    console.log(`✅ ${deal.title}`);
  }

  // Commands
  await notion.blocks.children.append({
    block_id: PAGE_ID,
    children: [{
      object: 'block',
      type: 'heading_3',
      heading_3: {
        rich_text: [{ text: { content: '⚡ Update Commands' } }]
      }
    }]
  });

  await notion.blocks.children.append({
    block_id: PAGE_ID,
    children: [{
      object: 'block',
      type: 'code',
      code: {
        rich_text: [{ text: { content: 'python3 pipedrive-open-deals-export.py --notion' } }],
        language: 'bash'
      }
    }]
  });

  await notion.blocks.children.append({
    block_id: PAGE_ID,
    children: [{ object: 'block', type: 'divider', divider: {} }]
  });

  console.log('\n✅ DEALS TAB UPLOADED!');
  console.log('📄 https://notion.so/27c2252cbb1581a5bbfcef3736d7c14e\n');
}

upload().catch(err => console.error('❌', err.message));
