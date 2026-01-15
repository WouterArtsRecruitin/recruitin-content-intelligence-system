# 🧹 NOTION REORGANISATIE - Clean Master Dashboard

**Probleem**: Pagina is nu rommelig (teveel losse secties)
**Oplossing**: Clean structure met Master (top) + Tabs (collapsible)

---

## 🎯 NIEUWE STRUCTURE (Clean & Overzichtelijk)

### OPTIE A: Reorganiseer Bestaande Page (15 min)

**In Notion** (manual cleanup):

**Stap 1**: Archiveer oude rommel (5 min)
- Scroll door pagina
- Selecteer oude/dubbele secties
- Delete (of move to archive page)

**Stap 2**: Creëer clean structure (10 min)
- Voeg toggle blocks toe (collapsible sections)
- Organiseer in volgorde (zie hieronder)

---

### OPTIE B: Nieuwe Clean Page Maken (10 min) ← **AANBEVOLEN!**

**Stappenplan**:

**1. Maak nieuwe page** (2 min):
```
In Notion:
- Nieuwe page: "📊 Recruitin Master Dashboard"
- Icon: 📊
- Cover: Gradient (blauw/groen)
```

**2. Voeg structure toe** (8 min):
```
Gebruik template hieronder (copy-paste in Notion)
```

**3. Link vanuit oude hub** (1 min):
```
In oude hub:
- Bovenaan add link: "→ Nieuwe Master Dashboard"
```

**4. Update bookmarks**:
```
Nieuwe URL bookmark (wordt je start page)
```

**KLAAR!** Clean dashboard, oude = archief

---

## 📊 CLEAN DASHBOARD TEMPLATE (Copy-Paste in Notion)

```markdown
# 📊 RECRUITIN MASTER DASHBOARD

Week [X] | [Maand] 2026 | Wouter Arts

---

## 🎯 EXECUTIVE SUMMARY

### Top 4 KPIs (This Week)

Omzet MTD: €[X] (target: €70k)
Pipeline: €478,044 (269 deals)
Deals Won: [X] / 4
New Deals: [X] / 8

Status: 🟢🟡🔴 [Pick one]

### Top 3 Priorities

1. 🚨 [Priority 1]
2. 💰 [Priority 2]
3. 📞 [Priority 3]

---

## 📊 TOP 10 KPIs

/table (maak inline table)

| KPI | Week | Month | Target | Status |
|-----|------|-------|--------|--------|
| Revenue | [€] | [€] | €70k | [✅/📈/🚨] |
| Pipeline | - | €478k | €800k | ✅ |
| Placements | [X] | [X] | 4 | [Status] |
| Win Rate | - | [%] | >50% | [Status] |
| Time-to-Fill | - | [d] | <30d | [Status] |
| New Deals | [X] | [X] | 8 | [Status] |
| Stage 2 Conv | - | [%] | >45% | [Status] |
| Stuck Deals | - | [X] | <5 | [Status] |
| Activities | [X] | [X] | 100 | [Status] |
| Content | [X] | [X] | 12 | [Status] |

---

## 💰 OMZET PER DIENST

/table

| Dienst | Deals | Omzet | Pipeline | % Total | Status |
|--------|-------|-------|----------|---------|--------|
| W&S | [X] | €[X] | €[X] | [%] | ✅ |
| RPO | [X] | €[X] | €[X] | [%] | 📈 |
| Interim | [X] | €[X] | €[X] | [%] | 🔴 |
| RMA | [X] | €[X] | €[X] | [%] | 📊 |
| **TOTAAL** | [X] | €[X] | €478k | 100% | [Status] |

---

## 🚨 STUCK DEALS (>14d)

[Top 5 stuck deals - bullets]

1. [Deal] - €[X] | [Org] | [Days]d → [Action]
2. [Deal] - €[X] | [Org] | [Days]d → [Action]
3-5. [etc]

Total at risk: €[X]
Target: Resolve 5 deze week

---

## 🎯 DEZE WEEK (Ma-Vr)

**Ma**: [Top 3 acties]
**Di**: [Top 3 acties]
**Wo**: [Top 3 acties]
**Do**: [Top 3 acties]
**Vr**: [Top 3 acties]

---

## ⚡ QUICK UPDATES

/toggle "🔄 Update Dashboard (Click to expand)"

   Commands:
   ```bash
   python3 build-master-dashboard.py
   ```

   Frequency: Elke maandag 10:00
   Time: 5 minuten

---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📂 RAW DATA TABS (Detail Views)

/toggle "📋 DEALS - Alle 269 Openstaande Deals"

   /linked_database [Connect to Deals database]

   Views:
   - Alle deals (sorted by value)
   - Stuck only (>14d filter)
   - By dienst (W&S, RPO, Interim, RMA)
   - By stage

   [End toggle]

/toggle "📰 NEWS - Weekly Top 10 Artikelen"

   Week 2 - 12 jan 2026
   [Top 10 list]

   Week 3 - [next week]
   [etc]

   [End toggle]

/toggle "📊 CONTENT PERFORMANCE - Tracking Database"

   /linked_database [Connect to Content Tracker]

   Views:
   - Deze week
   - All posts
   - Top performers (A-tier)
   - By platform

   [End toggle]

/toggle "📋 COMMANDS - Quick Reference"

   [Alle commands hier]

   [End toggle]

/toggle "📅 SCHEDULE - Weekly Planning"

   [Calendar schema hier]

   [End toggle]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Updated: [Auto-timestamp]
```

---

## 🎯 WAAROM BETER?

**Voor**:
- ❌ Alles open (scroll hell)
- ❌ Geen overview (direct in details)
- ❌ Onoverzichtelijk (wat is belangrijk?)

**Na**:
- ✅ Master bovenaan (executive summary)
- ✅ Tabs collapsed (details on-demand)
- ✅ Clean (1 scherm overview)
- ✅ Drill-down (open tab voor details)

**Perfect voor**:
- Morning check: MASTER only (30 sec)
- Deep work: Open relevante tab (5 min)
- Executive: Share page = professional

---

## 📋 IMPLEMENTATIE MORGEN (15 min)

### Optie A: Reorganiseer Huidige

**In je Notion page**:
1. Bovenaan: Add "📊 MASTER DASHBOARD" heading
2. Onder master: Add KPI scorecard (table)
3. Alle details: Convert to Toggle blocks (collapsible)
4. Cleanup: Delete dubbele/oude secties

**Time**: 15 minuten manual werk

---

### Optie B: Nieuwe Page (MAKKELIJKER!)

**Nieuwe clean page maken**:
1. Duplicate huidige page
2. Delete alles behalve essentials
3. Reorganiseer met template hierboven
4. Bookmark nieuwe page

**Time**: 10 minuten

**Voordeel**: Oude page blijft (backup), nieuwe = clean

---

## 🤖 AUTOMATIC REBUILD (Later)

**Script**: `rebuild-clean-dashboard.py`

**Wat het doet**:
- Create nieuwe page
- Build clean structure (master + tabs)
- Populate met live data
- Return nieuwe page URL

**Command**:
```bash
python3 rebuild-clean-dashboard.py
```

**Output**: Nieuwe clean dashboard page ✅

**Wil je dat ik dit script maak?** (30 min werk)

---

## 💡 VOOR NU - QUICK FIX

**In je Notion** (5 minuten):

1. **Scroll naar top**
2. **Add heading**: "📊 MASTER DASHBOARD - KIJK HIER EERST"
3. **Add callout**: "Overview: Scroll down voor details | Tabs onderaan voor raw data"
4. **Add divider** onder master
5. **All details**: Scroll voorbij = tabs

**Result**: Duidelijke scheiding (master vs tabs)

---

**Welke optie**:
- A: Reorganiseer huidige (15 min manual)
- B: Nieuwe page maken (10 min, cleaner)
- C: Script laten bouwen (30 min, dan automatic)

**Wat wil je?** 🎯
