# GitHub Actions Setup Guide

## Notion Content Manager Automation

This guide explains how to set up automated daily content management using GitHub Actions.

## Overview

The automation runs **every weekday at 07:00 CET** and:
- ✅ Fetches latest recruitment news from Notion NEWS database
- ✅ Exports news to dated JSON files
- ✅ Lists current LinkedIn drafts
- ✅ Generates workflow summary reports
- ✅ Commits results back to repository

## Prerequisites

- GitHub repository with Actions enabled
- Notion API key with access to your databases
- Push access to the repository

## Setup Instructions

### Step 1: Configure GitHub Secret

1. Go to your GitHub repository
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Add the following secret:

   ```
   Name: NOTION_API_KEY
   Value: secret_your_notion_api_key_here
   ```

   Get your API key from: https://www.notion.so/my-integrations

### Step 2: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. If prompted, enable Actions for this repository
3. The workflow will appear as **"Notion Content Manager - Daily Automation"**

### Step 3: Test the Workflow

Run a manual test to verify everything works:

1. Go to **Actions** tab
2. Select **"Notion Content Manager - Daily Automation"**
3. Click **Run workflow** dropdown
4. Click **Run workflow** button

This will:
- Test your Notion API connection
- Fetch current news
- List existing drafts
- Generate artifacts

### Step 4: Review Results

After the workflow completes:

1. Click on the workflow run
2. Check the job logs for any errors
3. Download artifacts:
   - **daily-news-XXX**: JSON export of news articles
   - **workflow-summary-XXX**: Daily automation report

## Workflow Schedule

### Automatic Runs

```yaml
Monday-Friday at 07:00 CET (06:00 UTC)
```

This timing ensures news is aggregated before your workday starts.

### Manual Runs

You can trigger the workflow manually anytime:
1. Go to Actions tab
2. Select the workflow
3. Click "Run workflow"

Manual runs include an additional connection test job.

## Workflow Jobs

### 1. Fetch News (fetch-news)

**Purpose:** Aggregate daily recruitment news

**Steps:**
1. Checkout repository
2. Set up Python 3.11
3. Install dependencies from requirements.txt
4. Run: `python notion_content_manager.py --action fetch_news --save`
5. Commit news-YYYY-MM-DD.json to repository
6. Upload JSON as artifact

**Output:**
- File: `news-YYYY-MM-DD.json`
- Artifact: `daily-news-{run_number}`

### 2. List Drafts (list-drafts)

**Purpose:** Generate overview of current content pipeline

**Steps:**
1. Set up Python environment
2. Run: `python notion_content_manager.py --action list_drafts`
3. Generate workflow summary report
4. Upload summary as artifact

**Output:**
- File: `workflow-summary.md`
- Artifact: `workflow-summary-{run_number}`

### 3. Test Connection (test-connection)

**Purpose:** Verify Notion API connectivity

**Trigger:** Manual workflow runs only

**Steps:**
1. Set up Python environment
2. Run: `python notion_content_manager.py --action test`
3. Display connection status

## Artifacts

All workflow artifacts are retained for **30 days**.

### Daily News JSON

```json
{
  "export_date": "2024-01-15",
  "total_articles": 12,
  "articles": [
    {
      "title": "Article Title",
      "url": "https://...",
      "date": "2024-01-15",
      "score": 85
    }
  ]
}
```

### Workflow Summary

Markdown report with:
- Execution date and status
- Completed tasks checklist
- Next steps for content creation
- Quick links to Notion databases

## Integration with Daily Workflow

### Morning Routine (Automated)

**07:00 CET** - GitHub Actions runs automatically:
1. ✅ Fetches news from Notion
2. ✅ Exports to JSON
3. ✅ Lists current drafts
4. ✅ Commits results

### Your Daily Tasks (Manual)

**08:00-09:00** - Review and create content:

```bash
# 1. Pull latest news export
git pull

# 2. Review news file
cat news-$(date +%Y-%m-%d).json

# 3. Generate template for interesting topic
python notion_content_manager.py \
  --action generate \
  --title "Selected Topic" \
  --style contrarian

# 4. Create draft in Notion
python notion_content_manager.py \
  --action create_draft \
  --title "Post Title" \
  --content "Your content here" \
  --style contrarian \
  --url "https://source.com"
```

## Troubleshooting

### "NOTION_API_KEY not found"

**Problem:** Secret not configured correctly

**Solution:**
1. Verify secret name is exactly `NOTION_API_KEY`
2. Check secret value starts with `secret_`
3. Ensure integration has access to databases
4. Re-run workflow after updating secret

### Workflow Not Running Automatically

**Problem:** Schedule not triggering

**Solution:**
1. Check repository has recent activity (GitHub may disable Actions on inactive repos)
2. Verify Actions are enabled in repository settings
3. Check GitHub Actions status page for service issues
4. Try manual run to verify workflow configuration

### "Permission denied" on Commit

**Problem:** Workflow can't push commits

**Solution:**
1. Go to **Settings → Actions → General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Check **Allow GitHub Actions to create and approve pull requests**
5. Save changes

### News File Not Generated

**Problem:** Empty results from Notion

**Possibilities:**
1. NEWS database is empty
2. API key lacks database access
3. Database ID incorrect

**Debug:**
```bash
# Test locally with your credentials
python notion_content_manager.py --action fetch_news --save
```

### Python Dependencies Fail

**Problem:** pip install errors

**Solution:**
1. Verify requirements.txt is in repository root
2. Check Python version is 3.8+
3. Review workflow logs for specific error
4. Test locally: `pip install -r requirements.txt`

## Monitoring

### View Workflow History

1. Go to **Actions** tab
2. Select **"Notion Content Manager - Daily Automation"**
3. Review run history and status

### Email Notifications

GitHub automatically sends email notifications for:
- ❌ Failed workflow runs
- ✅ Fixed workflows (after previous failure)

Configure in: **Settings → Notifications → Actions**

## Security Best Practices

✅ **DO:**
- Store API key in GitHub Secrets (never in code)
- Use workflow_dispatch for testing
- Review workflow logs regularly
- Rotate API keys periodically

❌ **DON'T:**
- Commit .env files with real credentials
- Share secret values in issues or comments
- Use personal access tokens unnecessarily
- Disable required status checks

## Customization

### Change Schedule

Edit `.github/workflows/notion-content-automation.yml`:

```yaml
on:
  schedule:
    # Run at different time (UTC)
    - cron: '30 8 * * 1-5'  # 08:30 UTC = 09:30 CET
```

Use https://crontab.guru/ to test cron expressions.

### Add Notifications

Add Slack/Discord notifications:

```yaml
- name: Notify on completion
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "Daily news aggregation completed ✅"
      }
```

### Generate Content Automatically

Add content generation step:

```yaml
- name: Auto-generate draft
  env:
    NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
  run: |
    # Get top news article
    TITLE=$(jq -r '.articles[0].title' news-*.json)

    # Generate template
    python notion_content_manager.py \
      --action generate \
      --title "$TITLE" \
      --style contrarian
```

## Related Documentation

- Main README: `README.md`
- Content Manager docs: `README-notion-content-manager.md`
- Notion API: https://developers.notion.com
- GitHub Actions: https://docs.github.com/actions

## Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Verify secret configuration
3. Test commands locally
4. Review Notion integration permissions

---

**Last Updated:** 2024-01-15
**Workflow Version:** 1.0
**Maintained by:** Recruitin B.V.
