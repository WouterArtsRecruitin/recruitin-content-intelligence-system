# Quick Start Guide - Notion Content Manager

## 🚀 Complete Setup in 5 Minutes

### Step 1: Local Setup (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials
cp .env.example .env
# Edit .env and add your NOTION_API_KEY from https://www.notion.so/my-integrations

# 3. Test connection
python notion_content_manager.py --action test
```

### Step 2: GitHub Actions Setup (3 minutes)

```bash
# 1. Add GitHub Secret
# Go to: Settings → Secrets and variables → Actions
# Add: NOTION_API_KEY = your_notion_key

# 2. Enable workflow permissions
# Go to: Settings → Actions → General
# Select: Read and write permissions
# Save

# 3. Test workflow
# Go to: Actions → Notion Content Manager → Run workflow
```

## 📋 Daily Workflow

### Automated (Every Weekday 07:00 CET)

GitHub Actions automatically:
- ✅ Fetches recruitment news from Notion
- ✅ Exports to news-YYYY-MM-DD.json
- ✅ Commits to repository

### Manual (Your Morning Routine)

```bash
# Pull latest news
git pull

# Review news
cat news-$(date +%Y-%m-%d).json

# Generate content template
python notion_content_manager.py \
  --action generate \
  --title "Interessant Nieuwsitem" \
  --style contrarian

# Create draft in Notion
python notion_content_manager.py \
  --action create_draft \
  --title "LinkedIn Post Titel" \
  --content "Je content hier (max 1300 chars)" \
  --style contrarian \
  --url "https://bron.com"
```

## 🎯 Available Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `--action test` | Test Notion connection | See connection status |
| `--action fetch_news` | Get latest articles | `--save` to export JSON |
| `--action list_drafts` | View all drafts | See title, style, status |
| `--action generate` | Create post template | `--title "News" --style contrarian` |
| `--action create_draft` | Add draft to Notion | `--title --content --style --url` |

## 🎨 Content Styles

| Style | Best For | Timing | Hashtags |
|-------|----------|--------|----------|
| `contrarian` | Hot takes, meningen | Wed 12:00 | #recruitment #technischepersoneel |
| `data_story` | Cijfers, insights | Tue 08:00 | #recruitment #data #hiring |
| `how_to` | Tips, tutorials | Thu 08:00 | #recruitment #tips #hiring |
| `behind_scenes` | Persoonlijk, learnings | Fri 10:00 | #recruitment #learnings |

## 📊 Notion Databases

**NEWS Database**
- ID: `2e62252c-bb15-8126-97a9-eb7166e6b3b8`
- Link: https://notion.so/2e62252c-bb15-8126-97a9-eb7166e6b3b8

**DRAFTS Database**
- ID: `50bc3e75-94d7-4b5b-a12a-96762ef29784`
- Link: https://notion.so/50bc3e75-94d7-4b5b-a12a-96762ef29784

## 🎯 Target Audience (ICP)

**Decision Makers:**
- Operations/Technisch Directeuren
- HR Managers
- Scale-up Founders

**Company Profile:**
- 50-800 FTE
- Technisch/Productie
- Oost-Nederland

## 📝 Tone of Voice

- ✅ Direct en eerlijk ("no-bullshit")
- ✅ Data-driven met voorbeelden
- ✅ Contrarian perspectives
- ✅ Altijd eindigen met vraag
- ✅ Max 1300 karakters
- ✅ 3-5 hashtags onderaan

## ⚠️ Common Issues

**"NOTION_API_KEY not found"**
```bash
# Check .env file exists
ls -la .env

# Verify format (no spaces around =)
cat .env
```

**"Connection failed"**
- Verify API key at https://www.notion.so/my-integrations
- Check integration has database access
- Test network: `curl https://api.notion.com/v1`

**"Content exceeds limit"**
- Warning only, draft still created
- Edit in Notion to shorten

## 📚 Documentation

- **Full docs:** README-notion-content-manager.md
- **GitHub setup:** GITHUB-ACTIONS-SETUP.md
- **Main system:** README.md

## 🔗 Quick Links

- [Notion Integrations](https://www.notion.so/my-integrations)
- [GitHub Actions](https://github.com/YOUR-REPO/actions)
- [Cron Schedule Helper](https://crontab.guru/)

---

**Need help?** Check the full documentation or workflow logs in GitHub Actions.
