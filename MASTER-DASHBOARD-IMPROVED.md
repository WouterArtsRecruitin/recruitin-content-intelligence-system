# 📊 MASTER DASHBOARD - Verbeterd Concept

**Live Pipedrive Data**: 269 deals | €478,044 pipeline
**Google Sheets Voorbeeld**: Bekeken (clean structure!)

---

## 🎯 VERBETERD DASHBOARD ONTWERP (1 Scherm)

### SECTIE 1: KPI SCORECARD (Top)

```
═══════════════════════════════════════════════════════════════════════════
WEEK 2 - JANUARI 2026 | WOUTER ARTS | RECRUITIN B.V.
═══════════════════════════════════════════════════════════════════════════

┌────────────┬────────────┬────────────┬────────────┬────────────┐
│  OMZET MTD │  PIPELINE  │  DEALS WON │  NEW DEALS │  WIN RATE  │
│  [€72k]    │  €478,044  │  4 / 4 ✅  │  12 / 8 ✅ │  55% ✅    │
├────────────┼────────────┼────────────┼────────────┼────────────┤
│ TIME-FILL  │  STUCK >14 │  ACTIVITEIT│  CONTENT   │  FOLLOWERS │
│  28d ✅    │  12 🚨     │  112 ✅    │  8 / 12    │  +25 ✅    │
└────────────┴────────────┴────────────┴────────────┴────────────┘

HEALTH: 🟡 Yellow (8/10 targets, maar Stage 2 bottleneck!)
```

---

### SECTIE 2: OMZET PER DIENST (Tabel)

| Dienst | Deals MTD | Omzet MTD | Pipeline | Avg Fee | % Total | Target | Status |
|--------|-----------|-----------|----------|---------|---------|--------|--------|
| **W&S** | 3 | €42k | €360k | €14k | 58% | Core | ✅ |
| **RPO** | 1 | €18k | €96k | €18k | 25% | Grow | 📈 |
| **Interim** | 0 | €0 | €15k | - | 0% | Test | 🔴 |
| **RMA** | - | €12k | €7k | €12k | 17% | Project | 📊 |
| **TOTAAL** | 4 | €72k | €478k | €18k | 100% | €70k | ✅ |

**Insights**:
- W&S = 75% pipeline (core focus) ✅
- RPO = 20% pipeline (growing!) 📈
- Interim = 3% (test fase)
- Focus: W&S + RPO (95% van business)

---

### SECTIE 3: STUCK DEALS (Urgent!)

**12 Deals >14 Dagen Stage 2** (€91k at risk):

| Priority | Deal | Org | Value | Days | Actie Deze Week |
|----------|------|-----|-------|------|-----------------|
| 🔥 1 | Siemens Enschede | Siemens NL | €28k | 21d | LinkedIn + Break-up |
| ⚠️ 2 | Vanderlande Veghel | Vanderlande | €16k | 18d | Break-up email |
| ⚠️ 3 | Gasunie Groningen | Gasunie NL | €15k | 16d | New sourcing |
| ... | [9 more] | ... | €32k | 14-21d | [Actions] |

**Target**: Resolve 5 deze week (move of park)

---

### SECTIE 4: TOP 10 DEALS (By Value)

[LIVE from Pipedrive - 269 deals, top 10 shown]

1. [Deal 1] - €[X] | [Org] | Stage [X]
2. [Deal 2] - €[X] | [Org] | Stage [X]
...
10. [Deal 10] - €[X] | [Org] | Stage [X]

---

### SECTIE 5: WEEK ACTIES (Ma-Vr)

**Ma**: Pipeline review + Stuck #1
**Di**: JobDigger + Stuck #2
**Wo**: Move 3 deals + Stuck #3
**Do**: Close push (ASML + Dow)
**Vr**: Week review + Content

---

### SECTIE 6: QUICK COMMANDS

```bash
# Update dashboard
python3 build-master-dashboard.py

# Weekly reports
python3 generate_weekly_report.py
python3 pipedrive-weekly-dashboard.py
```

═══════════════════════════════════════════════════════════════════════════

ALLES IN 1 SCHERM - Clean, Executive-ready ✅
```

**Dit is beter toch?** 1 dashboard, alles zichtbaar, geen tabs gedoe.

Zal ik dit nu volledig uitbouwen met je live Pipedrive data? 🎯
