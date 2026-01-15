#!/usr/bin/env python3
"""
Content Sentiment Analyzer - HuggingFace Inference API
======================================================
Analyzes LinkedIn comments for sentiment and engagement quality.
Uses HuggingFace Inference API - no local models needed!

Usage:
    python analyze_content_sentiment.py --comments "comment1" "comment2" "comment3"
    python analyze_content_sentiment.py --file comments.txt
    python analyze_content_sentiment.py --test

Requirements:
    pip install requests python-dotenv

Environment:
    HF_TOKEN=your_huggingface_token (optional, for higher rate limits)

Author: Recruitin B.V.
Version: 1.1
"""

import os
import sys
import json
import argparse
import requests
from typing import List, Dict, Optional
from datetime import datetime

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Sentiment analyzer configuration"""
    
    # HuggingFace model for multilingual sentiment (works great for Dutch)
    SENTIMENT_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
    
    # Alternative Dutch-specific model (if needed)
    DUTCH_MODEL = "DTAI-KULeuven/robbert-v2-dutch-sentiment"
    
    # Notion database ID for updating posts
    PERFORMANCE_TRACKER_ID = "2e62252c-bb15-81ef-bf65-d474eb0353ce"
    
    # Quality indicators - Dutch keywords
    PERSONAL_STORY_KEYWORDS = [
        'ik', 'wij', 'bij ons', 'mijn ervaring', 'onze', 
        'we hebben', 'ik heb', 'bij mij', 'in mijn'
    ]
    
    DATA_REQUEST_KEYWORDS = [
        'cijfers', 'data', 'bron', 'onderzoek', 'statistieken',
        'percentage', 'hoeveel', 'welke bron', 'waar haal je'
    ]
    
    AGREEMENT_KEYWORDS = [
        'eens', 'precies', 'klopt', 'inderdaad', 'absoluut',
        'helemaal', 'exact', 'zo is het', 'mee eens'
    ]
    
    DISAGREEMENT_KEYWORDS = [
        'oneens', 'maar', 'echter', 'niet helemaal', 'twijfel',
        'vraag me af', 'ben het er niet mee eens', 'nuanceren'
    ]


# ============================================================================
# SENTIMENT ANALYZER
# ============================================================================

class ContentSentimentAnalyzer:
    """Analyzes LinkedIn comments for sentiment and engagement quality"""
    
    def __init__(self, hf_token: str = None):
        """Initialize the sentiment analyzer with HuggingFace API"""
        self.hf_token = hf_token or os.getenv("HF_TOKEN") or os.getenv("HR-CVMATCHING-TOKEN")
        self.api_url = "https://router.huggingface.co/hf-inference/models/nlptown/bert-base-multilingual-uncased-sentiment"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"} if self.hf_token else {}
        print("🤖 Using HuggingFace Inference API (no local models)")
        if self.hf_token:
            print("✅ HF Token configured")
        else:
            print("⚠️ No HF token - using free tier (rate limited)")
    
    def _query_api(self, text: str) -> Optional[List]:
        """Query the HuggingFace Inference API"""
        try:
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json={"inputs": text[:512]},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                # Model loading, retry once
                import time
                time.sleep(5)
                response = requests.post(
                    self.api_url, 
                    headers=self.headers, 
                    json={"inputs": text[:512]},
                    timeout=30
                )
                if response.status_code == 200:
                    return response.json()
            return None
        except Exception as e:
            print(f"⚠️ API error: {e}")
            return None
    
    def analyze_single_comment(self, comment: str) -> Dict:
        """
        Analyze a single comment for sentiment
        
        Args:
            comment: The comment text to analyze
            
        Returns:
            Dict with sentiment label, score, and quality indicators
        """
        result = {
            'text': comment[:100] + '...' if len(comment) > 100 else comment,
            'char_count': len(comment),
            'sentiment': 'neutral',
            'sentiment_score': 0.5,
            'is_meaningful': False,
            'has_question': False,
            'has_personal_story': False,
            'has_data_request': False,
            'shows_agreement': False,
            'shows_disagreement': False
        }
        
        # API-based sentiment analysis
        api_result = self._query_api(comment)
        if api_result and isinstance(api_result, list) and len(api_result) > 0:
            try:
                # API returns list of predictions sorted by score
                predictions = api_result[0] if isinstance(api_result[0], list) else api_result
                top_pred = max(predictions, key=lambda x: x['score'])
                label = top_pred['label']
                score = top_pred['score']
                
                # Map model output to sentiment categories
                # nlptown model outputs: 1-5 stars
                if '5' in label or '4' in label:
                    result['sentiment'] = 'positive'
                    result['sentiment_score'] = 0.7 + (score * 0.3)
                elif '3' in label:
                    result['sentiment'] = 'neutral'
                    result['sentiment_score'] = 0.5
                else:
                    result['sentiment'] = 'negative'
                    result['sentiment_score'] = 0.3 - (score * 0.3)
                    
            except Exception as e:
                print(f"⚠️ Parse error: {e}")
        
        # Quality indicators
        comment_lower = comment.lower()
        
        # Meaningful discussion (>50 chars and not just emoji)
        result['is_meaningful'] = len(comment) > 50 and any(c.isalpha() for c in comment)
        
        # Contains question
        result['has_question'] = '?' in comment
        
        # Personal story indicators
        result['has_personal_story'] = any(
            kw in comment_lower for kw in Config.PERSONAL_STORY_KEYWORDS
        )
        
        # Data request indicators
        result['has_data_request'] = any(
            kw in comment_lower for kw in Config.DATA_REQUEST_KEYWORDS
        )
        
        # Agreement/disagreement
        result['shows_agreement'] = any(
            kw in comment_lower for kw in Config.AGREEMENT_KEYWORDS
        )
        result['shows_disagreement'] = any(
            kw in comment_lower for kw in Config.DISAGREEMENT_KEYWORDS
        )
        
        return result
    
    def analyze_comments(self, comments: List[str]) -> Dict:
        """
        Analyze a list of LinkedIn comments
        
        Args:
            comments: List of comment texts
            
        Returns:
            Complete analysis with breakdown and scores
        """
        if not comments:
            return {
                'total_comments': 0,
                'error': 'No comments provided'
            }
        
        print(f"\n📊 Analyzing {len(comments)} comments...")
        
        results = {
            'total_comments': len(comments),
            'analyzed_at': datetime.now().isoformat(),
            'sentiment_breakdown': {
                'positive': 0,
                'neutral': 0,
                'negative': 0
            },
            'avg_sentiment_score': 0,
            'quality_indicators': {
                'meaningful_discussions': 0,
                'questions_asked': 0,
                'personal_stories': 0,
                'data_requests': 0,
                'agreements': 0,
                'disagreements': 0
            },
            'engagement_quality_score': 0,
            'individual_analyses': [],
            'recommendations': []
        }
        
        total_sentiment_score = 0
        
        for i, comment in enumerate(comments, 1):
            print(f"  Analyzing comment {i}/{len(comments)}...", end='\r')
            
            analysis = self.analyze_single_comment(comment)
            results['individual_analyses'].append(analysis)
            
            # Aggregate sentiment
            results['sentiment_breakdown'][analysis['sentiment']] += 1
            total_sentiment_score += analysis['sentiment_score']
            
            # Aggregate quality indicators
            if analysis['is_meaningful']:
                results['quality_indicators']['meaningful_discussions'] += 1
            if analysis['has_question']:
                results['quality_indicators']['questions_asked'] += 1
            if analysis['has_personal_story']:
                results['quality_indicators']['personal_stories'] += 1
            if analysis['has_data_request']:
                results['quality_indicators']['data_requests'] += 1
            if analysis['shows_agreement']:
                results['quality_indicators']['agreements'] += 1
            if analysis['shows_disagreement']:
                results['quality_indicators']['disagreements'] += 1
        
        print(f"  ✅ Analyzed {len(comments)} comments    ")
        
        # Calculate averages
        n = len(comments)
        results['avg_sentiment_score'] = round((total_sentiment_score / n) * 100, 1)
        
        # Calculate engagement quality score (0-100)
        quality_score = (
            (results['quality_indicators']['meaningful_discussions'] / n) * 40 +
            (results['quality_indicators']['questions_asked'] / n) * 25 +
            (results['quality_indicators']['personal_stories'] / n) * 20 +
            (results['quality_indicators']['data_requests'] / n) * 15
        )
        results['engagement_quality_score'] = round(min(quality_score * 100, 100), 1)
        
        # Determine engagement quality tier
        if results['engagement_quality_score'] >= 75:
            results['engagement_quality_tier'] = 'High'
        elif results['engagement_quality_score'] >= 40:
            results['engagement_quality_tier'] = 'Medium'
        else:
            results['engagement_quality_tier'] = 'Low'
        
        # Calculate controversy score (0-10)
        if results['quality_indicators']['agreements'] + results['quality_indicators']['disagreements'] > 0:
            controversy = (
                results['quality_indicators']['disagreements'] / 
                (results['quality_indicators']['agreements'] + results['quality_indicators']['disagreements'])
            ) * 10
        else:
            controversy = 0
        results['controversy_score'] = round(controversy, 1)
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recs = []
        
        n = results['total_comments']
        qi = results['quality_indicators']
        
        # Sentiment recommendations
        pos_ratio = results['sentiment_breakdown']['positive'] / max(n, 1)
        neg_ratio = results['sentiment_breakdown']['negative'] / max(n, 1)
        
        if pos_ratio > 0.7:
            recs.append("✅ Highly positive reception - this angle resonates well, replicate!")
        elif neg_ratio > 0.3:
            recs.append("⚠️ Significant negative sentiment - review content for controversial claims")
        
        # Quality recommendations
        if qi['meaningful_discussions'] / max(n, 1) < 0.3:
            recs.append("💡 Low meaningful engagement - try adding a more specific question in your CTA")
        
        if qi['questions_asked'] / max(n, 1) > 0.4:
            recs.append("✅ High question rate - your content sparks curiosity, great!")
        
        if qi['personal_stories'] / max(n, 1) > 0.3:
            recs.append("✅ People sharing personal experiences - strong relatability")
        
        if qi['data_requests'] / max(n, 1) > 0.2:
            recs.append("📊 Data requests indicate interest - consider follow-up post with deeper data")
        
        # Controversy check
        if results['controversy_score'] > 6:
            recs.append("🔥 High controversy - this is engagement gold, but monitor carefully")
        
        if not recs:
            recs.append("📈 Solid engagement - continue with similar content approach")
        
        return recs
    
    def determine_performance_tier(
        self, 
        engagement_rate: float, 
        comments: int, 
        sentiment_score: float,
        quality_score: float
    ) -> str:
        """
        Determine A/B/C/D performance tier
        
        Args:
            engagement_rate: LinkedIn engagement rate (%)
            comments: Number of comments
            sentiment_score: Sentiment score (0-100)
            quality_score: Engagement quality score (0-100)
            
        Returns:
            Tier letter (A/B/C/D)
        """
        # A-Tier: Top performers
        if engagement_rate > 5 and comments > 15 and sentiment_score > 70 and quality_score > 75:
            return 'A'
        
        # B-Tier: Above average
        if engagement_rate > 3 and comments > 8 and sentiment_score > 50:
            return 'B'
        
        # C-Tier: Average
        if engagement_rate > 2 and comments > 3:
            return 'C'
        
        # D-Tier: Below average
        return 'D'


# ============================================================================
# NOTION INTEGRATION
# ============================================================================

class NotionUpdater:
    """Updates Notion database with sentiment analysis results"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                from notion_client import Client
                self.client = Client(auth=self.api_key)
            except ImportError:
                print("⚠️ notion-client not installed. Notion updates disabled.")
    
    def update_post_sentiment(
        self, 
        page_id: str, 
        sentiment_score: float,
        engagement_quality: str,
        performance_tier: str,
        key_learnings: str
    ) -> bool:
        """Update a Notion page with sentiment analysis results"""
        if not self.client:
            print("⚠️ Notion client not available")
            return False
        
        try:
            # Note: This assumes the Notion page has these properties
            # You'll need to adjust property names to match your database
            self.client.pages.update(
                page_id=page_id,
                properties={
                    # These would need to match your actual Notion property names
                    # "Sentiment Score": {"number": sentiment_score},
                    # "Engagement Quality": {"select": {"name": engagement_quality}},
                    # "Performance Tier": {"select": {"name": performance_tier}},
                    # "Key Learnings": {"rich_text": [{"text": {"content": key_learnings}}]}
                }
            )
            print(f"✅ Updated Notion page: {page_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to update Notion: {e}")
            return False


# ============================================================================
# CLI INTERFACE
# ============================================================================

def print_analysis_report(results: Dict):
    """Pretty print the analysis results"""
    print("\n" + "="*60)
    print("📊 CONTENT SENTIMENT ANALYSIS REPORT")
    print("="*60)
    
    print(f"\n📝 Total Comments Analyzed: {results['total_comments']}")
    print(f"🕐 Analyzed at: {results['analyzed_at']}")
    
    # Sentiment breakdown
    print("\n📈 SENTIMENT BREAKDOWN")
    print("-"*40)
    sb = results['sentiment_breakdown']
    total = results['total_comments']
    print(f"  ✅ Positive: {sb['positive']} ({sb['positive']/total*100:.0f}%)")
    print(f"  ➖ Neutral:  {sb['neutral']} ({sb['neutral']/total*100:.0f}%)")
    print(f"  ❌ Negative: {sb['negative']} ({sb['negative']/total*100:.0f}%)")
    print(f"\n  Average Sentiment Score: {results['avg_sentiment_score']}/100")
    
    # Quality indicators
    print("\n🎯 QUALITY INDICATORS")
    print("-"*40)
    qi = results['quality_indicators']
    print(f"  💬 Meaningful discussions: {qi['meaningful_discussions']}")
    print(f"  ❓ Questions asked: {qi['questions_asked']}")
    print(f"  👤 Personal stories shared: {qi['personal_stories']}")
    print(f"  📊 Data requests: {qi['data_requests']}")
    print(f"  👍 Agreements: {qi['agreements']}")
    print(f"  👎 Disagreements: {qi['disagreements']}")
    
    # Scores
    print("\n📊 SCORES")
    print("-"*40)
    print(f"  Engagement Quality Score: {results['engagement_quality_score']}/100")
    print(f"  Engagement Quality Tier: {results['engagement_quality_tier']}")
    print(f"  Controversy Score: {results['controversy_score']}/10")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-"*40)
    for rec in results['recommendations']:
        print(f"  {rec}")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze LinkedIn comments for sentiment and engagement quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_content_sentiment.py --test
  python analyze_content_sentiment.py --comments "Great post!" "Interesting perspective"
  python analyze_content_sentiment.py --file comments.txt
  python analyze_content_sentiment.py --comments "..." --json
        """
    )
    
    parser.add_argument(
        "--comments",
        nargs="+",
        help="List of comments to analyze"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="File with comments (one per line)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run with test comments"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="HuggingFace API token"
    )
    
    args = parser.parse_args()
    
    # Collect comments
    comments = []
    
    if args.test:
        comments = [
            "Helemaal mee eens! Ik zie dit ook bij onze klanten in de techniek.",
            "Interessant perspectief. Heb je cijfers hierover?",
            "Culture fit is inderdaad een vaag begrip. Wij gebruiken nu een competentie matrix.",
            "👍",
            "Waar haal je deze data vandaan? Graag de bron!",
            "Ben het er niet helemaal mee eens. In mijn ervaring...",
            "Top post! Ga ik zeker delen met mijn team.",
            "Dit is precies wat ik bedoel als ik zeg dat recruitment moet veranderen.",
            "?",
            "Mooi geschreven, maar hoe zit het met de kosten?"
        ]
        print("🧪 Running with test comments...")
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                comments = [line.strip() for line in f if line.strip()]
            print(f"📄 Loaded {len(comments)} comments from {args.file}")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
    elif args.comments:
        comments = args.comments
    else:
        print("❌ No comments provided. Use --comments, --file, or --test")
        parser.print_help()
        sys.exit(1)
    
    # Analyze
    analyzer = ContentSentimentAnalyzer(hf_token=args.token)
    results = analyzer.analyze_comments(comments)
    
    # Output
    if args.json:
        # Remove individual analyses for cleaner JSON output
        output = {k: v for k, v in results.items() if k != 'individual_analyses'}
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print_analysis_report(results)
    
    # Determine tier example
    print("\n📊 PERFORMANCE TIER CALCULATION")
    print("-"*40)
    tier = analyzer.determine_performance_tier(
        engagement_rate=4.5,  # Example: 4.5%
        comments=len(comments),
        sentiment_score=results['avg_sentiment_score'],
        quality_score=results['engagement_quality_score']
    )
    print(f"  With 4.5% engagement rate and {len(comments)} comments:")
    print(f"  → Performance Tier: {tier}")
    
    # Tier explanation
    tier_desc = {
        'A': "🏆 Top 20% - Replicate this content!",
        'B': "✅ Above average - Good performance",
        'C': "➖ Average - Room for improvement",
        'D': "⚠️ Below average - Analyze what went wrong"
    }
    print(f"  → {tier_desc[tier]}")


if __name__ == "__main__":
    main()
