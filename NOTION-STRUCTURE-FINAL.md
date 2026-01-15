# 📊 NOTION STRUCTURE - Master Dashboard + Data Tabs

**Concept**: 1 Master overview + Detail tabs voor raw data
**Perfect!** Executive view + Deep-dive data

---

## 🏠 TAB 1: MASTER DASHBOARD (Home/Overview)

**Dit zie je eerste** - Alles in 1 oogopslag:

### KPI Scorecard (Top 10 Metrics)
```
┌─────────────────────────────────────────────────────┐
│  WEEK 2 - JANUARI 2026                              │
├─────────────────────────────────────────────────────┤
│  Omzet MTD    │ Pipeline  │ Deals Won │ New Deals  │
│  €72k ✅      │ €478k ✅  │ 4/4 ✅    │ 12/8 ✅    │
│                                                      │
│  Win Rate     │ Time-Fill │ Stuck     │ Activities │
│  55% ✅       │ 28d ✅    │ 12 🚨     │ 112 ✅     │
│                                                      │
│  Content      │ Followers │ Lead Conv │ Score      │
│  8/12 📈      │ +25 ✅    │ 15% ✅    │ 8/10 ✅    │
└─────────────────────────────────────────────────────┘
```

### Omzet Breakdown (Per Dienst)
| W&S | RPO | Interim | RMA | Total |
| €42k (58%) | €18k (25%) | €0 (0%) | €12k (17%) | €72k |

### Top 3 Priorities Deze Week
🚨 Stage 2 bottleneck (12 stuck)
💰 Close ASML + Dow (€43k)
📞 JobDigger batch score

### Quick Links to Tabs
→ [Alle 269 Deals](#tab-deals)
→ [Content Performance](#tab-content)
→ [Weekly News](#tab-news)

---

## 📋 TAB 2: DEALS - Raw Data (269 Deals)

**Volledige lijst** met filters/views:

### View 1: Alle Deals (Table)
| # | Deal Naam | Organisatie | Contact | € | Stage | Datum | Dagen | Owner |
|---|-----------|-------------|---------|---|-------|-------|-------|-------|
| 1 | [Deal 1] | [Org] | [Person] | €[X] | [Stage] | [Date] | [D]d | [Owner] |
| ... 269 rows ... |

**Filters**:
- By Stage (dropdown)
- By Owner (filter)
- By Value (>€20k, €10-20k, <€10k)
- Stuck only (>14d)

### View 2: Stuck Deals Only
Filter: Dagen >14

### View 3: High Value (>€20k)
Filter: Value >20000

### View 4: By Dienst
Group by: Service type (W&S, RPO, Interim, RMA)

**Use**: Deep-dive, find specific deals, export data

---

## 📰 TAB 3: NEWS - Raw Data (Weekly Articles)

**Alle scraped artikelen** per week:

### Week 2 - 163 Artikelen
- Source: Brave Search (31 queries)
- Categories: Technical recruitment, Engineering, Manufacturing
- Top 10: Highlighted
- Rest: Archived (searchable)

**Views**:
- By Source (UWV, CBS, RecruitmentTech, etc.)
- By Relevance Score (>70, 50-70, <50)
- Used for Content (Yes/No filter)

**Use**: Content research, trend analysis, archief

---

## 📊 TAB 4: CONTENT PERFORMANCE - Raw Data

**Database**: Content Performance Tracker (26 properties)

### View 1: Deze Week (Gallery)
Filter: Last 7 days

### View 2: All Posts (Table)
All time, sortable

### View 3: Top Performers (A-Tier Only)
Filter: Tier = A

### View 4: By Platform
Group by: Wouter/Recruitin/Blog

**Use**: Track performance, find best posts, replicate winners

---

## 📋 TAB 5: COMMANDS & WORKFLOWS - Reference

**Alle commands** (copy-paste ready):
- News scraping
- Content generation
- Pipedrive dashboards
- Claude Code commands (51!)

**Use**: Quick reference, onboarding, documentation

---

## 📅 TAB 6: SCHEDULE & CALENDAR - Planning

**Weekly schedule**:
- Vrijdag 17:00: Content
- Maandag 10:00: Metrics
- Daily actions

**Use**: Time blocking, routine reference

---

## 🎯 NAVIGATIE DESIGN

```
┌─────────────────────────────────────────────────────┐
│  RECRUITIN INTELLIGENCE HUB                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🏠 MASTER DASHBOARD  ← START HIER (Overview)      │
│     ├─ KPI Scorecard (10 metrics)                  │
│     ├─ Omzet per Dienst                            │
│     ├─ Stuck Deals (top 5)                         │
│     ├─ Week Priorities                             │
│     └─ Quick Links → Tabs                          │
│                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                     │
│  📋 TAB: Deals (269 deals - raw data)              │
│     4 views: All | Stuck | High Value | By Dienst  │
│                                                     │
│  📰 TAB: News (weekly articles - raw data)         │
│     Views: By Source | By Relevance | Used         │
│                                                     │
│  📊 TAB: Content Performance (tracking - raw data) │
│     Views: Week | All | Top | Platform             │
│                                                     │
│  📋 TAB: Commands (reference)                      │
│  📅 TAB: Schedule (planning)                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Design**:
- **MASTER** = Samenvatting (always visible)
- **TABS** = Details (drill down as needed)

**Perfect voor**:
- Quick check: MASTER (30 sec)
- Deep-dive: TAB (5 min)
- Executive: MASTER only
- Operational: MASTER + TABS

---

## 🎯 MORGEN BOUWEN

**Ik maak**:
1. **MASTER DASHBOARD** (bovenaan page)
   - 10 KPIs met live data
   - Omzet per dienst (W&S, RPO, Interim, RMA)
   - Stuck deals (top 5)
   - Goals tracking
   - Week priorities
   - Links naar tabs

2. **TABS blijven** (onder master)
   - Deals (269 deals data)
   - News (articles archief)
   - Content (performance tracking)
   - Commands (reference)
   - Schedule (planning)

**Structure**: Master (overview) + Tabs (raw data) ✅

**Is dit wat je bedoelde?** 🎯
