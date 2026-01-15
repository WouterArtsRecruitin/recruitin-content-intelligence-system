# Notion Content Manager

Automated LinkedIn newsletter content aggregation and draft management system for Recruitin B.V.

## Overview

This Python-based automation connects to Notion databases to:
- Fetch daily recruitment news articles from the NEWS database
- Manage LinkedIn content drafts in the DRAFTS database
- Generate LinkedIn post templates in multiple styles
- Create and organize content for the Oost-Nederland recruitment market

## Prerequisites

- Python 3.8+
- Notion API key with access to your workspace
- Access to the configured Notion databases

## Installation

1. Install required dependencies:
```bash
pip install requests python-dotenv
```

2. Configure your Notion API key:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Notion API key
# Get your API key from: https://www.notion.so/my-integrations
```

3. Verify the connection:
```bash
python notion_content_manager.py --action test
```

## Notion Database Configuration

### NEWS Database
**ID:** `2e62252c-bb15-8126-97a9-eb7166e6b3b8`

Properties:
- **Name/Title** (Title): Article headline
- **URL** (URL): Source link
- **Date** (Date): Publication date
- **Score** (Number): Content relevance score

### DRAFTS Database
**ID:** `50bc3e75-94d7-4b5b-a12a-96762ef29784`

Properties:
- **Name/Title** (Title): Post title
- **Style** (Select): contrarian | data_story | how_to | behind_scenes
- **Status** (Select): Draft | Published
- **Created** (Date): Creation timestamp
- **URL** (URL): Optional source reference

## Available Commands

### Test Connection
Verify Notion API connectivity and authentication:
```bash
python notion_content_manager.py --action test
```

### Fetch News
Retrieve latest articles from NEWS database:
```bash
# Fetch and display
python notion_content_manager.py --action fetch_news

# Fetch and save to JSON file
python notion_content_manager.py --action fetch_news --save
```

Outputs: `news-YYYY-MM-DD.json` with article data sorted by date.

### List Drafts
Display all drafts from DRAFTS database:
```bash
python notion_content_manager.py --action list_drafts
```

Shows: Title, style, status, and creation date for each draft.

### Generate Template
Create a LinkedIn post template based on news title:
```bash
python notion_content_manager.py \
  --action generate \
  --title "NIEUWS_TITEL" \
  --style contrarian
```

Available styles: `contrarian`, `data_story`, `how_to`, `behind_scenes`

### Create Draft
Add a new draft to Notion DRAFTS database:
```bash
python notion_content_manager.py \
  --action create_draft \
  --title "Post Title" \
  --content "Post content here (max 1300 chars)" \
  --style contrarian \
  --url "https://source-url.com"
```

**Note:** System validates LinkedIn's 1300 character limit and displays warnings if exceeded.

## Content Styles

### 1. Contrarian (contrarian)
**Best for:** Hot takes, controversial opinions
**Timing:** Wednesday 12:00
**Structure:**
```
[BOLD STATEMENT over {title}]

[3-5 regels met concrete data/voorbeelden uit eigen praktijk]

[Plot twist of nuance die discussie opent]

[Vraag die uitnodigt tot reactie]

#recruitment #technischepersoneel #hiring
```

### 2. Data Story (data_story)
**Best for:** Statistics, insights, data-driven content
**Timing:** Tuesday 08:00
**Structure:**
```
[Specifiek getal] over {title}

Dit is wat dit betekent voor recruitment in Oost-Nederland:

→ [Insight 1 met data]
→ [Insight 2 met voorbeeld]
→ [Insight 3 met actie]

[Conclusie + vraag aan lezer]

#recruitment #data #hiring
```

### 3. How-To (how_to)
**Best for:** Tips, tutorials, actionable advice
**Timing:** Thursday 08:00
**Structure:**
```
[Herkenbaar probleem rond {title}]

Hier is de fix in 4 stappen:

1. [Concrete actie 1]
2. [Concrete actie 2]
3. [Concrete actie 3]
4. [Concrete actie 4]

Resultaat: [Specifiek cijfer of uitkomst]

Save deze post voor later.

#recruitment #tips #hiring
```

### 4. Behind the Scenes (behind_scenes)
**Best for:** Personal stories, learnings, experiences
**Timing:** Friday 10:00
**Structure:**
```
[Eerlijke bekentenis rond {title}]

Dit gebeurde:
[Context in 2-3 zinnen]

Wat ik leerde:
[Concrete les met voorbeeld]

Nu doe ik dit anders:
[Nieuwe aanpak]

Herken je dit?

#recruitment #learnings #hiring
```

## Tone of Voice Guidelines

- **Direct en eerlijk**: "No-bullshit" approach
- **Data-driven**: Support claims with numbers and examples from own practice
- **Contrarian perspectives**: Challenge conventional thinking
- **Always end with a question**: Invite engagement and discussion
- **Maximum 1300 characters**: LinkedIn post limit (validated automatically)
- **3-5 hashtags**: Always at the bottom of posts

## Target Audience (ICP)

**Decision Makers:**
- Operations Directors / Technical Directors
- HR Managers
- Scale-up Founders

**Company Profile:**
- Size: 50-800 FTE
- Industry: Technical/Production sectors
- Region: Oost-Nederland

## Automation Workflow

### Daily Morning Routine (Recommended)
```bash
# 1. Fetch latest news articles
python notion_content_manager.py --action fetch_news --save

# 2. Review articles and select interesting topics
# 3. Generate template for selected topic
python notion_content_manager.py --action generate --title "Selected Topic" --style contrarian

# 4. Write content based on template
# 5. Create draft in Notion
python notion_content_manager.py --action create_draft \
  --title "Final Post Title" \
  --content "Completed content" \
  --style contrarian \
  --url "https://source.com"

# 6. Review and refine in Notion web interface
```

## Error Handling

The system includes comprehensive error handling:

- **Connection failures**: 10-second timeout with clear error messages
- **Missing credentials**: Validation at startup with setup instructions
- **API errors**: HTTP error details displayed for debugging
- **Invalid data**: Graceful handling of missing properties
- **Character limit warnings**: Non-blocking alerts for LinkedIn limit

## Security Best Practices

✅ **DO:**
- Store API key in `.env` file (never commit to git)
- Keep `.env` in `.gitignore`
- Use environment variables for credentials
- Regularly rotate API keys

❌ **DON'T:**
- Hardcode API keys in scripts
- Commit `.env` files to version control
- Share API keys in documentation or messages

## Troubleshooting

### "NOTION_API_KEY not found in environment variables"
1. Verify `.env` file exists in project root
2. Check that `NOTION_API_KEY` is set in `.env`
3. Ensure no spaces around the `=` sign
4. Restart your terminal/IDE to reload environment

### "Notion API connection failed"
1. Verify API key is valid at https://www.notion.so/my-integrations
2. Check that integration has access to your databases
3. Confirm database IDs are correct in the script
4. Test network connectivity to api.notion.com

### "Content exceeds LinkedIn limit"
This is a warning, not an error. The draft is still created, but you should:
1. Review and shorten the content in Notion
2. Remove unnecessary details
3. Consider splitting into multiple posts

## Development

### Adding New Content Styles

Edit `generate_template()` method in `notion_content_manager.py`:

```python
templates = {
    "your_style": """[Template structure here]

{title}

[More structure]

#hashtags""",
}
```

Then add to the choices in argparse configuration.

### Extending Database Properties

To add new properties, update the relevant methods:
- `fetch_news()`: Add property extraction logic
- `create_draft()`: Add property to page creation payload

## Related Systems

This Notion Content Manager is part of the larger Recruitin Content Intelligence System, which also includes:

- **Intelligence Hub**: Web scrapers for market trends, ICP monitoring, and competitor tracking (see main README.md)
- **GitHub Actions**: Automated weekly scraping workflows

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Notion API documentation: https://developers.notion.com
3. Verify database permissions in Notion workspace settings

## License

Internal tool for Recruitin B.V. - Not for public distribution.
