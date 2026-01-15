#!/usr/bin/env python3
"""
Build Master Management Dashboard in Notion
With LIVE Pipedrive Data
"""

import requests
from notion_client import Client
from datetime import datetime
from collections import defaultdict

# API Keys
PIPEDRIVE_API_KEY = "e689cc5b89affb98d93b1af95d115851f2d3d492"
NOTION_API_KEY = "ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3"
NOTION_PAGE_ID = "27c2252cbb1581a5bbfcef3736d7c14e"

notion = Client(auth=NOTION_API_KEY)

print("🚀 Building Master Management Dashboard with LIVE data...\n")

# ============================================================================
# FETCH PIPEDRIVE DATA
# ============================================================================

def get_pipedrive_data():
    """Fetch live Pipedrive data"""
    
    print("📡 Fetching from Pipedrive...")
    
    base_url = "https://api.pipedrive.com/v1"
    
    try:
        # Get all open deals
        response = requests.get(
            f"{base_url}/deals",
            params={'api_token': PIPEDRIVE_API_KEY, 'status': 'open', 'limit': 500}
        )
        
        if response.status_code == 200:
            deals_data = response.json().get('data', []) or []
            print(f"✅ {len(deals_data)} deals fetched")
        else:
            print(f"⚠️  Pipedrive API error: {response.status_code}")
            deals_data = []
        
        # Get deals summary
        response2 = requests.get(
            f"{base_url}/deals/summary",
            params={'api_token': PIPEDRIVE_API_KEY, 'status': 'open'}
        )
        
        summary = response2.json().get('data', {}) if response2.status_code == 200 else {}
        
        return deals_data, summary
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return [], {}

deals, summary = get_pipedrive_data()

if not deals:
    print("⚠️  No data - using placeholders\n")
    total_deals = 0
    total_value = 0
else:
    total_deals = len(deals)
    total_value = sum(d.get('value', 0) or 0 for d in deals)
    print(f"💰 Total pipeline: {total_deals} deals, €{total_value:,}\n")

# ============================================================================
# BUILD DASHBOARD
# ============================================================================

print("📊 Building Master Dashboard in Notion...\n")

# Clear old content first (optional - skip for now)

# SECTION 1: Header
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[
        {"object": "block", "type": "divider", "divider": {}},
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"text": {"content": "📊 MASTER MANAGEMENT DASHBOARD"}}],
                "color": "blue_background"
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "text": {"content": f"Recruitin B.V. | Update: {datetime.now().strftime('%d %B %Y, %H:%M')} | Live Pipedrive Data"}
                }]
            }
        }
    ]
)
print("✅ Header")

# SECTION 2: Executive Summary
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"text": {"content": "🎯 Executive Summary"}}]
        }
    }]
)

notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{
                "text": {"content": f"Pipeline: {total_deals} deals | €{total_value:,} | Status: {'✅ Healthy' if total_deals >= 50 else '⚠️ Build Pipeline'}"}
            }],
            "icon": {"emoji": "💰"},
            "color": "green_background" if total_deals >= 50 else "yellow_background"
        }
    }]
)
print("✅ Executive Summary")

# SECTION 3: Top 10 KPIs Table
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"text": {"content": "📊 Top 10 KPIs"}}]
        }
    }]
)

# KPIs as bullets (simplified)
kpis = [
    f"1. Pipeline Value: €{total_value:,}",
    f"2. Total Deals: {total_deals}",
    "3. Revenue MTD: [Update manual]",
    "4. Placements MTD: [Update manual]",
    "5. Win Rate: [Calculate]",
    "6. Time-to-Fill: [Track]",
    "7. New Deals: [Count this month]",
    "8. Stage 2 Conversion: [Calculate]",
    "9. Activities: [Count]",
    "10. Content Posts: [Track]"
]

for kpi in kpis:
    notion.blocks.children.append(
        block_id=NOTION_PAGE_ID,
        children=[{
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": kpi}}]
            }
        }]
    )

print("✅ Top 10 KPIs")

# SECTION 4: Omzet per Dienst
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"text": {"content": "💰 Omzet per Dienstverlening"}}]
        }
    }]
)

diensten = [
    {"naam": "W&S (Werving & Selectie)", "deals": "[?]", "omzet": "[€]", "pipeline": "[€]"},
    {"naam": "RPO (Recruitment Process Outsourcing)", "deals": "[?]", "omzet": "[€]", "pipeline": "[€]"},
    {"naam": "Interim", "deals": "[?]", "omzet": "[€]", "pipeline": "[€]"},
    {"naam": "RMA (Recruitment Marketing Advies)", "deals": "[?]", "omzet": "[€]", "pipeline": "[€]"}
]

for dienst in diensten:
    notion.blocks.children.append(
        block_id=NOTION_PAGE_ID,
        children=[{
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "text": {"content": f"{dienst['naam']}: {dienst['deals']} deals | Omzet: {dienst['omzet']} | Pipeline: {dienst['pipeline']}"}
                }]
            }
        }]
    )

print("✅ Omzet per Dienst")

# SECTION 5: Top 10 Deals
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"text": {"content": "💼 Top 10 Deals (By Value)"}}]
        }
    }]
)

if deals:
    sorted_deals = sorted(deals, key=lambda x: x.get('value', 0) or 0, reverse=True)[:10]
    
    for i, deal in enumerate(sorted_deals, 1):
        title = deal.get('title', 'N/A')
        value = deal.get('value', 0) or 0
        org = deal.get('org_name', 'N/A')
        
        notion.blocks.children.append(
            block_id=NOTION_PAGE_ID,
            children=[{
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{
                        "text": {"content": f"{i}. {title} - €{value:,} | {org}"}
                    }]
                }
            }]
        )
    
    print("✅ Top 10 Deals (LIVE DATA!)")
else:
    notion.blocks.children.append(
        block_id=NOTION_PAGE_ID,
        children=[{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": "No deals found - check Pipedrive connection"}}]
            }
        }]
    )
    print("⚠️  No deals to display")

# SECTION 6: Week Priorities
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"text": {"content": "🎯 Week Priorities"}}]
        }
    }]
)

priorities = [
    "Stage 2 bottleneck: Focus stuck deals",
    "Close 2 Stage 3 deals (target)",
    "Score nieuwe leads (JobDigger batch)"
]

for p in priorities:
    notion.blocks.children.append(
        block_id=NOTION_PAGE_ID,
        children=[{
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"text": {"content": p}}],
                "checked": False
            }
        }]
    )

print("✅ Week Priorities")

# SECTION 7: Quick Commands
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"text": {"content": "⚡ Update Commands"}}]
        }
    }]
)

notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{
                "text": {"content": "# Update dashboard (Maandag 10:00)\npython3 build-master-dashboard.py"}
            }],
            "language": "bash"
        }
    }]
)

print("✅ Quick Commands")

# Final
notion.blocks.children.append(
    block_id=NOTION_PAGE_ID,
    children=[{"object": "block", "type": "divider", "divider": {}}]
)

print("\n" + "="*70)
print("🎉 MASTER DASHBOARD CREATED!")
print("="*70)
print(f"\n📊 Live Data Used:")
print(f"   • Deals: {total_deals}")
print(f"   • Pipeline: €{total_value:,}")
print(f"\n📄 View: https://notion.so/{NOTION_PAGE_ID.replace('-', '')}")
print(f"\n💡 Update elke maandag: python3 build-master-dashboard.py")
print()
