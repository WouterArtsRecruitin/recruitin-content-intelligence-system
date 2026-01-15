#!/usr/bin/env python3
"""
Pipedrive Weekly Dashboard Generator
=====================================
Haalt Pipedrive data en genereert weekly KPI dashboard in Notion

Usage:
    python pipedrive-weekly-dashboard.py
    python pipedrive-weekly-dashboard.py --week 1
    python pipedrive-weekly-dashboard.py --upload-notion

Author: Recruitin B.V.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Pipedrive & Notion configuration"""

    # API Keys (from environment or hardcoded)
    PIPEDRIVE_API_KEY = os.getenv("PIPEDRIVE_API_KEY", "YOUR_KEY_HERE")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY", "ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3")

    # Notion Page voor dashboard
    NOTION_HUB_ID = "27c2252cbb1581a5bbfcef3736d7c14e"

    # Pipedrive Pipeline IDs (update met jouw pipeline IDs!)
    PIPELINE_IDS = {
        'main': 12,  # Technische Vacatures pipeline
        'jobdigger': 14  # JobDigger automation pipeline (als je die hebt)
    }

    # Stage IDs (update met jouw stage IDs!)
    CRITICAL_STAGES = {
        'stage_2': 95,  # Stage 2 bottleneck
        'proposal': 105,
        'negotiation': 110,
        'closed_won': 115
    }

    # Targets (weekly)
    WEEKLY_TARGETS = {
        'new_deals': 5,
        'deals_moved': 8,
        'deals_closed': 2,
        'revenue_target': 36000,  # €36k/week = €156k/month
        'activities': 25,
        'calls': 15,
        'meetings': 5
    }


# ============================================================================
# PIPEDRIVE API CLIENT
# ============================================================================

class PipedriveClient:
    """Simplified Pipedrive API client"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pipedrive.com/v1"

    def _request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request"""
        params = params or {}
        params['api_token'] = self.api_key

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Pipedrive API error: {response.status_code}")

    def get_deals(self, status: str = 'open', limit: int = 500) -> List[Dict]:
        """Get deals"""
        data = self._request('deals', {'status': status, 'limit': limit})
        return data.get('data', []) or []

    def get_activities(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get activities"""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        data = self._request('activities', params)
        return data.get('data', []) or []

    def get_deals_summary(self) -> Dict:
        """Get deals summary"""
        data = self._request('deals/summary')
        return data.get('data', {})


# ============================================================================
# DASHBOARD GENERATOR
# ============================================================================

class WeeklyDashboard:
    """Generates weekly Pipedrive dashboard"""

    def __init__(self, pipedrive_key: str = None):
        self.pd = PipedriveClient(pipedrive_key or Config.PIPEDRIVE_API_KEY)
        self.use_demo = not pipedrive_key and Config.PIPEDRIVE_API_KEY == "YOUR_KEY_HERE"

    def get_week_dates(self, weeks_ago: int = 0) -> tuple:
        """Get Monday-Sunday of specific week"""
        today = datetime.now()
        monday = today - timedelta(days=today.weekday()) - timedelta(weeks=weeks_ago)
        sunday = monday + timedelta(days=6)
        return monday, sunday

    def fetch_weekly_data(self, weeks_ago: int = 0) -> Dict:
        """Fetch all Pipedrive data for the week"""

        if self.use_demo:
            print("⚠️  Using DEMO data (set PIPEDRIVE_API_KEY for live data)\n")
            return self._get_demo_data()

        monday, sunday = self.get_week_dates(weeks_ago)

        print(f"📊 Fetching Pipedrive data for week {monday.strftime('%d %b')} - {sunday.strftime('%d %b')}...")

        try:
            # Get all open deals
            deals = self.pd.get_deals(status='open')

            # Get this week's activities
            activities = self.pd.get_activities(
                start_date=monday.strftime('%Y-%m-%d'),
                end_date=sunday.strftime('%Y-%m-%d')
            )

            # Get summary
            summary = self.pd.get_deals_summary()

            # Process data
            data = self._process_pipedrive_data(deals, activities, summary, monday, sunday)

            print(f"✅ Data fetched: {len(deals)} deals, {len(activities)} activities\n")

            return data

        except Exception as e:
            print(f"❌ Pipedrive fetch failed: {e}")
            print("⚠️  Using demo data instead\n")
            return self._get_demo_data()

    def _process_pipedrive_data(self, deals: List, activities: List, summary: Dict, monday: datetime, sunday: datetime) -> Dict:
        """Process raw Pipedrive data into metrics"""

        # Stage 2 deals (bottleneck analysis)
        stage_2_deals = [d for d in deals if d.get('stage_id') == Config.CRITICAL_STAGES.get('stage_2')]
        stage_2_stuck = [d for d in stage_2_deals if self._days_in_stage(d) > 14]

        # This week metrics
        week_deals_added = [d for d in deals if self._is_in_week(d.get('add_time'), monday, sunday)]
        week_deals_moved = [a for a in activities if a.get('type') == 'deal_update']
        week_deals_won = [d for d in deals if d.get('status') == 'won' and self._is_in_week(d.get('won_time'), monday, sunday)]

        # Activity breakdown
        calls = [a for a in activities if a.get('type') == 'call']
        meetings = [a for a in activities if a.get('type') == 'meeting']
        emails = [a for a in activities if a.get('type') == 'email']

        # Revenue
        week_revenue = sum(d.get('value', 0) for d in week_deals_won)
        pipeline_value = sum(d.get('value', 0) for d in deals)

        return {
            'period': {'start': monday, 'end': sunday},
            'pipeline': {
                'total_deals': len(deals),
                'total_value': pipeline_value,
                'stage_2_count': len(stage_2_deals),
                'stage_2_stuck': len(stage_2_stuck),
                'stage_2_value': sum(d.get('value', 0) for d in stage_2_deals)
            },
            'weekly': {
                'deals_added': len(week_deals_added),
                'deals_moved': len(week_deals_moved),
                'deals_won': len(week_deals_won),
                'revenue': week_revenue
            },
            'activities': {
                'total': len(activities),
                'calls': len(calls),
                'meetings': len(meetings),
                'emails': len(emails)
            },
            'top_deals': self._get_top_deals(deals, 5),
            'stuck_deals': stage_2_stuck[:5],  # Top 5 stuck
            'urgent_actions': self._get_urgent_actions(deals, activities)
        }

    def _days_in_stage(self, deal: Dict) -> int:
        """Calculate days in current stage"""
        stage_change_time = deal.get('stage_change_time')
        if not stage_change_time:
            return 0

        changed = datetime.fromisoformat(stage_change_time.replace('Z', '+00:00'))
        return (datetime.now() - changed).days

    def _is_in_week(self, timestamp: str, monday: datetime, sunday: datetime) -> bool:
        """Check if timestamp is in given week"""
        if not timestamp:
            return False

        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return monday <= dt <= sunday
        except:
            return False

    def _get_top_deals(self, deals: List, n: int) -> List[Dict]:
        """Get top N deals by value"""
        sorted_deals = sorted(deals, key=lambda x: x.get('value', 0), reverse=True)
        return [{
            'title': d.get('title'),
            'value': d.get('value'),
            'stage': d.get('stage_id'),
            'owner': d.get('owner_name'),
            'days': self._days_in_stage(d)
        } for d in sorted_deals[:n]]

    def _get_urgent_actions(self, deals: List, activities: List) -> List[str]:
        """Generate urgent action items"""
        actions = []

        # Stuck deals
        stage_2 = [d for d in deals if d.get('stage_id') == Config.CRITICAL_STAGES.get('stage_2')]
        stuck = [d for d in stage_2 if self._days_in_stage(d) > 14]

        if stuck:
            actions.append(f"🚨 {len(stuck)} deals stuck >14d in Stage 2 - URGENT review needed")

        # High value deals
        high_value = [d for d in deals if d.get('value', 0) > 20000]
        if high_value:
            actions.append(f"💰 {len(high_value)} high-value deals (>€20k) - prioritize these")

        # No activity recently
        # (Would need more complex logic to check last activity date)

        return actions[:5]  # Top 5 urgent

    def _get_demo_data(self) -> Dict:
        """Demo data for testing"""
        monday, sunday = self.get_week_dates(0)

        return {
            'period': {'start': monday, 'end': sunday},
            'pipeline': {
                'total_deals': 65,
                'total_value': 952000,
                'stage_2_count': 18,
                'stage_2_stuck': 12,
                'stage_2_value': 310000
            },
            'weekly': {
                'deals_added': 7,
                'deals_moved': 9,
                'deals_won': 2,
                'revenue': 32000
            },
            'activities': {
                'total': 28,
                'calls': 15,
                'meetings': 5,
                'emails': 8
            },
            'top_deals': [
                {'title': 'Siemens Enschede - Senior Automation', 'value': 28000, 'stage': 95, 'owner': 'Wouter', 'days': 21},
                {'title': 'ASML Veldhoven - Lead Control Systems', 'value': 24000, 'stage': 105, 'owner': 'Wouter', 'days': 12},
                {'title': 'Shell Rotterdam - SCADA Specialist', 'value': 22000, 'stage': 95, 'owner': 'Wouter', 'days': 8},
                {'title': 'Dow Terneuzen - Instrumentation Engineer', 'value': 19000, 'stage': 110, 'owner': 'Wouter', 'days': 5},
                {'title': 'Nouryon Deventer - Process Automation', 'value': 18000, 'stage': 95, 'owner': 'Wouter', 'days': 15}
            ],
            'stuck_deals': [
                {'title': 'Siemens Enschede', 'value': 28000, 'days': 21, 'stage': 95},
                {'title': 'Vanderlande Veghel', 'value': 16000, 'days': 18, 'stage': 95},
                {'title': 'Gasunie Groningen', 'value': 15000, 'days': 16, 'stage': 95}
            ],
            'urgent_actions': [
                '🚨 12 deals stuck >14d in Stage 2 - URGENT review',
                '💰 5 high-value deals (>€20k) - prioritize',
                '📞 3 deals geen activiteit in 7 dagen - follow-up needed'
            ]
        }

    def generate_dashboard(self, weeks_ago: int = 0) -> str:
        """Generate complete weekly dashboard"""

        data = self.fetch_weekly_data(weeks_ago)
        period = data['period']
        week_num = period['start'].isocalendar()[1]

        # Generate markdown dashboard
        dashboard = f"""# 📊 PIPEDRIVE WEEKLY DASHBOARD - Week {week_num}

**Periode**: {period['start'].strftime('%d %b')} - {period['end'].strftime('%d %b %Y')}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Voor**: Wouter Arts | Recruitin B.V.

---

## 🎯 EXECUTIVE SUMMARY

### Pipeline Health

| Metric | Value | Status |
|--------|-------|--------|
| **Total Open Deals** | {data['pipeline']['total_deals']} | {'✅' if data['pipeline']['total_deals'] >= 50 else '⚠️'} |
| **Pipeline Value** | €{data['pipeline']['total_value']:,} | {'✅' if data['pipeline']['total_value'] >= 800000 else '📈'} |
| **Stage 2 Deals** | {data['pipeline']['stage_2_count']} (€{data['pipeline']['stage_2_value']:,}) | {'🚨' if data['pipeline']['stage_2_stuck'] > 10 else '✅'} |
| **Stuck >14d** | {data['pipeline']['stage_2_stuck']} deals | {'🚨' if data['pipeline']['stage_2_stuck'] > 5 else '✅'} |

### Weekly Performance

| Metric | This Week | Target | Status |
|--------|-----------|--------|--------|
| **New Deals** | {data['weekly']['deals_added']} | {Config.WEEKLY_TARGETS['new_deals']} | {'✅' if data['weekly']['deals_added'] >= Config.WEEKLY_TARGETS['new_deals'] else '📈'} |
| **Deals Moved** | {data['weekly']['deals_moved']} | {Config.WEEKLY_TARGETS['deals_moved']} | {'✅' if data['weekly']['deals_moved'] >= Config.WEEKLY_TARGETS['deals_moved'] else '📈'} |
| **Deals Closed** | {data['weekly']['deals_won']} | {Config.WEEKLY_TARGETS['deals_closed']} | {'✅' if data['weekly']['deals_won'] >= Config.WEEKLY_TARGETS['deals_closed'] else '⚠️'} |
| **Revenue** | €{data['weekly']['revenue']:,} | €{Config.WEEKLY_TARGETS['revenue_target']:,} | {'✅' if data['weekly']['revenue'] >= Config.WEEKLY_TARGETS['revenue_target'] else '📈'} |

### Activity Metrics

| Activity | This Week | Target | Status |
|----------|-----------|--------|--------|
| **Total Activities** | {data['activities']['total']} | {Config.WEEKLY_TARGETS['activities']} | {'✅' if data['activities']['total'] >= Config.WEEKLY_TARGETS['activities'] else '📈'} |
| **Calls** | {data['activities']['calls']} | {Config.WEEKLY_TARGETS['calls']} | {'✅' if data['activities']['calls'] >= Config.WEEKLY_TARGETS['calls'] else '📈'} |
| **Meetings** | {data['activities']['meetings']} | {Config.WEEKLY_TARGETS['meetings']} | {'✅' if data['activities']['meetings'] >= Config.WEEKLY_TARGETS['meetings'] else '⚠️'} |
| **Emails** | {data['activities']['emails']} | - | ℹ️ |

---

## 💰 TOP 5 DEALS (By Value)

"""
        # Top deals
        for i, deal in enumerate(data['top_deals'], 1):
            emoji = "🔥" if deal.get("days", 0) < 14 else ('⚠️' if deal['days'] > 21 else '📊')
            dashboard += f"""{i}. {emoji} **{deal['title']}** - €{deal['value']:,}
   - Stage ID: {deal['stage']} | Days in stage: {deal['days']} | Owner: {deal['owner']}

"""

        # Stuck deals
        dashboard += """---

## 🚨 STUCK DEALS (>14 Dagen in Stage 2)

**URGENT**: Deze deals vereisen actie!

"""
        if data['stuck_deals']:
            for deal in data['stuck_deals']:
                dashboard += f"""- **{deal['title']}** (€{deal['value']:,})
  - Stuck: {deal['days']} dagen | Stage: {deal['stage']}
  - **Actie nodig**: Follow-up, blocker identificeren, rescue plan

"""
        else:
            dashboard += "✅ Geen stuck deals! Pipeline loopt goed.\n\n"

        # Urgent actions
        dashboard += """---

## 🎯 URGENT ACTIONS DEZE WEEK

"""
        for action in data['urgent_actions']:
            dashboard += f"- {action}\n"

        # Weekly priorities
        dashboard += """
---

## 📋 WEEKLY PRIORITIES

### 🔴 HIGH PRIORITY (Deze Week MOET)

"""
        # Generate priorities from data
        priorities_high = []

        if data['pipeline']['stage_2_stuck'] > 5:
            priorities_high.append(f"1. **Stage 2 Bottleneck Sprint**: Focus op {data['pipeline']['stage_2_stuck']} stuck deals")
            priorities_high.append("   - Run pipeline-optimizer skill voor prioritization")
            priorities_high.append("   - Target: Move 5 deals to Stage 3 deze week")

        if data['weekly']['deals_won'] < Config.WEEKLY_TARGETS['deals_closed']:
            gap = Config.WEEKLY_TARGETS['deals_closed'] - data['weekly']['deals_won']
            priorities_high.append(f"2. **Close Deals**: {gap} more closings needed to hit weekly target")
            priorities_high.append("   - Focus op Stage 3 (negotiation) deals")

        if data['weekly']['deals_added'] < Config.WEEKLY_TARGETS['new_deals']:
            gap = Config.WEEKLY_TARGETS['new_deals'] - data['weekly']['deals_added']
            priorities_high.append(f"3. **Lead Generation**: {gap} more deals needed")
            priorities_high.append("   - Score JobDigger leads (lead-quality-scorer skill)")
            priorities_high.append("   - Outreach to A-tier leads")

        for p in priorities_high:
            dashboard += f"{p}\n"

        dashboard += """
### 🟡 MEDIUM PRIORITY

- Review all Stage 2 deals (not just stuck ones)
- Follow-up on proposals sent last week
- Schedule client check-ins (Tier 1 clients)
- Prep for next week's interviews

### 🟢 LOW PRIORITY (If Time)

- Update CRM data quality
- Process new JobDigger batch
- Content creation (already scheduled Friday)

---

## 📞 KEY ACTIONS BY DAY

"""
        # Daily action plan
        days = ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag']

        dashboard += """**Maandag**:
- [ ] Pipeline review (Stage 2 focus)
- [ ] Metrics update (content + deals)
- [ ] Top 3 stuck deals: Action plan

**Dinsdag**:
- [ ] Outreach nieuwe leads (A-tier)
- [ ] Follow-up proposals (pending decisions)
- [ ] Client check-ins (2-3 calls)

**Woensdag**:
- [ ] Stage 2 deals: Move 3 to Stage 3
- [ ] Prep interviews deze week
- [ ] Candidate engagement updates

**Donderdag**:
- [ ] Close deals in Stage 3 (negotiations)
- [ ] Pipeline cleanup (update statuses)
- [ ] Plan volgende week

**Vrijdag**:
- [ ] Week review (metrics + learnings)
- [ ] Content creation (17:00-18:00)
- [ ] Weekend prep (urgent only)

---

## 📊 METRICS DETAILS

**Pipeline Breakdown by Stage** (Top 5 Stages):
"""
        # Would need actual stage data - simplified for now
        dashboard += """
- Stage 1 (Prospecting): X deals (€X)
- Stage 2 (Proposal): {stage_2_count} deals (€{stage_2_value:,})
- Stage 3 (Negotiation): X deals (€X)
- Stage 4 (Closed Won): X deals (€X)

**Conversion Rates** (This Week):
- Stage 1→2: X%
- Stage 2→3: X% (Target: >45%)
- Stage 3→4: X% (Target: >50%)

**Velocity**:
- Avg days Stage 1: X
- Avg days Stage 2: X (Target: <21)
- Avg days Stage 3: X
- Total sales cycle: X days

---

## 🎯 CLAUDE CODE COMMANDS (Voor Deze Week)

### Pipeline Analysis
```
Analyseer Stage 2 bottleneck:

Deals: {total_deals}
Stuck >14d: {stage_2_stuck}
Total value: €{stage_2_value:,}

Geef: Top 5 ROI actions + specific next steps per deal
```

### Lead Scoring
```
Score nieuwe JobDigger batch:

[Paste leads CSV]

Output: A-tier only + drafted outreach emails
```

### Deal Rescue
```
Deal rescue: [Stuck deal titel]

Stuck: {days}d
Value: €{value}
Last contact: {date}

Generate: Recovery plan + email templates
```

---

## 📈 WEEK-OVER-WEEK COMPARISON

*Update deze sectie elke week met previous week data*

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| New Deals | {deals_added} | [Last] | [+/-X] |
| Revenue | €{revenue:,} | [Last] | [+/-X%] |
| Stuck Deals | {stage_2_stuck} | [Last] | [+/-X] |
| Activities | {total_activities} | [Last] | [+/-X] |

**Trend**: [Improving / Stable / Declining]

---

## 💡 INSIGHTS & LEARNINGS

*Auto-generated insights:*

""".format(
            stage_2_count=data['pipeline']['stage_2_count'],
            stage_2_value=data['pipeline']['stage_2_value'],
            stage_2_stuck=data['pipeline']['stage_2_stuck'],
            total_deals=data['pipeline']['total_deals'],
            deals_added=data['weekly']['deals_added'],
            revenue=data['weekly']['revenue'],
            total_activities=data['activities']['total']
        )

        # Generate insights
        insights = self._generate_insights(data)
        for insight in insights:
            dashboard += f"- {insight}\n"

        # Next week recommendations
        dashboard += """
---

## 🎯 RECOMMENDATIONS NEXT WEEK

"""
        recs = self._generate_recommendations(data)
        for i, rec in enumerate(recs, 1):
            dashboard += f"{i}. {rec}\n"

        # Footer
        dashboard += f"""
---

## 📊 RAW DATA

```json
{json.dumps(data, indent=2, default=str)}
```

---

*Dashboard generated by Recruitin Pipeline Intelligence v1.0*
*Data source: {'Demo Data - Set PIPEDRIVE_API_KEY for live data' if self.use_demo else 'Live Pipedrive Data'}*
*Next update: Volgende maandag 10:00*
"""

        return dashboard

    def _generate_insights(self, data: Dict) -> List[str]:
        """Generate actionable insights"""
        insights = []

        # Pipeline health
        if data['pipeline']['stage_2_stuck'] > 10:
            insights.append("🚨 Stage 2 bottleneck critical - {stuck} deals stuck >14d (€{value:,} at risk)".format(
                stuck=data['pipeline']['stage_2_stuck'],
                value=data['pipeline']['stage_2_value']
            ))

        # Weekly performance
        if data['weekly']['deals_won'] >= Config.WEEKLY_TARGETS['deals_closed']:
            insights.append(f"✅ Weekly close target hit: {data['weekly']['deals_won']}/{Config.WEEKLY_TARGETS['deals_closed']}")
        else:
            insights.append(f"📈 Close target missed: {data['weekly']['deals_won']}/{Config.WEEKLY_TARGETS['deals_closed']} - push harder Thursday/Friday")

        # Activity level
        if data['activities']['total'] < Config.WEEKLY_TARGETS['activities']:
            gap = Config.WEEKLY_TARGETS['activities'] - data['activities']['total']
            insights.append(f"📞 Activity below target: {gap} more activities needed")

        # Revenue
        if data['weekly']['revenue'] > 0:
            insights.append(f"💰 Revenue generated: €{data['weekly']['revenue']:,} (target: €{Config.WEEKLY_TARGETS['revenue_target']:,})")

        return insights

    def _generate_recommendations(self, data: Dict) -> List[str]:
        """Generate recommendations"""
        recs = []

        # Based on stuck deals
        if data['pipeline']['stage_2_stuck'] > 5:
            recs.append("Focus Week: Stage 2 bottleneck sprint - target: reduce stuck deals by 50%")
            recs.append("Use pipeline-optimizer skill daily voor prioritization")

        # Based on activity
        if data['activities']['calls'] < Config.WEEKLY_TARGETS['calls']:
            recs.append(f"Increase call activity: {Config.WEEKLY_TARGETS['calls'] - data['activities']['calls']} more calls needed")

        # Based on revenue
        if data['weekly']['revenue'] < Config.WEEKLY_TARGETS['revenue_target']:
            recs.append("Accelerate closings: Focus op Stage 3 deals (negotiation) voor snellere revenue")

        # General
        recs.append("Daily morning routine: Pipeline check + top 5 actions (15 min)")
        recs.append("Weekly: Use recruitment-kpi-dashboard skill voor detailed analysis")

        return recs


# ============================================================================
# NOTION UPLOADER
# ============================================================================

def upload_to_notion(dashboard_text: str, notion_key: str, page_id: str):
    """Upload dashboard to Notion page"""

    try:
        from notion_client import Client

        notion = Client(auth=notion_key)

        # Add as collapsible toggle block
        notion.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"text": {"content": f"📊 Pipedrive Dashboard - Week {datetime.now().isocalendar()[1]}"}}],
                        "color": "orange_background"
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": dashboard_text[:2000]}}]  # First 2000 chars
                    }
                }
            ]
        )

        print("✅ Dashboard uploaded to Notion!")
        print(f"📄 View: https://notion.so/{page_id.replace('-', '')}")

    except Exception as e:
        print(f"❌ Notion upload failed: {e}")
        print("💡 Tip: Copy dashboard text en paste manual in Notion")


# ============================================================================
# CLI
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate Pipedrive weekly dashboard")
    parser.add_argument("--week", type=int, default=0, help="Weeks ago (0=current)")
    parser.add_argument("--upload-notion", action="store_true", help="Upload to Notion")
    parser.add_argument("-o", "--output", help="Save to file")

    args = parser.parse_args()

    # Generate dashboard
    generator = WeeklyDashboard()
    dashboard = generator.generate_dashboard(weeks_ago=args.week)

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(dashboard)
        print(f"✅ Dashboard saved to: {args.output}")
    else:
        print(dashboard)

    # Upload to Notion
    if args.upload_notion:
        upload_to_notion(dashboard, Config.NOTION_API_KEY, Config.NOTION_HUB_ID)


if __name__ == "__main__":
    main()
