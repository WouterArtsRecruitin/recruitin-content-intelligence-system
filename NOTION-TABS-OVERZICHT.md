# 📊 NOTION HUB - Complete Tabs Overzicht

**URL**: https://notion.so/27c2252cbb1581a5bbfcef3736d7c14e
**Naam**: LinkedIn Intelligence Hub - Master Dashboard

---

## 📑 TABS/SECTIES IN NOTION (Nu Live!)

### 1. 📰 Week 2 Top 10 News
**Bevat**: Top 10 technical recruitment artikelen (deze week)
- Artikel titels met scores
- URLs naar bronnen
- Gebruikt status (✅/❌)

**Update**: Elke vrijdag (automatic via upload-to-correct-notion.js)

---

### 2. 📋 Complete Commands & Workflows
**Bevat**: Alle commands voor weekly content workflow
- News scraping commands
- Content generation prompts
- Publishing workflow
- 8-stappen quick start

**Static**: Eenmalig uploaded (reference)

---

### 3. 📊 Content Tracking Database Design
**Bevat**: Database schema uitleg
- 26 properties explained
- View configuratie
- Tracking workflow

**Static**: Documentation

---

### 4. 📅 Weekly Content Schedule
**Bevat**: Complete weekly schema
- Optimale posting tijden
- Outlook calendar info
- Daily/weekly/monthly routine

**Static**: Schedule reference

---

### 5. 📊 CONTENT INTELLIGENCE DASHBOARD
**Bevat**: Live database + views
- Content Performance Tracker (26 properties!)
- 3 embedded views:
  - Deze Week (gallery)
  - Performance (table)
  - Top Performers (filtered)
- Weekly Insights section (update maandag)

**Dynamic**: Update na elke post (vrijdag + maandag)

---

### 6. 📋 OPENSTAANDE DEALS ✅ NIEUW!
**Bevat**: Alle open Pipedrive deals
- Deal naam + Waarde
- Organisatie
- Contact persoon
- Stage + Dagen
- 🚨 Warning voor stuck deals (>14d)

**Kolommen**:
1. Deal naam (met value)
2. Organisatie
3. Contact persoon
4. Stage
5. Datum
6. Dagen in stage (met warning)

**Voorbeeld**:
```
1. 🚨 Siemens Enschede - Senior Automation - €28,000
   • Organisatie: Siemens Nederland
   • Contact: Jan de Vries
   • Stage: Stage 2 | 21 dagen
```

**Update**: Elke maandag (command: `node upload-deals-simple.js`)

---

## ⚡ UPDATE COMMANDS (Weekly)

**Vrijdag 17:05** - Top 10 News:
```bash
node upload-to-correct-notion.js
```

**Maandag 10:25** - Openstaande Deals:
```bash
node upload-deals-simple.js
```

**Maandag 10:30** - Content Metrics:
```
Manual update in database (LinkedIn stats)
```

---

## 📊 NOTION HUB NAVIGATIE

**Scroll door page** - van boven naar beneden zie je:

1. [Originele content - wat er al was]
2. 📰 Week 2 Top 10 News
3. 📋 Commands & Workflows
4. 📊 Database Design
5. 📅 Weekly Schedule
6. 📊 Content Intelligence Dashboard (met database!)
7. 💡 Weekly Insights
8. 📋 OPENSTAANDE DEALS ← NIEUW!
9. ⚡ Update commands

**Alles in 1 page**: Complete intelligence hub ✅

---

## 🎯 VOOR MORGEN

**Check Notion hub** (5 min):
- Open: https://notion.so/27c2252cbb1581a5bbfcef3736d7c14e
- Scroll: Door alle secties
- Zie: 8 deals staan erin (demo data)
- Configure: Database views (optioneel, 5 min)

**Met live Pipedrive data** (later):
```bash
export PIPEDRIVE_API_KEY=your_real_key
node upload-deals-simple.js
```

→ Real deals in Notion! ✅

---

**STATUS**: Openstaande Deals tab toegevoegd! ✅
