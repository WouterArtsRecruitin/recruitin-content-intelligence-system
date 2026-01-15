# 🎯 ICP SCORING - Pipedrive Automation

**Gevonden**: Complete ICP scoring systeem voor Pipedrive
**Status**: Ready to implement
**ROI**: Automatic lead qualification = €15,000/jaar time savings

---

## 📦 WAT JE HEBT

**3 Files in icp/ folder**:

### 1. ICP_Scoring_Implementation_Guide.xlsx ✅
**Wat**: Excel guide met complete uitleg
**Bevat**: 
- ICP criteria (7 factors)
- Scoring matrix
- Implementation steps
- Pipedrive field setup

**Status**: Geopend voor review

---

### 2. icp_scoring_zapier.py ✅
**Wat**: Python code voor Zapier "Code by Zapier" step
**Bevat**:
- Complete scoring algorithm
- 7 criteria weighted scoring
- Output: ICP score (0-28.5), Match (Yes/No), Breakdown

**Criteria** (7 factors):
1. **Bedrijfsgrootte** (Weight 2x): 50-200 FTE = ideal, 200-800 = target
2. **Sector** (Weight 1.5x): Oil & Gas, Renewable = perfect | Productie, Constructie = target
3. **Regio** (Weight 1x): Gelderland, Overijssel, Brabant = target
4. **Recruitment Type** (Weight 1.5x): RPO = best, W&S = good
5. **Budget Range** (Weight 2x): €50-100k = ideal
6. **Decision Maker** (Weight 1.5x): Direct hiring manager = best
7. **Urgentie** (Weight 1x): ASAP = high, <4 weeks = medium

**Threshold**: 14.25/28.5 (50%) = ICP Match

---

### 3. zapier_setup_screenshots.md ✅
**Wat**: Step-by-step Zapier setup guide
**Bevat**:
- 9 stappen met screenshots locations
- Exact field mappings
- Filter configurations
- Test procedures

**Use**: Follow dit voor Zapier implementation

---

## 🔄 HOW IT WORKS

```
TRIGGER: Deal updated in Pipedrive
    ↓
FILTER: Only if custom fields filled
    ↓
CODE: Calculate ICP score (Python)
    ↓
UPDATE: Write score back to Pipedrive
    ↓
FILTER: Only low ICP (score <50%)
    ↓
SLACK: Alert voor low ICP deals
    ↓
SHEETS: Log to dashboard (optional)
```

**Result**: Every deal gets ICP score automatic! ✅

---

## 🎯 INTEGRATIE MET JOUW SYSTEEM

### Link Met Lead Quality Scorer Skill

**Claude Code Skill**: `lead-quality-scorer`
- Manual scoring (via Claude command)
- 12-factor model
- 0-100 score

**Zapier ICP Scoring**:
- Automatic scoring (via Pipedrive update)
- 7-factor model
- 0-28.5 score (0-100%)

**Gebruik Beide**:
- **Zapier**: Automatic eerste check (all deals)
- **Claude**: Detailed analyse (A-tier leads only)

**Workflow**:
```
Nieuwe lead → Pipedrive
  ↓
Zapier: Auto ICP score (30 sec)
  ↓
IF >50% → Claude: Detailed scoring (2 min)
  ↓
IF A-tier → Outreach
```

**Time saved**: 15 min/lead → 30 sec automatic

---

## 📋 SETUP CHECKLIST (Later - Als Je Wilt)

### Phase 1: Pipedrive Custom Fields (15 min)
- [ ] Create custom fields (7 velden):
  - Bedrijfsgrootte (FTE)
  - Sector
  - Regio
  - Recruitment Type
  - Budget Range
  - Contact Role
  - Decision Timeline
- [ ] Add to deal detail view

### Phase 2: Zapier Setup (30 min)
- [ ] Create Zap (follow zapier_setup_screenshots.md)
- [ ] Add 9 steps (trigger → code → update → filter → slack)
- [ ] Test met dummy deal
- [ ] Publish

### Phase 3: Integration (15 min)
- [ ] Link met lead-quality-scorer skill
- [ ] Test workflow (Zapier → Claude)
- [ ] Document process

**Total Setup**: 60 minuten (1x)
**ROI**: €15,000/jaar (lead qualification automation)

---

## 💡 VOOR NU - GEBRUIK CLAUDE SKILL

**Je hebt al**: `lead-quality-scorer` skill in Claude Code

**Command**:
```
Score lead:
- Company: [Name], [FTE], [Location]
- Industry: [Sector]
- Role: [Title]
- Budget: [€]
- Contact: [Hiring Manager/HR]
- Timeline: [Weeks]

Output: Score 0-100, Tier A/B/C/D, Next actions
```

**Tijd**: 30 seconden
**Later**: Automatiseer met Zapier (als je wilt)

---

## 📊 ICP FILES IN SYSTEEM

**Locatie**: `/Users/wouterarts/recruitin-content-intelligence-system/icp/`

**Files**:
1. ICP_Scoring_Implementation_Guide.xlsx (Excel guide)
2. icp_scoring_zapier.py (Python code)
3. zapier_setup_screenshots.md (Setup guide)

**Status**: Ready for implementation (optioneel)

**Priority**: Medium (nice to have, niet urgent)

**Advies**: Start met manual Claude scoring, automatiseer later als volume hoog genoeg

---

**Toegevoegd aan systeem!** ✅

*ICP Scoring | Zapier Automation | Optional Enhancement*
