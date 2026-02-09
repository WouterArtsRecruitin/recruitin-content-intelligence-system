#!/usr/bin/env node
const { Client } = require('@notionhq/client');
const fs = require('fs');
const path = require('path');

const notion = new Client({ auth: process.env.NOTION_API_KEY || 'ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3' });
const PAGE_ID = '27c2252cbb1581a5bbfcef3736d7c14e'; // Correct ID from user

function findLatestReport() {
  const reportsDir = path.join(__dirname, 'reports');
  const reports = fs.readdirSync(reportsDir)
    .filter(f => f.startsWith('top-articles-') && f.endsWith('.json'))
    .sort()
    .reverse();

  if (reports.length === 0) {
    throw new Error('No top-articles JSON found. Run select-top-articles.js first.');
  }

  return path.join(reportsDir, reports[0]);
}

function getWeekInfo(dateStr) {
  const date = new Date(dateStr);
  const weekNum = Math.ceil((date.getDate()) / 7);
  const months = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
                  'juli', 'augustus', 'september', 'oktober', 'november', 'december'];
  return {
    week: weekNum,
    month: months[date.getMonth()],
    year: date.getFullYear(),
    day: date.getDate()
  };
}

async function upload() {
  console.log('📤 Uploading to LinkedIn Intelligence Hub...\n');

  // Find latest report
  const reportPath = findLatestReport();
  const reportFile = path.basename(reportPath);
  const dateMatch = reportFile.match(/top-articles-(\d{4}-\d{2}-\d{2})\.json/);
  const reportDate = dateMatch ? dateMatch[1] : new Date().toISOString().split('T')[0];

  console.log(`📄 Using report: ${reportFile}\n`);

  const reportData = JSON.parse(fs.readFileSync(reportPath));
  const top10 = reportData.top_10;

  if (!top10 || top10.length === 0) {
    throw new Error('No articles found in report');
  }

  const weekInfo = getWeekInfo(reportDate);
  const heading = `📰 Week ${weekInfo.week} - ${weekInfo.day} ${weekInfo.month} ${weekInfo.year} - Top 10 News`;

  // Add heading
  await notion.blocks.children.append({
    block_id: PAGE_ID,
    children: [{
      type: 'heading_2',
      heading_2: {
        rich_text: [{ text: { content: heading } }]
      }
    }]
  });

  // Add divider
  await notion.blocks.children.append({
    block_id: PAGE_ID,
    children: [{ type: 'divider', divider: {} }]
  });

  // Add each article
  for (let i = 0; i < top10.length; i++) {
    const article = top10[i];
    const star = i === 0 ? ' ⭐' : '';
    
    // Title
    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        type: 'paragraph',
        paragraph: {
          rich_text: [{
            text: { content: `${i + 1}.${star} ${article.title} (${article.score}/100)` },
            annotations: { bold: i === 0 }
          }]
        }
      }]
    });
    
    // URL
    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        type: 'bulleted_list_item',
        bulleted_list_item: {
          rich_text: [{ text: { content: article.url, link: { url: article.url } } }]
        }
      }]
    });
    
    // Gebruikt status
    const gebruikt = i === 0 ? '✅ Gebruikt voor content (LinkedIn + Blog)' : '❌ Niet gebruikt';
    await notion.blocks.children.append({
      block_id: PAGE_ID,
      children: [{
        type: 'bulleted_list_item',
        bulleted_list_item: {
          rich_text: [{ text: { content: gebruikt } }]
        }
      }]
    });
    
    console.log(`✅ ${i + 1}. ${article.title.substring(0, 60)}...`);
  }

  // Add summary callout
  await notion.blocks.children.append({
    block_id: PAGE_ID,
    children: [{
      type: 'callout',
      callout: {
        rich_text: [{
          text: { content: `📊 Deze week: Beste artikel gebruikt voor LinkedIn Wouter (contrarian) + Recruitin (data story) + Blog. Review: CONTENT-REVIEW-DOCUMENT.md` }
        }],
        icon: { emoji: '✅' },
        color: 'green_background'
      }
    }]
  });

  console.log('\n✅ TOP 10 UPLOADED TO NOTION!');
  console.log('📄 Check: https://notion.so/27c2252cbb1581a5bbfcef3736d7c14e');
}

upload().catch(err => {
  console.error('❌', err.message);
  if (err.code === 'object_not_found') {
    console.log('\n🔧 Share page with integration first:');
    console.log('Notion → Page → ... → Connections → Add integration');
  }
});
