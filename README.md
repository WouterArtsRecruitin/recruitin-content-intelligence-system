# INTELLIGENCE HUB - SCRAPING SCRIPTS

**Status:** Day 2 - Agent-Browser Scrapers  
**Created:** 2025-01-12  
**Spreadsheet:** https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit

---

## 📦 SCRAPERS OVERZICHT

### 1️⃣ market-trends-scraper.js
**Doel:** Monitor vacature-trends op Indeed.nl en Monsterboard.nl

**Data Output:**
- `market_trends_[DATE].csv` - Vacature counts per keyword/locatie
- `ghosting_patterns_[DATE].csv` - Concurrent activity (ghosting risk)
- `market_summary_[DATE].txt` - Samenvatting + trends

**Configuratie:**
- 10 keywords (automation engineer, field service, maintenance, etc.)
- 3 locaties (Gelderland, Overijssel, Noord-Brabant)
- 2 bronnen (Indeed, Monsterboard)
- Total: 60 scrapes per run

**Metrics:**
- Vacature count per keyword/locatie
- Salary ranges (Indeed)
- Ghosting risk (HIGH/MEDIUM/LOW o.b.v. concurrent activiteit)
- Week-over-week trends

---

### 2️⃣ icp-monitor.js
**Doel:** Monitor ICP bedrijven voor hiring signals & nieuws

**Data Output:**
- `icp_activity_[DATE].csv` - Activity scores + status per bedrijf
- `icp_report_[DATE].txt` - Detailed breakdown + action items

**Configuratie:**
- 17 target bedrijven (Stork, Siemens, VDL, BAM, Alfen, etc.)
- 5 sectoren (Automation, Manufacturing, Construction, Infrastructure, Renewable)
- Career page detection (6 URL patterns)
- Google News search
- LinkedIn presence check

**Metrics:**
- Activity Score (0-100)
- Status: HOT (70-100) | WARM (40-69) | COLD (0-39)
- Action Priority: IMMEDIATE | THIS WEEK | MONITOR

---

### 3️⃣ concurrent-tracker.js
**Doel:** Monitor concurrent content activiteit (blog, PR, LinkedIn)

**Data Output:**
- `concurrent_activity_[DATE].csv` - Content metrics per concurrent
- `concurrent_summary_[DATE].txt` - Threat analysis + acties

**Configuratie:**
- 8 concurrenten (Yacht, Brunel, Olympia, Tempo-Team, Randstad, Unique, Manpower, Cottus)
- Content kanalen: Blog, LinkedIn, Google News
- Relevantie scoring op basis van keywords
- Threat level: HOOG | GEMIDDELD | LAAG | MINIMAAL

**Metrics:**
- Blog posts + relevantie %
- LinkedIn posts + relevantie %
- News items + relevantie %
- Activity Level: ZEER ACTIEF | ACTIEF | MATIG ACTIEF | INACTIEF
- Threat Level o.b.v. volume + relevantie

---

## 🚀 DEPLOYMENT

### Requirements
```bash
# Node.js 18+ vereist
node --version  # Check versie

# Dependencies
npm install puppeteer
```

### Local Testing
```bash
# Test individuele scraper
node market-trends-scraper.js
node icp-monitor.js
node concurrent-tracker.js

# Output verschijnt in ./scraper-output/
ls -la scraper-output/
```

### Production Setup

**OPTIE A: Cron Job (VPS/Server)**
```bash
# Wekelijkse run (elke maandag 08:00)
crontab -e

# Add:
0 8 * * 1 cd /path/to/scrapers && node market-trends-scraper.js
0 9 * * 1 cd /path/to/scrapers && node icp-monitor.js
0 10 * * 1 cd /path/to/scrapers && node concurrent-tracker.js
```

**OPTIE B: GitHub Actions (Gratis)**
```yaml
# .github/workflows/scrapers.yml
name: Weekly Scrape
on:
  schedule:
    - cron: '0 8 * * 1'  # Elke maandag 08:00 UTC
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install puppeteer
      - run: node market-trends-scraper.js
      - run: node icp-monitor.js
      - run: node concurrent-tracker.js
      - uses: actions/upload-artifact@v3
        with:
          name: scraper-output
          path: scraper-output/
```

**OPTIE C: Vercel Cron (Recommended)**
```json
// vercel.json
{
  "crons": [
    {
      "path": "/api/scrape-market",
      "schedule": "0 8 * * 1"
    },
    {
      "path": "/api/scrape-icp",
      "schedule": "0 9 * * 1"
    },
    {
      "path": "/api/scrape-concurrent",
      "schedule": "0 10 * * 1"
    }
  ]
}
```

---

## 📊 GOOGLE SHEETS IMPORT

### Automatisch (via Zapier - Day 3)
**Zap 1:** market-trends-scraper.js → Market Trends sheet  
**Zap 2:** icp-monitor.js → ICP Monitor sheet  
**Zap 6:** concurrent-tracker.js → Concurrent Tracker sheet

### Handmatig
1. Run scraper: `node market-trends-scraper.js`
2. Open CSV: `scraper-output/market_trends_2025-01-12.csv`
3. Google Sheets → File → Import → Upload → Replace data
4. Target sheet: "Market Trends"

---

## ⚙️ CONFIGURATIE AANPASSEN

### Keywords wijzigen (market-trends-scraper.js)
```javascript
// Regel 17-28
const CONFIG = {
  keywords: [
    'jouw custom keyword hier',
    // ...
  ]
}
```

### Bedrijven toevoegen (icp-monitor.js)
```javascript
// Regel 17-50
const CONFIG = {
  companies: [
    {
      name: 'Nieuw Bedrijf',
      sector: 'Jouw Sector',
      domain: 'nieuwbedrijf.nl'
    }
  ]
}
```

### Concurrenten aanpassen (concurrent-tracker.js)
```javascript
// Regel 17-80
const CONFIG = {
  concurrenten: [
    {
      naam: 'Nieuwe Concurrent',
      blogUrl: 'https://...',
      linkedinUrl: 'https://...'
    }
  ]
}
```

---

## 🐛 TROUBLESHOOTING

### "Puppeteer failed to download Chrome"
```bash
# Install Chrome manually
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# Or set custom executable
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome
```

### Rate Limiting / IP Blocks
```javascript
// Verhoog delays in CONFIG
delays: {
  betweenKeywords: 5000,  // 5 seconden
  betweenRequests: 3000   // 3 seconden
}
```

### Timeout Errors
```javascript
// Verhoog timeout
await page.goto(url, { 
  waitUntil: 'networkidle2',
  timeout: 30000  // 30 seconden
});
```

---

## 📅 ROADMAP

### Week 1 (IN PROGRESS)
- ✅ Day 1: Google Sheets setup + CSV samples
- ✅ Day 2: Agent-Browser scrapers (market, ICP, concurrent)
- ⏳ Day 3: Zapier workflows (3 Zaps)

### Week 2
- Day 4-5: Slack alerts, dashboard refinement
- Day 6-7: Testing + eerste production run

### Week 3-4
- Historical data collection (4 weken)
- Trend analysis validation
- Iterate op basis van data insights

---

## 📂 FILE STRUCTURE

```
intelligence-hub/
├── market-trends-scraper.js       # Vacature trends
├── icp-monitor.js                 # ICP activiteit
├── concurrent-tracker.js          # Concurrent content
├── scraper-output/                # Output directory
│   ├── market_trends_2025-01-12.csv
│   ├── ghosting_patterns_2025-01-12.csv
│   ├── market_summary_2025-01-12.txt
│   ├── icp_activity_2025-01-12.csv
│   ├── icp_report_2025-01-12.txt
│   ├── concurrent_activity_2025-01-12.csv
│   └── concurrent_summary_2025-01-12.txt
├── package.json
├── README.md                      # This file
└── .github/
    └── workflows/
        └── scrapers.yml           # GitHub Actions (optioneel)
```

---

## 🔗 LINKS

- **Spreadsheet:** https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit
- **Day 1 Files:** `/home/claude/*.csv` + import guides
- **Transcripts:** `/mnt/transcripts/2026-01-12-12-*.txt`

---

## 📞 SUPPORT

Vragen? Check:
1. Deze README
2. Script comments (alle 3 scrapers zijn uitgebreid gedocumenteerd)
3. Day 1 import guides (`market_trends_import_guide.md`)
4. Previous transcripts voor context

---

**Last Updated:** 2025-01-12  
**Version:** 1.0  
**Status:** Ready for deployment testing
