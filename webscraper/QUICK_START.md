# ⚡ QUICK START - 15 MINUTEN SETUP

## 🎯 JE HEBT ALLES KLAAR!

**Spreadsheet:** https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit

---

## 📋 STAP 1: CSV DATA IMPORTEREN (5 MIN)

Open de spreadsheet en copy-paste deze files:

### Market Trends (Sheet 1)
```bash
cat /home/claude/market_trends_data.csv
```
➜ Select A2, paste, done ✅

### ICP Activity (Sheet 2)
```bash
cat /home/claude/icp_activity_data.csv
```
➜ Select A2, paste, done ✅

### Ghosting Patterns (Sheet 3)
```bash
cat /home/claude/ghosting_patterns_data.csv
```
➜ Select A2, paste, done ✅

### Sector News (Sheet 4)
```bash
cat /home/claude/sector_news_data.csv
```
➜ Select A2, paste, done ✅

### Concurrent Activity (Sheet 5)
```bash
cat /home/claude/concurrent_activity_data.csv
```
➜ Select A2, paste, done ✅

### Newsletter Monthly Data (Sheet 6)
```bash
cat /home/claude/newsletter_monthly_data.csv
```
➜ Select A2, paste, done ✅

### Dashboard (Sheet 7)
```bash
cat /home/claude/dashboard_data.csv
```
➜ Select A2, paste, done ✅

---

## ✅ STAP 2: VALIDATIE TESTEN (2 MIN)

1. Go to **Market Trends** sheet
2. Click cell **C3** → Should show dropdown with 12 functiegroepen
3. Click cell **D3** → Should show dropdown with 6 regions
4. If dropdowns work ✅ = SUCCESS!

---

## 🎨 STAP 3: CONDITIONAL FORMATTING (OPTIONAL - 3 MIN)

**Market Trends - Priority colors:**
1. Select N2:N1000
2. Format → Conditional formatting
3. Add rules:
   - HIGH = Red #FF6B6B
   - MEDIUM = Orange #FFA500
   - LOW = Green #90EE90

**Repeat for:** ICP Activity (col J), Sector News (col H), Concurrent Activity (col J)

---

## 📊 VERIFICATIE

- [ ] Market Trends heeft 10 data rows
- [ ] ICP Activity heeft 7 data rows
- [ ] Ghosting heeft 6 data rows
- [ ] Sector News heeft 7 data rows
- [ ] Concurrent heeft 7 data rows
- [ ] Newsletter heeft 1 data row
- [ ] Dashboard heeft 10 metrics
- [ ] Dropdowns werken in Market Trends (col C, D)

---

## 🚀 KLAAR!

Je Intelligence Hub is nu **LIVE**! 

**Next steps:**
- Day 2: Agent-Browser scraping scripts
- Day 3: Zapier workflows bouwen
- Week 1 goal: Eerste automated scrape + 3 test posts

**Vragen?** wouter@recruitin.nl

---

**Files:**
- `/home/claude/COMPLETE_IMPORT_GUIDE.md` - Gedetailleerde guide
- `/home/claude/*.csv` - Alle data files
- `/home/claude/intelligence_hub_config.json` - Complete config

