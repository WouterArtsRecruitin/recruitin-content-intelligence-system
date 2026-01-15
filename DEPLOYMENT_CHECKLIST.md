# DEPLOYMENT CHECKLIST - Intelligence Hub Scrapers

**Target:** Week 1 - First Production Run  
**Deadline:** Maandag 20 januari 08:00

---

## ✅ PRE-DEPLOYMENT

### 1. Environment Setup
- [ ] Server/VPS met Node.js 18+ geïnstalleerd
- [ ] Puppeteer dependencies: `sudo apt-get install -y chromium-browser`
- [ ] Git repo clone: `git clone [repo-url]`
- [ ] Dependencies: `npm install`
- [ ] Output directory: `mkdir scraper-output`
- [ ] File permissions: `chmod +x *.js`

### 2. Configuration Review
- [ ] **market-trends-scraper.js:** Keywords + locaties check
- [ ] **icp-monitor.js:** Bedrijven lijst actueel (17 bedrijven)?
- [ ] **concurrent-tracker.js:** Concurrent URLs kloppen?
- [ ] Delays voldoende (niet te aggressive)?

### 3. Test Run (Local/Staging)
```bash
# Test elke scraper individueel
node market-trends-scraper.js   # ~3-5 min
node icp-monitor.js              # ~2-3 min  
node concurrent-tracker.js       # ~4-6 min

# Check output
ls -la scraper-output/
cat scraper-output/market_summary_*.txt
cat scraper-output/icp_report_*.txt
cat scraper-output/concurrent_summary_*.txt
```

**Expected Output:**
- [x] 3x CSV files gegenereerd
- [x] 3x TXT summary reports
- [x] Geen fatal errors in console
- [x] Data ziet er logisch uit (geen 0 values overal)

### 4. Google Sheets Import Test
- [ ] Open spreadsheet: https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit
- [ ] Handmatig import testen:
  - [ ] market_trends_[DATE].csv → Market Trends sheet
  - [ ] icp_activity_[DATE].csv → ICP Monitor sheet
  - [ ] concurrent_activity_[DATE].csv → Concurrent Tracker sheet
- [ ] Formules werken? (Trend % kolommen berekenen?)
- [ ] Conditional formatting klopt? (HOT/WARM/COLD kleuren)

---

## 🚀 PRODUCTION DEPLOYMENT

### OPTIE A: Cron Job (VPS)
```bash
# Edit crontab
crontab -e

# Voeg toe (wekelijks maandag 08:00):
0 8 * * 1 cd /path/to/scrapers && /usr/bin/node market-trends-scraper.js >> /var/log/scraper-market.log 2>&1
0 9 * * 1 cd /path/to/scrapers && /usr/bin/node icp-monitor.js >> /var/log/scraper-icp.log 2>&1
0 10 * * 1 cd /path/to/scrapers && /usr/bin/node concurrent-tracker.js >> /var/log/scraper-concurrent.log 2>&1

# Verify cron
crontab -l
```

**Checklist:**
- [ ] Cron entries toegevoegd
- [ ] Absolute paths gebruikt (/usr/bin/node)
- [ ] Log files aangemaakt: `touch /var/log/scraper-*.log`
- [ ] Test cron werkt: `sudo service cron status`

### OPTIE B: GitHub Actions (Gratis)
```bash
# Create workflow file
mkdir -p .github/workflows
nano .github/workflows/scrapers.yml
# [Kopieer inhoud uit README]

# Push to GitHub
git add .
git commit -m "Add weekly scraper workflow"
git push origin main
```

**Checklist:**
- [ ] `.github/workflows/scrapers.yml` exists
- [ ] Workflow enabled in GitHub repo settings
- [ ] Test: trigger manual run via Actions tab
- [ ] Artifacts downloaden + CSV checken

### OPTIE C: Vercel Cron (Recommended voor Recruitin)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod

# Add cron config
nano vercel.json
# [Zie README voor config]

# Redeploy
vercel --prod
```

**Checklist:**
- [ ] Vercel project created
- [ ] `vercel.json` with cron configured
- [ ] API routes created: `/api/scrape-market.js` etc.
- [ ] Test cron in Vercel dashboard
- [ ] Logs zichtbaar in Vercel

---

## 🔗 DAY 3: ZAPIER INTEGRATION

**Goal:** Automatisch CSV naar Google Sheets + Slack notificaties

### Zap 1: Market Trends → Sheets
- [ ] Trigger: Email/Webhook met CSV attachment
- [ ] Action 1: Parse CSV
- [ ] Action 2: Google Sheets - Update rows
- [ ] Action 3: Slack notificatie (high ghosting risk)

### Zap 2: ICP Activity → Sheets  
- [ ] Trigger: Email/Webhook met CSV attachment
- [ ] Action 1: Parse CSV
- [ ] Action 2: Google Sheets - Update rows
- [ ] Action 3: Slack notificatie (HOT companies)

### Zap 6: Concurrent Activity → Sheets
- [ ] Trigger: Email/Webhook met CSV attachment
- [ ] Action 1: Parse CSV
- [ ] Action 2: Google Sheets - Update rows
- [ ] Action 3: Slack notificatie (HIGH threat)

**Test Scenario:**
- [ ] Run scraper manually
- [ ] CSV automatisch geïmporteerd?
- [ ] Slack notificatie ontvangen?
- [ ] Data in juiste sheet + format?

---

## 📊 WEEK 1 VALIDATION

### Success Criteria
Na eerste production run (maandag 20 jan):

**Data Quality:**
- [ ] Market Trends: Min. 40/60 keywords hebben data (>0 vacatures)
- [ ] ICP Monitor: Min. 12/17 bedrijven hebben activity score >0
- [ ] Concurrent Tracker: Min. 6/8 concurrenten hebben content detected

**Technical:**
- [ ] Geen crashes/fatal errors
- [ ] Runtime < 15 minuten totaal
- [ ] CSV files valid + importable
- [ ] Geen rate limiting/IP blocks

**Business Value:**
- [ ] Min. 3 actionable insights uit data (ghosting risks, hot companies, concurrent threats)
- [ ] Summary reports zijn bruikbaar voor weekly sales meeting
- [ ] Wouter kan data interpreteren zonder tech support

---

## 🐛 ROLLBACK PLAN

Als scrapers niet werken in productie:

1. **Check logs:**
   ```bash
   tail -f /var/log/scraper-*.log
   # Of Vercel/GitHub Actions logs
   ```

2. **Fallback: Handmatige run**
   ```bash
   ssh [server]
   cd /path/to/scrapers
   node market-trends-scraper.js
   # Check output + errors
   ```

3. **Emergency: Skip automation**
   - Download CSVs lokaal
   - Handmatige import in Google Sheets
   - Debug scraper issues offline

4. **Contact:**
   - Claude: troubleshoot script
   - Zapier support: als Zap issue
   - Server admin: als infra issue

---

## 📅 TIMELINE

**Nu (12 jan):**
- ✅ Scrapers gebouwd
- ✅ README + deployment docs
- ⏳ Test run (lokaal)

**Dinsdag 14 jan:**
- Deploy naar productie (VPS/GitHub/Vercel)
- Eerste test run productie

**Woensdag 15 jan:**
- Zapier Zaps configureren
- End-to-end test

**Vrijdag 17 jan:**
- Final validation
- Fix bugs

**Maandag 20 jan 08:00:**
- 🚀 EERSTE PRODUCTION RUN
- Data in Sheets
- Weekly sales meeting met fresh intelligence

---

## ✅ SIGN-OFF

**Developer:** ___________  (Datum: _______)
**Tester:** ___________  (Datum: _______)
**Goedkeuring Wouter:** ___________  (Datum: _______)

**Notes:**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
