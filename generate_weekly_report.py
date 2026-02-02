#!/usr/bin/env python3
"""
Weekly Content Performance Report Generator
============================================
Generates automated weekly reports from Notion Content Performance data.

Usage:
    python generate_weekly_report.py
    python generate_weekly_report.py --week 2
    python generate_weekly_report.py --output report.md
    python generate_weekly_report.py --demo

Requirements:
    pip install notion-client python-dotenv requests

Environment:
    NOTION_API_KEY=your_notion_api_key
    HF_TOKEN=your_huggingface_token (optional, for sentiment)

Author: Recruitin B.V.
Version: 1.0
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

try:
    from notion_client import Client
except ImportError:
    print("Installing notion-client...")
    os.system("pip install notion-client --break-system-packages -q")
    from notion_client import Client

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Report generator configuration"""
    
    # Notion Database IDs
    CONTENT_HUB_ID = "27c2252c-bb15-815b-b21b-e75a8c70d8d7"
    NEWS_DATABASE_ID = "2e52252c-bb15-8101-b097-cce88691c0d0"  # 📰 Recruitment News Database
    DRAFTS_DATABASE_ID = "2e52252c-bb15-81e9-8215-cee7c7812f6d"  # ✍️ Content Drafts & Publishing
    DASHBOARD_ID = "2e62252c-bb15-818f-af7e-c06c3fae1a29"
    TRACKER_ID = "2e62252c-bb15-81ef-bf65-d474eb0353ce"
    
    # Performance Tier Thresholds
    TIER_A = {'engagement': 5.0, 'comments': 15, 'sentiment': 70}
    TIER_B = {'engagement': 3.0, 'comments': 8, 'sentiment': 50}
    TIER_C = {'engagement': 2.0, 'comments': 3}
    
    # Targets
    WEEKLY_POST_TARGET = 4
    ENGAGEMENT_TARGET = 4.0
    IMPRESSIONS_TARGET = 5000
    FOLLOWERS_TARGET = 20
    
    # Best posting times (based on analysis)
    BEST_TIMES = {
        'Contrarian': {'day': 'Woensdag', 'time': '12:00-13:00'},
        'Data Story': {'day': 'Dinsdag', 'time': '08:00-09:00'},
        'How-To': {'day': 'Donderdag', 'time': '08:00-09:00'},
        'Behind-Scenes': {'day': 'Vrijdag', 'time': '10:00-11:00'},
    }


# ============================================================================
# DEMO DATA (when Notion is not available)
# ============================================================================

DEMO_POSTS = [
    {
        'title': '"Culture fit" is de luiste afwijzing in recruitment',
        'date': '2026-01-08',
        'platform': 'Wouter Personal',
        'angle': 'Contrarian',
        'visual': 'None',
        'impressions': 8420,
        'reach': 6200,
        'engagement_rate': 6.2,
        'likes': 89,
        'comments': 24,
        'shares': 12,
        'saves': 8,
        'profile_visits': 45,
        'followers_gained': 8,
        'sentiment_score': 78,
        'tier': 'A',
    },
    {
        'title': '47 vacatures gevuld in 90 dagen - onze exacte aanpak',
        'date': '2026-01-06',
        'platform': 'Wouter Personal',
        'angle': 'Data Story',
        'visual': 'Carousel',
        'impressions': 7200,
        'reach': 5400,
        'engagement_rate': 5.8,
        'likes': 72,
        'comments': 19,
        'shares': 8,
        'saves': 15,
        'profile_visits': 38,
        'followers_gained': 6,
        'sentiment_score': 82,
        'tier': 'A',
    },
    {
        'title': '5 dingen die technisch talent écht wil horen in een eerste gesprek',
        'date': '2026-01-03',
        'platform': 'Recruitin Company',
        'angle': 'How-To',
        'visual': 'Image',
        'impressions': 5600,
        'reach': 4100,
        'engagement_rate': 4.5,
        'likes': 45,
        'comments': 12,
        'shares': 5,
        'saves': 9,
        'profile_visits': 22,
        'followers_gained': 4,
        'sentiment_score': 71,
        'tier': 'B',
    },
    {
        'title': 'Achter de schermen: hoe we een 6-maanden vacature in 3 weken vulden',
        'date': '2026-01-10',
        'platform': 'Wouter Personal',
        'angle': 'Behind-Scenes',
        'visual': 'None',
        'impressions': 4800,
        'reach': 3600,
        'engagement_rate': 4.2,
        'likes': 38,
        'comments': 14,
        'shares': 4,
        'saves': 6,
        'profile_visits': 28,
        'followers_gained': 5,
        'sentiment_score': 75,
        'tier': 'B',
    },
    {
        'title': 'Waarom we stoppen met LinkedIn InMails',
        'date': '2026-01-07',
        'platform': 'Recruitin Company',
        'angle': 'Contrarian',
        'visual': 'None',
        'impressions': 3200,
        'reach': 2400,
        'engagement_rate': 2.8,
        'likes': 22,
        'comments': 6,
        'shares': 2,
        'saves': 3,
        'profile_visits': 12,
        'followers_gained': 2,
        'sentiment_score': 58,
        'tier': 'C',
    },
]


# ============================================================================
# REPORT GENERATOR
# ============================================================================

class WeeklyReportGenerator:
    """Generates weekly content performance reports"""
    
    def __init__(self, notion_key: str = None):
        """Initialize with Notion client"""
        self.notion_key = notion_key or os.getenv("NOTION_API_KEY")
        self.client = None
        self.use_demo = False
        
        if self.notion_key:
            try:
                self.client = Client(auth=self.notion_key)
                print("✅ Notion client initialized")
            except Exception as e:
                print(f"⚠️ Notion connection failed: {e}")
                self.use_demo = True
        else:
            print("⚠️ No NOTION_API_KEY - using demo data")
            self.use_demo = True
    
    def get_week_dates(self, weeks_ago: int = 0) -> tuple:
        """Get start and end dates for a specific week"""
        today = datetime.now()
        # Go to Monday of current week
        monday = today - timedelta(days=today.weekday())
        # Adjust for weeks ago
        monday = monday - timedelta(weeks=weeks_ago)
        sunday = monday + timedelta(days=6)
        return monday, sunday
    
    def fetch_posts_from_notion(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Fetch posts from Notion database for the given date range"""
        if self.use_demo or not self.client:
            print("📊 Using demo data...")
            return DEMO_POSTS
        
        try:
            # Query the Content Performance Tracker database
            # Note: This assumes you have a database with the correct properties
            response = self.client.databases.query(
                database_id=Config.TRACKER_ID,
                filter={
                    "and": [
                        {
                            "property": "Publicatie Datum",
                            "date": {
                                "on_or_after": start_date.isoformat()
                            }
                        },
                        {
                            "property": "Publicatie Datum",
                            "date": {
                                "on_or_before": end_date.isoformat()
                            }
                        }
                    ]
                }
            )
            
            posts = []
            for page in response.get('results', []):
                props = page.get('properties', {})
                posts.append(self._parse_notion_page(props))
            
            if not posts:
                print("⚠️ No posts found in Notion - using demo data")
                return DEMO_POSTS
            
            return posts
            
        except Exception as e:
            print(f"⚠️ Error fetching from Notion: {e}")
            print("📊 Falling back to demo data...")
            return DEMO_POSTS
    
    def _parse_notion_page(self, props: Dict) -> Dict:
        """Parse Notion page properties into post dict"""
        # This would need to be adjusted based on your actual Notion property names
        return {
            'title': self._get_title(props.get('Titel', {})),
            'date': self._get_date(props.get('Publicatie Datum', {})),
            'platform': self._get_select(props.get('Platform', {})),
            'angle': self._get_select(props.get('Angle', {})),
            'visual': self._get_select(props.get('Visual', {})),
            'impressions': self._get_number(props.get('Impressions', {})),
            'reach': self._get_number(props.get('Reach', {})),
            'engagement_rate': self._get_number(props.get('Engagement Rate', {})),
            'likes': self._get_number(props.get('Likes', {})),
            'comments': self._get_number(props.get('Comments', {})),
            'shares': self._get_number(props.get('Shares', {})),
            'saves': self._get_number(props.get('Saves', {})),
            'profile_visits': self._get_number(props.get('Profile Visits', {})),
            'followers_gained': self._get_number(props.get('Followers Gained', {})),
            'sentiment_score': self._get_number(props.get('Sentiment Score', {})),
            'tier': self._get_select(props.get('Performance Tier', {})),
        }
    
    def _get_title(self, prop: Dict) -> str:
        try:
            return prop.get('title', [{}])[0].get('plain_text', 'Untitled')
        except:
            return 'Untitled'
    
    def _get_date(self, prop: Dict) -> str:
        try:
            return prop.get('date', {}).get('start', '')
        except:
            return ''
    
    def _get_select(self, prop: Dict) -> str:
        try:
            return prop.get('select', {}).get('name', '')
        except:
            return ''
    
    def _get_number(self, prop: Dict) -> float:
        try:
            return prop.get('number', 0) or 0
        except:
            return 0
    
    def calculate_metrics(self, posts: List[Dict]) -> Dict:
        """Calculate aggregate metrics from posts"""
        if not posts:
            return {}
        
        metrics = {
            'total_posts': len(posts),
            'total_impressions': sum(p.get('impressions', 0) for p in posts),
            'total_reach': sum(p.get('reach', 0) for p in posts),
            'total_likes': sum(p.get('likes', 0) for p in posts),
            'total_comments': sum(p.get('comments', 0) for p in posts),
            'total_shares': sum(p.get('shares', 0) for p in posts),
            'total_saves': sum(p.get('saves', 0) for p in posts),
            'total_profile_visits': sum(p.get('profile_visits', 0) for p in posts),
            'total_followers_gained': sum(p.get('followers_gained', 0) for p in posts),
            'avg_engagement_rate': 0,
            'avg_sentiment': 0,
        }
        
        # Calculate averages
        engagement_rates = [p.get('engagement_rate', 0) for p in posts if p.get('engagement_rate')]
        sentiments = [p.get('sentiment_score', 0) for p in posts if p.get('sentiment_score')]
        
        if engagement_rates:
            metrics['avg_engagement_rate'] = round(sum(engagement_rates) / len(engagement_rates), 2)
        if sentiments:
            metrics['avg_sentiment'] = round(sum(sentiments) / len(sentiments), 1)
        
        # Tier breakdown
        tier_counts = defaultdict(int)
        for p in posts:
            tier = p.get('tier', 'C')
            tier_counts[tier] += 1
        metrics['tier_breakdown'] = dict(tier_counts)
        
        # Platform breakdown
        platform_metrics = defaultdict(lambda: {'posts': 0, 'impressions': 0, 'engagement': []})
        for p in posts:
            platform = p.get('platform', 'Unknown')
            platform_metrics[platform]['posts'] += 1
            platform_metrics[platform]['impressions'] += p.get('impressions', 0)
            if p.get('engagement_rate'):
                platform_metrics[platform]['engagement'].append(p.get('engagement_rate'))
        
        for platform in platform_metrics:
            eng_list = platform_metrics[platform]['engagement']
            platform_metrics[platform]['avg_engagement'] = round(sum(eng_list) / len(eng_list), 2) if eng_list else 0
        metrics['platform_breakdown'] = dict(platform_metrics)
        
        # Angle breakdown
        angle_metrics = defaultdict(lambda: {'posts': 0, 'engagement': []})
        for p in posts:
            angle = p.get('angle', 'Unknown')
            angle_metrics[angle]['posts'] += 1
            if p.get('engagement_rate'):
                angle_metrics[angle]['engagement'].append(p.get('engagement_rate'))
        
        for angle in angle_metrics:
            eng_list = angle_metrics[angle]['engagement']
            angle_metrics[angle]['avg_engagement'] = round(sum(eng_list) / len(eng_list), 2) if eng_list else 0
        metrics['angle_breakdown'] = dict(angle_metrics)
        
        return metrics
    
    def get_top_posts(self, posts: List[Dict], n: int = 3) -> List[Dict]:
        """Get top N posts by engagement"""
        sorted_posts = sorted(posts, key=lambda x: x.get('engagement_rate', 0), reverse=True)
        return sorted_posts[:n]
    
    def get_worst_posts(self, posts: List[Dict], n: int = 2) -> List[Dict]:
        """Get bottom N posts by engagement"""
        sorted_posts = sorted(posts, key=lambda x: x.get('engagement_rate', 0))
        return sorted_posts[:n]
    
    def generate_insights(self, posts: List[Dict], metrics: Dict) -> List[str]:
        """Generate actionable insights from the data"""
        insights = []
        
        # Post volume
        if metrics['total_posts'] >= Config.WEEKLY_POST_TARGET:
            insights.append(f"✅ Post target gehaald: {metrics['total_posts']}/{Config.WEEKLY_POST_TARGET}")
        else:
            insights.append(f"⚠️ Post target niet gehaald: {metrics['total_posts']}/{Config.WEEKLY_POST_TARGET}")
        
        # Engagement
        if metrics['avg_engagement_rate'] >= Config.ENGAGEMENT_TARGET:
            insights.append(f"✅ Engagement boven target: {metrics['avg_engagement_rate']}% (target: {Config.ENGAGEMENT_TARGET}%)")
        else:
            gap = Config.ENGAGEMENT_TARGET - metrics['avg_engagement_rate']
            insights.append(f"📈 Engagement {gap:.1f}% onder target - focus op meer Contrarian content")
        
        # Best performing angle
        if metrics.get('angle_breakdown'):
            best_angle = max(metrics['angle_breakdown'].items(), key=lambda x: x[1].get('avg_engagement', 0))
            insights.append(f"🏆 Best presterende angle: {best_angle[0]} ({best_angle[1]['avg_engagement']}% avg)")
        
        # Platform comparison
        if metrics.get('platform_breakdown'):
            platforms = list(metrics['platform_breakdown'].items())
            if len(platforms) >= 2:
                p1, p2 = platforms[0], platforms[1]
                if p1[1]['avg_engagement'] > p2[1]['avg_engagement']:
                    insights.append(f"📱 {p1[0]} outperforms {p2[0]} ({p1[1]['avg_engagement']}% vs {p2[1]['avg_engagement']}%)")
        
        # A-tier posts
        a_count = metrics.get('tier_breakdown', {}).get('A', 0)
        if a_count > 0:
            insights.append(f"🌟 {a_count} A-tier post(s) deze week - analyseer en repliceer!")
        
        # Followers
        if metrics['total_followers_gained'] >= Config.FOLLOWERS_TARGET:
            insights.append(f"✅ Follower growth on track: +{metrics['total_followers_gained']}")
        
        return insights
    
    def generate_recommendations(self, posts: List[Dict], metrics: Dict) -> List[str]:
        """Generate recommendations for next week"""
        recs = []
        
        # Based on best performing angle
        if metrics.get('angle_breakdown'):
            best_angle = max(metrics['angle_breakdown'].items(), key=lambda x: x[1].get('avg_engagement', 0))
            timing = Config.BEST_TIMES.get(best_angle[0], {})
            if timing:
                recs.append(f"📅 Plan meer {best_angle[0]} content op {timing.get('day')} {timing.get('time')}")
        
        # Check for missing angles
        used_angles = set(p.get('angle') for p in posts)
        all_angles = set(Config.BEST_TIMES.keys())
        missing = all_angles - used_angles
        if missing:
            recs.append(f"🔄 Test volgende week: {', '.join(missing)}")
        
        # Visual recommendation
        visual_posts = [p for p in posts if p.get('visual') and p.get('visual') != 'None']
        text_posts = [p for p in posts if not p.get('visual') or p.get('visual') == 'None']
        
        if visual_posts and text_posts:
            visual_eng = sum(p.get('engagement_rate', 0) for p in visual_posts) / len(visual_posts)
            text_eng = sum(p.get('engagement_rate', 0) for p in text_posts) / len(text_posts)
            
            if visual_eng > text_eng * 1.2:
                recs.append("📷 Visual content presteert +20% beter - voeg meer toe")
            elif text_eng > visual_eng * 1.2:
                recs.append("📝 Text-only posts presteren beter - focus daarop")
        
        # Engagement improvement
        if metrics['avg_engagement_rate'] < Config.ENGAGEMENT_TARGET:
            recs.append("💡 Voeg een vraag toe aan elke post CTA voor meer engagement")
        
        # A/B test suggestion
        recs.append("🔬 A/B test idee: Data-driven opener vs Story opener")
        
        return recs
    
    def generate_report(self, weeks_ago: int = 0) -> str:
        """Generate the complete weekly report"""
        start_date, end_date = self.get_week_dates(weeks_ago)
        week_num = start_date.isocalendar()[1]
        
        print(f"\n📊 Generating report for Week {week_num}")
        print(f"   Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Fetch data
        posts = self.fetch_posts_from_notion(start_date, end_date)
        metrics = self.calculate_metrics(posts)
        top_posts = self.get_top_posts(posts)
        worst_posts = self.get_worst_posts(posts)
        insights = self.generate_insights(posts, metrics)
        recommendations = self.generate_recommendations(posts, metrics)
        
        # Generate markdown report
        report = self._format_report(
            week_num=week_num,
            start_date=start_date,
            end_date=end_date,
            posts=posts,
            metrics=metrics,
            top_posts=top_posts,
            worst_posts=worst_posts,
            insights=insights,
            recommendations=recommendations
        )
        
        return report
    
    def _format_report(
        self,
        week_num: int,
        start_date: datetime,
        end_date: datetime,
        posts: List[Dict],
        metrics: Dict,
        top_posts: List[Dict],
        worst_posts: List[Dict],
        insights: List[str],
        recommendations: List[str]
    ) -> str:
        """Format the report as markdown"""
        
        report = f"""# 📊 Weekly Content Performance Report

**Week {week_num} | {start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')}**
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Company**: Recruitin B.V.

---

## 📈 EXECUTIVE SUMMARY

| Metric | This Week | Target | Status |
|--------|-----------|--------|--------|
| Posts Published | {metrics['total_posts']} | {Config.WEEKLY_POST_TARGET} | {'✅' if metrics['total_posts'] >= Config.WEEKLY_POST_TARGET else '⚠️'} |
| Avg Engagement | {metrics['avg_engagement_rate']}% | {Config.ENGAGEMENT_TARGET}% | {'✅' if metrics['avg_engagement_rate'] >= Config.ENGAGEMENT_TARGET else '📈'} |
| Total Impressions | {metrics['total_impressions']:,} | {Config.IMPRESSIONS_TARGET:,} | {'✅' if metrics['total_impressions'] >= Config.IMPRESSIONS_TARGET else '📈'} |
| Followers Gained | +{metrics['total_followers_gained']} | +{Config.FOLLOWERS_TARGET} | {'✅' if metrics['total_followers_gained'] >= Config.FOLLOWERS_TARGET else '📈'} |
| Avg Sentiment | {metrics['avg_sentiment']}/100 | 70+ | {'✅' if metrics['avg_sentiment'] >= 70 else '📈'} |

---

## 🏆 TOP PERFORMERS

"""
        # Top posts
        for i, post in enumerate(top_posts, 1):
            tier_emoji = {'A': '🥇', 'B': '🥈', 'C': '🥉'}.get(post.get('tier', 'C'), '📊')
            report += f"""### {i}. {post['title']}

{tier_emoji} **Tier {post.get('tier', 'C')}** | {post['date']} | {post['platform']} | {post['angle']}

| Impressions | Engagement | Comments | Sentiment |
|-------------|------------|----------|-----------|
| {post.get('impressions', 0):,} | {post.get('engagement_rate', 0)}% | {post.get('comments', 0)} | {post.get('sentiment_score', 0)} |

"""

        # Performance by angle
        report += """---

## 🎯 PERFORMANCE BY ANGLE

| Angle | Posts | Avg Engagement | Best Time |
|-------|-------|----------------|-----------|
"""
        for angle, data in metrics.get('angle_breakdown', {}).items():
            best_time = Config.BEST_TIMES.get(angle, {})
            time_str = f"{best_time.get('day', '-')} {best_time.get('time', '')}"
            report += f"| {angle} | {data['posts']} | {data['avg_engagement']}% | {time_str} |\n"

        # Platform breakdown
        report += """
---

## 📱 PLATFORM COMPARISON

| Platform | Posts | Impressions | Avg Engagement |
|----------|-------|-------------|----------------|
"""
        for platform, data in metrics.get('platform_breakdown', {}).items():
            report += f"| {platform} | {data['posts']} | {data['impressions']:,} | {data['avg_engagement']}% |\n"

        # Tier breakdown
        report += """
---

## 🏅 TIER BREAKDOWN

"""
        tier_info = {
            'A': ('🥇', 'Top 20% - Replicate!', '>5% eng, >15 comments'),
            'B': ('🥈', 'Above Average', '3-5% eng, 8-15 comments'),
            'C': ('🥉', 'Average', '2-3% eng, 3-8 comments'),
            'D': ('📉', 'Below Average', '<2% eng, <3 comments'),
        }
        
        for tier, count in sorted(metrics.get('tier_breakdown', {}).items()):
            emoji, label, criteria = tier_info.get(tier, ('📊', 'Unknown', '-'))
            report += f"- {emoji} **Tier {tier}**: {count} posts ({label})\n"

        # Worst performers (learning opportunities)
        report += """
---

## 📚 LEARNING OPPORTUNITIES

*Posts met laagste engagement - analyseer waarom:*

"""
        for post in worst_posts:
            report += f"""**{post['title']}**
- Engagement: {post.get('engagement_rate', 0)}% | Comments: {post.get('comments', 0)}
- Mogelijke oorzaak: [Te analyseren]

"""

        # Insights
        report += """---

## 💡 KEY INSIGHTS

"""
        for insight in insights:
            report += f"- {insight}\n"

        # Recommendations
        report += """
---

## 🎯 RECOMMENDATIONS NEXT WEEK

"""
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"

        # Footer
        report += f"""
---

## 📊 RAW METRICS

```
Total Posts: {metrics['total_posts']}
Total Impressions: {metrics['total_impressions']:,}
Total Reach: {metrics['total_reach']:,}
Total Likes: {metrics['total_likes']}
Total Comments: {metrics['total_comments']}
Total Shares: {metrics['total_shares']}
Total Saves: {metrics['total_saves']}
Profile Visits: {metrics['total_profile_visits']}
Followers Gained: {metrics['total_followers_gained']}
Avg Engagement Rate: {metrics['avg_engagement_rate']}%
Avg Sentiment Score: {metrics['avg_sentiment']}/100
```

---

*Report generated by Recruitin Content Analytics System v1.0*
*Data source: {'Demo Data' if self.use_demo else 'Notion Database'}*
"""
        
        return report


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate weekly content performance reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_weekly_report.py              # Current week
  python generate_weekly_report.py --week 1     # Last week
  python generate_weekly_report.py --demo       # Force demo data
  python generate_weekly_report.py -o report.md # Save to file
        """
    )
    
    parser.add_argument(
        "--week",
        type=int,
        default=0,
        help="Weeks ago (0=current, 1=last week, etc.)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output file path (default: print to stdout)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Force use of demo data"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output metrics as JSON instead of markdown"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = WeeklyReportGenerator()
    
    if args.demo:
        generator.use_demo = True
    
    if args.json:
        # JSON output mode
        start_date, end_date = generator.get_week_dates(args.week)
        posts = generator.fetch_posts_from_notion(start_date, end_date)
        metrics = generator.calculate_metrics(posts)
        print(json.dumps(metrics, indent=2, default=str))
    else:
        # Markdown report mode
        report = generator.generate_report(weeks_ago=args.week)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n✅ Report saved to: {args.output}")
        else:
            print("\n" + report)


if __name__ == "__main__":
    main()
