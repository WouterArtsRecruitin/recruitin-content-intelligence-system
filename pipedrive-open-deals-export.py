#!/usr/bin/env python3
"""
Pipedrive Open Deals Export
============================
Exporteert alle openstaande deals naar Excel/Notion

Usage:
    python pipedrive-open-deals-export.py
    python pipedrive-open-deals-export.py --excel
    python pipedrive-open-deals-export.py --notion
    python pipedrive-open-deals-export.py --demo

Output:
    - Excel: open-deals-[DATE].xlsx
    - Notion: Upload naar dashboard
    - Console: Formatted table
"""

import os
import sys
import requests
from datetime import datetime
from typing import List, Dict

# ============================================================================
# CONFIGURATION
# ============================================================================

PIPEDRIVE_API_KEY = os.getenv("PIPEDRIVE_API_KEY", "YOUR_KEY_HERE")
NOTION_API_KEY = "ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3"
NOTION_PAGE_ID = "27c2252cbb1581a5bbfcef3736d7c14e"

# ============================================================================
# DEMO DATA
# ============================================================================

DEMO_DEALS = [
    {
        'id': 12345,
        'title': 'Siemens Enschede - Senior Automation Engineer',
        'value': 28000,
        'currency': 'EUR',
        'org_name': 'Siemens Nederland N.V.',
        'person_name': 'Jan de Vries',
        'stage_id': 95,
        'stage_name': 'Stage 2 - Proposal',
        'add_time': '2025-12-22',
        'update_time': '2026-01-10',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 21,
        'status': 'open'
    },
    {
        'id': 12346,
        'title': 'ASML Veldhoven - Lead Control Systems Engineer',
        'value': 24000,
        'currency': 'EUR',
        'org_name': 'ASML Netherlands B.V.',
        'person_name': 'Peter Jansen',
        'stage_id': 105,
        'stage_name': 'Stage 3 - Negotiation',
        'add_time': '2026-01-02',
        'update_time': '2026-01-11',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 12,
        'status': 'open'
    },
    {
        'id': 12347,
        'title': 'Shell Rotterdam - SCADA Specialist',
        'value': 22000,
        'currency': 'EUR',
        'org_name': 'Shell Nederland B.V.',
        'person_name': 'Sarah van Dam',
        'stage_id': 95,
        'stage_name': 'Stage 2 - Proposal',
        'add_time': '2026-01-04',
        'update_time': '2026-01-11',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 8,
        'status': 'open'
    },
    {
        'id': 12348,
        'title': 'Dow Terneuzen - Instrumentation Engineer',
        'value': 19000,
        'currency': 'EUR',
        'org_name': 'Dow Benelux B.V.',
        'person_name': 'Mark Peters',
        'stage_id': 110,
        'stage_name': 'Stage 3 - Negotiation',
        'add_time': '2026-01-07',
        'update_time': '2026-01-12',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 5,
        'status': 'open'
    },
    {
        'id': 12349,
        'title': 'Nouryon Deventer - Process Automation Engineer',
        'value': 18000,
        'currency': 'EUR',
        'org_name': 'Nouryon Chemicals B.V.',
        'person_name': 'Lisa de Jong',
        'stage_id': 95,
        'stage_name': 'Stage 2 - Proposal',
        'add_time': '2025-12-28',
        'update_time': '2026-01-08',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 15,
        'status': 'open'
    },
    {
        'id': 12350,
        'title': 'Vanderlande Veghel - Automation Engineer',
        'value': 16000,
        'currency': 'EUR',
        'org_name': 'Vanderlande Industries B.V.',
        'person_name': 'Tom Bakker',
        'stage_id': 95,
        'stage_name': 'Stage 2 - Proposal',
        'add_time': '2025-12-25',
        'update_time': '2026-01-05',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 18,
        'status': 'open'
    },
    {
        'id': 12351,
        'title': 'Gasunie Groningen - SCADA Engineer',
        'value': 15000,
        'currency': 'EUR',
        'org_name': 'Gasunie Nederland N.V.',
        'person_name': 'Anna Smit',
        'stage_id': 95,
        'stage_name': 'Stage 2 - Proposal',
        'add_time': '2025-12-27',
        'update_time': '2026-01-06',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 16,
        'status': 'open'
    },
    {
        'id': 12352,
        'title': 'TechCorp Arnhem - Medior Automation',
        'value': 14000,
        'currency': 'EUR',
        'org_name': 'TechCorp Automation B.V.',
        'person_name': 'Piet Visser',
        'stage_id': 95,
        'stage_name': 'Stage 2 - Proposal',
        'add_time': '2025-12-29',
        'update_time': '2026-01-10',
        'owner_name': 'Wouter Arts',
        'days_in_stage': 14,
        'status': 'open'
    }
]

# Add more demo deals (total 65)
for i in range(8, 65):
    DEMO_DEALS.append({
        'id': 12300 + i,
        'title': f'Deal {i} - Technical Role',
        'value': 10000 + (i * 500),
        'currency': 'EUR',
        'org_name': f'Company {i} B.V.',
        'person_name': f'Contact {i}',
        'stage_id': 95,
        'stage_name': 'Stage 2 - Proposal',
        'add_time': '2026-01-01',
        'update_time': '2026-01-10',
        'owner_name': 'Wouter Arts',
        'days_in_stage': i % 20,
        'status': 'open'
    })

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def fetch_pipedrive_deals() -> List[Dict]:
    """Fetch open deals from Pipedrive API"""

    if PIPEDRIVE_API_KEY == "YOUR_KEY_HERE":
        print("⚠️  Using DEMO data (65 deals)\n")
        print("Set PIPEDRIVE_API_KEY voor live data\n")
        return DEMO_DEALS

    try:
        print("📡 Fetching deals from Pipedrive...")

        url = "https://api.pipedrive.com/v1/deals"
        params = {
            'api_token': PIPEDRIVE_API_KEY,
            'status': 'open',
            'limit': 500
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            deals = data.get('data', [])
            print(f"✅ Fetched {len(deals)} open deals\n")
            return deals
        else:
            print(f"❌ Pipedrive API error: {response.status_code}")
            print("⚠️  Using demo data instead\n")
            return DEMO_DEALS

    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️  Using demo data\n")
        return DEMO_DEALS

def format_as_table(deals: List[Dict]) -> str:
    """Format deals as markdown table"""

    table = f"""# 📊 OPENSTAANDE DEALS - {datetime.now().strftime('%d %B %Y')}

**Totaal**: {len(deals)} open deals
**Pipeline Value**: €{sum(d.get('value', 0) for d in deals):,}

---

## 📋 ALLE OPENSTAANDE DEALS

| # | Deal Naam | Organisatie | Contact Persoon | Waarde | Stage | Datum | Dagen | Owner |
|---|-----------|-------------|-----------------|--------|-------|-------|-------|-------|
"""

    # Sort by value (highest first)
    sorted_deals = sorted(deals, key=lambda x: x.get('value', 0), reverse=True)

    for i, deal in enumerate(sorted_deals, 1):
        # Add warning emoji voor stuck deals
        stuck_emoji = '🚨' if deal.get('days_in_stage', 0) > 14 else ''

        table += f"| {i} | {stuck_emoji}{deal.get('title', 'N/A')[:40]} | "
        table += f"{deal.get('org_name', 'N/A')[:25]} | "
        table += f"{deal.get('person_name', 'N/A')} | "
        table += f"€{deal.get('value', 0):,} | "
        table += f"{deal.get('stage_name', 'N/A')[:20]} | "
        table += f"{deal.get('add_time', 'N/A')[:10]} | "
        table += f"{deal.get('days_in_stage', 0)}d | "
        table += f"{deal.get('owner_name', 'N/A')} |\n"

    # Summary
    table += f"""
---

## 📊 SAMENVATTING

**Pipeline Breakdown**:
- Totaal deals: {len(deals)}
- Totale waarde: €{sum(d.get('value', 0) for d in deals):,}
- Gemiddelde deal: €{int(sum(d.get('value', 0) for d in deals) / len(deals)) if deals else 0:,}

**Stage Breakdown**:
"""

    # Count per stage
    from collections import defaultdict
    stage_counts = defaultdict(lambda: {'count': 0, 'value': 0})

    for deal in deals:
        stage = deal.get('stage_name', 'Unknown')
        stage_counts[stage]['count'] += 1
        stage_counts[stage]['value'] += deal.get('value', 0)

    for stage, data in sorted(stage_counts.items(), key=lambda x: x[1]['value'], reverse=True):
        table += f"- {stage}: {data['count']} deals (€{data['value']:,})\n"

    # Stuck deals warning
    stuck_count = sum(1 for d in deals if d.get('days_in_stage', 0) > 14)
    if stuck_count > 0:
        stuck_value = sum(d.get('value', 0) for d in deals if d.get('days_in_stage', 0) > 14)
        table += f"\n🚨 **URGENT**: {stuck_count} deals stuck >14 dagen (€{stuck_value:,} at risk)\n"

    return table

def export_to_excel(deals: List[Dict], filename: str = None):
    """Export deals to Excel file"""

    try:
        import pandas as pd

        # Convert to DataFrame
        df_data = []
        for deal in deals:
            df_data.append({
                'Deal Naam': deal.get('title', ''),
                'Organisatie': deal.get('org_name', ''),
                'Contact Persoon': deal.get('person_name', ''),
                'Waarde (€)': deal.get('value', 0),
                'Stage': deal.get('stage_name', ''),
                'Datum Toegevoegd': deal.get('add_time', ''),
                'Laatste Update': deal.get('update_time', ''),
                'Dagen in Stage': deal.get('days_in_stage', 0),
                'Owner': deal.get('owner_name', ''),
                'Deal ID': deal.get('id', ''),
                'Status': '🚨 STUCK' if deal.get('days_in_stage', 0) > 14 else 'OK'
            })

        df = pd.DataFrame(df_data)

        # Sort by value (highest first)
        df = df.sort_values('Waarde (€)', ascending=False)

        # Generate filename
        if not filename:
            filename = f"open-deals-{datetime.now().strftime('%Y-%m-%d')}.xlsx"

        # Export
        df.to_excel(filename, index=False, sheet_name='Openstaande Deals')

        print(f"✅ Excel exported: {filename}")
        print(f"📊 {len(df)} deals | €{df['Waarde (€)'].sum():,.0f} total value\n")

        return filename

    except ImportError:
        print("❌ pandas not installed. Install: pip install pandas openpyxl")
        return None

def upload_to_notion(deals: List[Dict]):
    """Upload deals table to Notion"""

    try:
        from notion_client import Client

        notion = Client(auth=NOTION_API_KEY)

        print("📤 Uploading to Notion...\n")

        # Add heading
        notion.blocks.children.append(
            block_id=NOTION_PAGE_ID,
            children=[
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{
                            "text": {"content": f"📊 Openstaande Deals - {datetime.now().strftime('%d %B %Y')}"}
                        }],
                        "color": "orange_background"
                    }
                }
            ]
        )

        # Summary callout
        total_value = sum(d.get('value', 0) for d in deals)
        stuck_count = sum(1 for d in deals if d.get('days_in_stage', 0) > 14)

        notion.blocks.children.append(
            block_id=NOTION_PAGE_ID,
            children=[{
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "text": {
                            "content": f"📊 Totaal: {len(deals)} deals | €{total_value:,} pipeline value | 🚨 {stuck_count} stuck >14d"
                        }
                    }],
                    "icon": {"emoji": "💰"},
                    "color": "blue_background"
                }
            }]
        )

        # Top 10 deals table
        notion.blocks.children.append(
            block_id=NOTION_PAGE_ID,
            children=[{
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "💰 Top 10 Deals (By Value)"}}]
                }
            }]
        )

        sorted_deals = sorted(deals, key=lambda x: x.get('value', 0), reverse=True)[:10]

        for i, deal in enumerate(sorted_deals, 1):
            stuck = "🚨 " if deal.get('days_in_stage', 0) > 14 else ""

            notion.blocks.children.append(
                block_id=NOTION_PAGE_ID,
                children=[{
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{
                            "text": {
                                "content": f"{stuck}{deal.get('title')} - €{deal.get('value', 0):,} | {deal.get('org_name')} | Contact: {deal.get('person_name')} | {deal.get('days_in_stage')}d in stage"
                            }
                        }]
                    }
                }]
            )

        print(f"✅ Uploaded to Notion!")
        print(f"📄 View: https://notion.so/{NOTION_PAGE_ID.replace('-', '')}\n")

    except Exception as e:
        print(f"❌ Notion upload failed: {e}")
        print("💡 Use --excel to export to file instead\n")

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Export Pipedrive open deals")
    parser.add_argument("--excel", action="store_true", help="Export to Excel")
    parser.add_argument("--notion", action="store_true", help="Upload to Notion")
    parser.add_argument("--demo", action="store_true", help="Force demo data")
    parser.add_argument("-o", "--output", help="Output filename")

    args = parser.parse_args()

    # Fetch deals
    if args.demo or PIPEDRIVE_API_KEY == "YOUR_KEY_HERE":
        deals = DEMO_DEALS
        print("⚠️  Using DEMO data (65 deals)\n")
    else:
        deals = fetch_pipedrive_deals()

    # Output
    if args.excel:
        export_to_excel(deals, args.output)
    elif args.notion:
        upload_to_notion(deals)
    else:
        # Console table
        table = format_as_table(deals)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(table)
            print(f"✅ Saved to: {args.output}\n")
        else:
            print(table)

if __name__ == "__main__":
    main()
