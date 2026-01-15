# Deploy to GitHub - Quick Guide

## ✅ Repository Status

Your repository is now initialized and ready for GitHub deployment:

```
✓ Git repository initialized
✓ All files committed (1607 files)
✓ GitHub Actions workflow configured
✓ Documentation complete
```

## 🚀 Deploy to GitHub (5 Minutes)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `recruitin-content-intelligence-system`
3. Description: `Automated content intelligence and management system for Recruitin B.V.`
4. Privacy: **Private** (recommended - contains business logic)
5. **Do NOT** initialize with README, .gitignore, or license (you already have these)
6. Click **Create repository**

### Step 2: Push to GitHub

GitHub will show you commands. Use these:

```bash
# Add remote origin
git remote add origin https://github.com/YOUR-USERNAME/recruitin-content-intelligence-system.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Replace** `YOUR-USERNAME` with your actual GitHub username.

### Step 3: Configure GitHub Actions Secret

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add secret:
   - Name: `NOTION_API_KEY`
   - Value: Your Notion API key from https://www.notion.so/my-integrations
5. Click **Add secret**

### Step 4: Enable Workflow Permissions

1. Still in **Settings**, go to **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select: ☑️ **Read and write permissions**
4. Check: ☑️ **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

### Step 5: Test the Automation

1. Go to **Actions** tab in your repository
2. Select **"Notion Content Manager - Daily Automation"**
3. Click **Run workflow** dropdown
4. Click **Run workflow** button (green)
5. Wait ~1 minute for completion
6. Check for green checkmark ✅

### Step 6: Verify Results

1. Click on the completed workflow run
2. Review job logs:
   - ✅ Fetch Daily Recruitment News
   - ✅ Generate Drafts Summary
   - ✅ Test Notion API Connection
3. Download artifacts to verify data export
4. Check repository for `news-YYYY-MM-DD.json` file

## 📋 Automated Schedule

Once deployed, the workflow will automatically run:

```
⏰ Every weekday (Monday-Friday) at 07:00 CET
```

Actions performed:
- Fetches latest recruitment news from Notion
- Exports to dated JSON files
- Lists current LinkedIn drafts
- Commits results to repository

## 🔗 Quick Access Links

After deployment, bookmark these:

- **Repository**: `https://github.com/YOUR-USERNAME/recruitin-content-intelligence-system`
- **Actions**: `https://github.com/YOUR-USERNAME/recruitin-content-intelligence-system/actions`
- **Settings**: `https://github.com/YOUR-USERNAME/recruitin-content-intelligence-system/settings`

## 📚 Documentation

Complete guides are available in your repository:

| File | Purpose |
|------|---------|
| `QUICK-START.md` | Fast setup and daily workflow |
| `GITHUB-ACTIONS-SETUP.md` | Detailed automation setup |
| `README-notion-content-manager.md` | Complete system documentation |
| `README.md` | Main project overview |

## ⚠️ Common Issues

### "remote: Permission denied"
**Problem**: SSH key not configured or HTTPS authentication failed

**Solution**:
```bash
# Use HTTPS with personal access token
git remote set-url origin https://github.com/YOUR-USERNAME/recruitin-content-intelligence-system.git

# Or set up SSH key at: https://github.com/settings/keys
```

### "NOTION_API_KEY not found" in workflow
**Problem**: Secret not configured

**Solution**:
- Verify secret name is exactly `NOTION_API_KEY` (case-sensitive)
- Check API key starts with `secret_`
- Ensure Notion integration has database access

### Workflow not running automatically
**Problem**: Schedule not active

**Solution**:
- Wait 24 hours - first scheduled run needs time
- Check Actions are enabled: Settings → Actions → General
- Repository must have activity (commits) in last 60 days

## ✅ Verification Checklist

After deployment, verify:

- [ ] Repository created on GitHub
- [ ] Code pushed successfully (1607 files)
- [ ] `NOTION_API_KEY` secret configured
- [ ] Workflow permissions enabled (read/write)
- [ ] Manual workflow run successful
- [ ] Test connection job passed
- [ ] News export artifact downloaded
- [ ] `news-YYYY-MM-DD.json` committed to repo
- [ ] Notion databases accessible

## 🎯 Next Steps

After successful deployment:

1. **Daily Routine** (07:30 CET):
   ```bash
   git pull
   cat news-$(date +%Y-%m-%d).json
   ```

2. **Generate Content**:
   ```bash
   python notion_content_manager.py \
     --action generate \
     --title "Your Topic" \
     --style contrarian
   ```

3. **Create Draft**:
   ```bash
   python notion_content_manager.py \
     --action create_draft \
     --title "LinkedIn Post Title" \
     --content "Your content here" \
     --style contrarian \
     --url "https://source.com"
   ```

## 🔐 Security Reminders

✅ **DO:**
- Keep `NOTION_API_KEY` in GitHub Secrets only
- Set repository to Private for business data
- Rotate API keys periodically
- Review workflow logs for errors

❌ **DON'T:**
- Commit `.env` file with real credentials
- Share API keys in issues or comments
- Make repository public with business data
- Disable required status checks

---

**Need Help?**
- Check workflow logs in Actions tab
- Review `GITHUB-ACTIONS-SETUP.md` for detailed troubleshooting
- Verify Notion integration permissions at https://www.notion.so/my-integrations

**System Version:** 1.0
**Last Updated:** 2026-01-15
**Status:** ✅ Ready for Deployment
