# INTELLIGENCE HUB - QUICK REFERENCE

**Voor:** Wouter Arts | Recruitin B.V.  
**Update:** Elke maandag 08:00 (automated)

---

## 🎯 WHAT IT DOES

**3 Scrapers = 3 CSV Reports:**

1. **Market Trends** → Vacature intel (Indeed + Monsterboard)
2. **ICP Monitor** → Target bedrijven activiteit  
3. **Concurrent Tracker** → Wat doen concurrenten?

**Output:** Google Sheets met live data + Slack alerts

---

## ⚡ QUICK COMMANDS

```bash
# Run ALL scrapers (10-15 min)
npm run scrape:all

# Run individueel
npm run scrape:market      # 3-5 min
npm run scrape:icp         # 2-3 min
npm run scrape:concurrent  # 4-6 min

# Check output
ls -la scraper-output/
cat scraper-output/*_summary_*.txt
```

---

## 📊 WHERE IS THE DATA?

**Google Sheets:**  
https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit

**Sheets:**
- Market Trends (vacature counts + ghosting risk)
- ICP Monitor (target bedrijven activiteit)
- Concurrent Tracker (content activiteit concurrenten)
- Client Intelligence (placeholder)
- Campaign ROI (placeholder)
- Regional Insights (placeholder)
- Lead Attribution (placeholder)
- Executive Dashboard (overview)

**Local CSVs:**
- `./scraper-output/market_trends_[DATE].csv`
- `./scraper-output/icp_activity_[DATE].csv`
- `./scraper-output/concurrent_activity_[DATE].csv`

---

## 🚨 WHAT TO WATCH

### Market Trends
- **Ghosting Risk = HIGH?** → Concurrenten zeer actief op die keyword
- **Vacature Count omhoog?** → Groeiende vraag
- **Salary Range stijgend?** → Markt wordt duurder

### ICP Monitor  
- **Status = HOT?** → BEL NU (binnen 24u)
- **Status = WARM?** → Actie deze week
- **News Signal?** → Check wat ze doen, relevant voor pitch?

### Concurrent Tracker
- **Threat Level = HOOG?** → Review hun content, maak counter-content
- **Activity Level = ZEER ACTIEF?** → Ze zijn veel bezig, blijf scherp
- **Relevance >60%?** → Ze focussen op onze markt

---

## 🔧 TROUBLESHOOTING

| Probleem | Oplossing |
|----------|-----------|
| "No data in CSV" | Check internet, probeer opnieuw over 1u |
| "Rate limited" | Verhoog delays in CONFIG (zie README) |
| "Timeout error" | Verhoog timeout in scraper (regel ~100) |
| "Chrome not found" | Install: `sudo apt install chromium-browser` |
| "Zap didn't trigger" | Check email/webhook, manual import CSV |

---

## 📞 SUPPORT

1. **Check README.md** (full docs)
2. **Check DEPLOYMENT_CHECKLIST.md** (setup guide)
3. **Check script comments** (alles is gedocumenteerd)
4. **Check logs:** `tail -f /var/log/scraper-*.log`
5. **Claude:** "Fix [error message] in [scraper-name]"

---

## 🎬 WEEKLY ROUTINE

**Elke maandag 08:00:**
1. Scrapers runnen automatisch (cron/GitHub/Vercel)
2. Data komt binnen in Google Sheets
3. Slack notificaties voor HIGH priority items
4. Open Executive Dashboard in Sheets
5. Review actionable insights (5-10 min)
6. Plan acties voor de week

**Wat te doen met insights:**
- HOT ICP bedrijf? → Belt het sales team
- Ghosting risk HIGH? → Pas SEA/ads targeting aan
- Concurrent threat? → Review content strategie
- Vacature trend omhoog? → Prioriteit voor die keyword

---

## 📈 SUCCESS METRICS

**Week 1 Target:**
- ✅ 3 scrapers operational
- ✅ Data in Google Sheets
- ✅ Min. 3 actionable insights per week

**Month 1 Target:**
- 4 weken data history
- Trend analysis werkend
- Min. 2 nieuwe klanten via ICP monitoring

**Quarter 1 Target:**
- Predictive insights (welke bedrijven gaan hiring doen?)
- ROI zichtbaar (€X aan deals via intelligence)
- Concurrent alerting 100% accurate

---

## 🔗 LINKS

- **Spreadsheet:** https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit
- **README:** `/home/claude/README.md`
- **Deployment:** `/home/claude/DEPLOYMENT_CHECKLIST.md`
- **Transcripts:** `/mnt/transcripts/2026-01-12-*.txt`

---

**Print deze pagina en hang hem bij je bureau. 📌**
