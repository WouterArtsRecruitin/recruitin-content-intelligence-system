#!/usr/bin/env python3
"""
Notion Content Manager for Recruitin B.V.
Handles LinkedIn newsletter content aggregation and draft management.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database IDs - UPDATED 2026-02-02
# NOTE: Make sure these databases are shared with the Notion integration!
NEWS_DATABASE_ID = "2e52252c-bb15-8101-b097-cce88691c0d0"  # 📰 Recruitment News Database
DRAFTS_DATABASE_ID = "2e52252c-bb15-81e9-8215-cee7c7812f6d"  # ✍️ Content Drafts & Publishing
CONTENT_HUB_ID = "27c2252c-bb15-815b-b21b-e75a8c70d8d7"  # 🚀 LinkedIn & Recruitment Intelligence Hub

# Notion API configuration
NOTION_VERSION = "2022-06-28"


class NotionContentManager:
    """Manages content flow between news sources and Notion databases."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Notion client."""
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("NOTION_API_KEY not found in environment variables")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        }
        self.base_url = "https://api.notion.com/v1"

    def test_connection(self) -> bool:
        """Test Notion API connection."""
        try:
            response = requests.get(
                f"{self.base_url}/users/me", headers=self.headers, timeout=10
            )
            response.raise_for_status()
            print("✅ Notion API connection successful")
            print(f"   Connected as: {response.json().get('name', 'Unknown')}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Notion API connection failed: {e}")
            return False

    def fetch_news(self, save: bool = False) -> List[Dict]:
        """
        Fetch latest news articles from Notion NEWS database.

        Args:
            save: If True, save results to JSON file

        Returns:
            List of news articles
        """
        print("📰 Fetching news from Notion NEWS database...")

        try:
            # Query the NEWS database
            response = requests.post(
                f"{self.base_url}/databases/{NEWS_DATABASE_ID}/query",
                headers=self.headers,
                json={
                    "sorts": [{"property": "Date", "direction": "descending"}],
                    "page_size": 50,
                },
                timeout=30,
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            # Parse news items
            news_items = []
            for item in results:
                props = item.get("properties", {})

                # Extract title
                title_prop = props.get("Name", {}) or props.get("Title", {})
                title = ""
                if title_prop.get("title"):
                    title = "".join([t.get("plain_text", "") for t in title_prop["title"]])

                # Extract URL
                url_prop = props.get("URL", {})
                url = url_prop.get("url", "")

                # Extract date
                date_prop = props.get("Date", {})
                date = date_prop.get("date", {}).get("start", "") if date_prop.get("date") else ""

                # Extract score if available
                score_prop = props.get("Score", {})
                score = score_prop.get("number", 0)

                news_items.append({
                    "id": item["id"],
                    "title": title,
                    "url": url,
                    "date": date,
                    "score": score,
                    "created_time": item.get("created_time", ""),
                })

            print(f"✅ Found {len(news_items)} news articles")

            # Save to file if requested
            if save and news_items:
                filename = f"news-{datetime.now().strftime('%Y-%m-%d')}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(news_items, f, indent=2, ensure_ascii=False)
                print(f"💾 Saved to {filename}")

            return news_items

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch news: {e}")
            return []

    def list_drafts(self) -> List[Dict]:
        """List all drafts from Notion DRAFTS database."""
        print("📝 Listing drafts from Notion DRAFTS database...")

        try:
            response = requests.post(
                f"{self.base_url}/databases/{DRAFTS_DATABASE_ID}/query",
                headers=self.headers,
                json={
                    "sorts": [{"property": "Created", "direction": "descending"}],
                    "page_size": 50,
                },
                timeout=30,
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            # Parse drafts
            drafts = []
            for item in results:
                props = item.get("properties", {})

                # Extract title
                title_prop = props.get("Name", {}) or props.get("Title", {})
                title = ""
                if title_prop.get("title"):
                    title = "".join([t.get("plain_text", "") for t in title_prop["title"]])

                # Extract style
                style_prop = props.get("Style", {})
                style = ""
                if style_prop.get("select"):
                    style = style_prop["select"].get("name", "")

                # Extract status
                status_prop = props.get("Status", {})
                status = ""
                if status_prop.get("select"):
                    status = status_prop["select"].get("name", "")

                # Extract date
                created_prop = props.get("Created", {})
                created = created_prop.get("created_time", "")

                drafts.append({
                    "id": item["id"],
                    "title": title,
                    "style": style,
                    "status": status,
                    "created": created,
                })

            print(f"✅ Found {len(drafts)} drafts\n")

            # Display drafts
            for i, draft in enumerate(drafts, 1):
                status_emoji = "✅" if draft["status"] == "Published" else "📝"
                print(f"{i}. {status_emoji} {draft['title']}")
                print(f"   Style: {draft['style']} | Status: {draft['status']}")
                print(f"   Created: {draft['created'][:10]}\n")

            return drafts

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to list drafts: {e}")
            return []

    def create_draft(
        self, title: str, content: str, style: str = "contrarian", url: Optional[str] = None
    ) -> bool:
        """
        Create a new draft in Notion DRAFTS database.

        Args:
            title: Post title
            content: Post content (max 1300 chars for LinkedIn)
            style: Post style (contrarian, data_story, how_to, behind_scenes)
            url: Optional source URL

        Returns:
            True if successful
        """
        print(f"📝 Creating draft: {title}")
        print(f"   Style: {style}")
        print(f"   Content length: {len(content)} chars")

        # Validate content length for LinkedIn
        if len(content) > 1300:
            print(f"⚠️  Warning: Content exceeds LinkedIn limit (1300 chars)")

        try:
            # Prepare page properties
            properties = {
                "Name": {"title": [{"text": {"content": title}}]},
                "Style": {"select": {"name": style}},
                "Status": {"select": {"name": "Draft"}},
                "Created": {"date": {"start": datetime.now().isoformat()}},
            }

            # Add URL if provided
            if url:
                properties["URL"] = {"url": url}

            # Create the page in DRAFTS database
            page_data = {
                "parent": {"database_id": DRAFTS_DATABASE_ID},
                "properties": properties,
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": content}}]
                        },
                    }
                ],
            }

            response = requests.post(
                f"{self.base_url}/pages", headers=self.headers, json=page_data, timeout=30
            )
            response.raise_for_status()
            result = response.json()

            print(f"✅ Draft created successfully")
            print(f"   ID: {result['id']}")
            print(f"   URL: {result['url']}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to create draft: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"   Response: {e.response.text}")
            return False

    def generate_template(self, title: str, style: str = "contrarian") -> str:
        """
        Generate a LinkedIn post template based on style.

        Args:
            title: Topic or news title
            style: Post style

        Returns:
            Template string
        """
        templates = {
            "contrarian": """[BOLD STATEMENT over {title}]

[Lege regel]

[3-5 regels met concrete data/voorbeelden uit eigen praktijk]

[Lege regel]

[Plot twist of nuance die discussie opent]

[Lege regel]

[Vraag die uitnodigt tot reactie]

#recruitment #technischepersoneel #hiring""",
            "data_story": """[Specifiek getal] over {title}

[Lege regel]

Dit is wat dit betekent voor recruitment in Oost-Nederland:

→ [Insight 1 met data]
→ [Insight 2 met voorbeeld]
→ [Insight 3 met actie]

[Lege regel]

[Conclusie + vraag aan lezer]

#recruitment #data #hiring""",
            "how_to": """[Herkenbaar probleem rond {title}]

[Lege regel]

Hier is de fix in 4 stappen:

1. [Concrete actie 1]
2. [Concrete actie 2]
3. [Concrete actie 3]
4. [Concrete actie 4]

[Lege regel]

Resultaat: [Specifiek cijfer of uitkomst]

Save deze post voor later.

#recruitment #tips #hiring""",
            "behind_scenes": """[Eerlijke bekentenis rond {title}]

[Lege regel]

Dit gebeurde:
[Context in 2-3 zinnen]

[Lege regel]

Wat ik leerde:
[Concrete les met voorbeeld]

[Lege regel]

Nu doe ik dit anders:
[Nieuwe aanpak]

Herken je dit?

#recruitment #learnings #hiring""",
        }

        template = templates.get(style, templates["contrarian"])
        return template.replace("{title}", title)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Notion Content Manager for Recruitin B.V."
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["test", "fetch_news", "list_drafts", "create_draft", "generate"],
        help="Action to perform",
    )
    parser.add_argument("--title", help="Title for draft or template generation")
    parser.add_argument("--content", help="Content for draft creation")
    parser.add_argument(
        "--style",
        default="contrarian",
        choices=["contrarian", "data_story", "how_to", "behind_scenes"],
        help="Post style",
    )
    parser.add_argument("--url", help="Source URL for draft")
    parser.add_argument("--save", action="store_true", help="Save results to file")

    args = parser.parse_args()

    # Initialize manager
    try:
        manager = NotionContentManager()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Set NOTION_API_KEY in .env file or environment")
        sys.exit(1)

    # Execute action
    if args.action == "test":
        success = manager.test_connection()
        sys.exit(0 if success else 1)

    elif args.action == "fetch_news":
        manager.fetch_news(save=args.save)

    elif args.action == "list_drafts":
        manager.list_drafts()

    elif args.action == "create_draft":
        if not args.title or not args.content:
            print("❌ --title and --content required for create_draft action")
            sys.exit(1)
        manager.create_draft(args.title, args.content, args.style, args.url)

    elif args.action == "generate":
        if not args.title:
            print("❌ --title required for generate action")
            sys.exit(1)
        template = manager.generate_template(args.title, args.style)
        print("\n" + "=" * 60)
        print(f"TEMPLATE: {args.style.upper()}")
        print("=" * 60)
        print(template)
        print("=" * 60)


if __name__ == "__main__":
    main()
