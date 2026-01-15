# 🚀 RECRUITIN INTELLIGENCE HUB - COMPLETE SETUP GUIDE
**Spreadsheet:** https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit

---

## ✅ STAP 1: IMPORT ALLE CSV DATA (5 MINUTEN)

### 📊 Market Trends
1. Open sheet "Market Trends"
2. Select cell A2
3. **Copy-paste** alle data uit `/home/claude/market_trends_data.csv`
4. ✅ Result: 10 rows met complete data

### 👥 ICP Activity
1. Open sheet "ICP Activity"
2. Select cell A2
3. **Copy-paste** alle data uit `/home/claude/icp_activity_data.csv`
4. ✅ Result: 7 rows met high-value prospects

### 👻 Ghosting Patterns
1. Open sheet "Ghosting Patterns"
2. Select cell A2
3. **Copy-paste** alle data uit `/home/claude/ghosting_patterns_data.csv`
4. ✅ Result: 6 rows met pipeline patterns

### 📰 Sector News
1. Open sheet "Sector News"
2. Select cell A2
3. **Copy-paste** alle data uit `/home/claude/sector_news_data.csv`
4. ✅ Result: 7 rows met industry updates

### 🔍 Concurrent Activity
1. Open sheet "Concurrent Activity"
2. Select cell A2
3. **Copy-paste** alle data uit `/home/claude/concurrent_activity_data.csv`
4. ✅ Result: 7 rows met competitor intelligence

### 📧 Newsletter Monthly Data
1. Open sheet "Newsletter Monthly Data"
2. Select cell A2
3. **Copy-paste** alle data uit `/home/claude/newsletter_monthly_data.csv`
4. ✅ Result: 1 row met monthly aggregation

### 📈 Dashboard
1. Open sheet "Dashboard"
2. Select cell A2
3. **Copy-paste** alle data uit `/home/claude/dashboard_data.csv`
4. ✅ Result: 10 KPI metrics

---

## ✅ STAP 2: DATA VALIDATION TOEVOEGEN (5 MINUTEN)

### Market Trends - Kolom C (Functiegroep)
1. Select range **C2:C1000**
2. Data → Data validation
3. Criteria: **List from a range** → Type manually:
```
Werkvoorbereider Elektro, Werkvoorbereider Bouw, Calculator Bouw, Constructeur, Servicemonteur, Monteur Elektro, PLC Programmeur, Projectleider Elektro, Projectleider Installatie, Allround Monteur, Mechatronicus, Tekenaar Constructeur
```
4. ✅ Dropdown active

### Market Trends - Kolom D (Region)
1. Select range **D2:D1000**
2. Data → Data validation
3. Criteria: **List of items** → Type:
```
Gelderland, Overijssel, Noord-Brabant, Utrecht, Limburg, Flevoland
```
4. ✅ Dropdown active

### ICP Activity - Kolom C (Industry Sector)
1. Select range **C2:C1000**
2. Data → Data validation
3. Criteria: **List of items** → Type:
```
Oil & Gas, Construction, Manufacturing, Automation, Renewable Energy, Metal, Installation, Offshore, Process Industry, Machinebouw, Utilities, Petrochemie
```
4. ✅ Dropdown active

### ICP Activity - Kolom D (Region)
1. Select range **D2:D1000**
2. Data → Data validation
3. Same as Market Trends Region dropdown

### ICP Activity - Kolom I (Match Score)
1. Select range **I2:I1000**
2. Data → Data validation
3. Criteria: **Number** → Between 1 and 10
4. ✅ Score validation active

### Sector News - Kolom E (Sector Tag)
1. Select range **E2:E1000**
2. Data → Data validation
3. Same as ICP Activity Industry Sector dropdown

### Sector News - Kolom F (Relevance Score)
1. Select range **F2:F1000**
2. Data → Data validation
3. Criteria: **Number** → Between 1 and 10

### Sector News - Kolom G (Angle)
1. Select range **G2:G1000**
2. Data → Data validation
3. Criteria: **List of items** → Type:
```
Trend, Innovation, Challenge, Policy, Market Shift, Technology, Skills Gap
```

### Concurrent Activity - Kolom B (Concurrent Name)
1. Select range **B2:B1000**
2. Data → Data validation
3. Criteria: **List of items** → Type:
```
Brunel Nederland, Yacht, YER, Synsel Techniek, RGF Staffing, Time to Hire, ENHR, RecruitmentNow, Profound, Randstad Sourceright, Manpower RPO, Vanujska, Continu, FYGI, Ede
```

### Concurrent Activity - Kolom C (Tier)
1. Select range **C2:C1000**
2. Data → Data validation
3. Criteria: **List of items** → Type:
```
1, 2
```

### Newsletter - Kolom C (Status)
1. Select range **C2:C1000**
2. Data → Data validation
3. Criteria: **List of items** → Type:
```
Draft, Ready to Send, Sent, Archived
```

---

## ✅ STAP 3: CONDITIONAL FORMATTING (3 MINUTEN)

### Market Trends - Priority Colors (Kolom N)
1. Select range **N2:N1000**
2. Format → Conditional formatting
3. Add 3 rules:
   - **HIGH**: Text is exactly "HIGH" → Background: #FF6B6B (red)
   - **MEDIUM**: Text is exactly "MEDIUM" → Background: #FFA500 (orange)
   - **LOW**: Text is exactly "LOW" → Background: #90EE90 (green)

### ICP Activity - Priority Colors (Kolom J)
1. Select range **J2:J1000**
2. Same color rules as Market Trends

### Ghosting Patterns - Reportable Flag (Kolom I)
1. Select range **I2:I1000**
2. Format → Conditional formatting
3. Rule: **TRUE** → Background: #FFFF99 (yellow)

### Sector News - Content Opportunity (Kolom H)
1. Select range **H2:H1000**
2. Same as Ghosting Patterns (TRUE = yellow)

### Concurrent Activity - Content Opportunity (Kolom J)
1. Select range **J2:J1000**
2. Same yellow highlighting for TRUE

---

## ✅ STAP 4: HEADER FORMATTING (2 MINUTEN)

### All Sheets
1. Select row 1 (header row)
2. Format → Background color: **#0066CC** (blue)
3. Format → Text color: **White**
4. Format → Bold
5. View → Freeze → 1 row

**Apply to:** Market Trends, ICP Activity, Ghosting Patterns, Sector News, Concurrent Activity, Newsletter, Dashboard, README

---

## ✅ STAP 5: FORMULAS UPDATEN (OPTIONAL - 5 MINUTEN)

**Market Trends** formulas zijn al ingevuld als sample data. 

Als je **dynamische formulas** wilt voor nieuwe rows:

### Week Number Auto-Calculate (Kolom B)
- B2: `=WEEKNUM(A2)`
- Drag down voor alle rows

### Change % Auto-Calculate (Kolom H)
- H2: `=IFERROR(IF(G2=0,0,(F2-G2)/G2*100),0)`
- Drag down

### Priority Auto-Calculate (Kolom N)
- N2: `=IF(OR(H2>15,F2>100),"HIGH",IF(OR(H2>8,F2>50),"MEDIUM","LOW"))`
- Drag down

**ICP Activity** kolom J (Priority):
- J2: `=IF(AND(I2>=7,E2>0),"HIGH",IF(AND(I2>=5,E2>0),"MEDIUM","LOW"))`

**Dashboard** formulas (replace static values):
- B2 (Total Vacatures): `=SUMIF('Market Trends'!B:B,WEEKNUM(TODAY()),'Market Trends'!F:F)`
- B3 (Change %): `=(B2-SUMIF('Market Trends'!B:B,WEEKNUM(TODAY())-1,'Market Trends'!F:F))/SUMIF('Market Trends'!B:B,WEEKNUM(TODAY())-1,'Market Trends'!F:F)*100`
- B4 (HIGH Priority): `=COUNTIF('Market Trends'!N:N,"HIGH")`
- B5 (Hottest FG): `=INDEX('Market Trends'!C:C,MATCH(MAX('Market Trends'!F:F),'Market Trends'!F:F,0))`

---

## ✅ STAP 6: NUMBER FORMATTING (2 MINUTEN)

### Market Trends
- Kolom H (Change %): Format → Number → Custom: `0.00"%"`
- Kolom I, J, K (Salary): Format → Number → Currency: `€#,##0`

### ICP Activity
- Kolom E (New Vacancies): Format → Number → No decimals

### Concurrent Activity
- Kolom F (Vacature Count): Format → Number → No decimals
- Kolom G (Change %): Format → Number → Custom: `0.00"%"`
- Kolom I (Activity Score): Format → Number → No decimals

### Dashboard
- B3 (Change %): Format → Number → Custom: `0.00"%"`
- B7, B10 (Salary/Score): Format → Number → `#,##0`

---

## ✅ VERIFICATION CHECKLIST

- [ ] All 8 sheets have sample data
- [ ] Market Trends: 10 rows × 14 columns
- [ ] ICP Activity: 7 rows × 10 columns
- [ ] Ghosting Patterns: 6 rows × 9 columns
- [ ] Sector News: 7 rows × 8 columns
- [ ] Concurrent Activity: 7 rows × 11 columns
- [ ] Newsletter: 1 row × 32 columns
- [ ] Dashboard: 10 metrics
- [ ] README: 14 info rows
- [ ] All dropdowns working (test by clicking cell)
- [ ] Conditional formatting shows colors
- [ ] Headers are blue/white/bold
- [ ] Row 1 is frozen on all sheets

---

## 🚀 NEXT STEPS: AUTOMATION

### Week 2: Agent-Browser Scripts
1. `market-trends-scraper.js` - Indeed + Monsterboard scraping
2. `icp-monitor.js` - Company news aggregation
3. `concurrent-tracker.js` - Competitor blog/PR monitoring

### Week 2: Zapier Workflows
1. **Zap 1:** Market Trends HIGH → Claude content gen → Notion
2. **Zap 2:** ICP Activity HIGH → Claude analysis → Notion
3. **Zap 6:** Concurrent Opportunity → Claude response → Notion
4. **Zap Newsletter:** Monthly trigger → Claude aggregation → Resend

---

## 📞 SUPPORT

Issues? Contact: wouter@recruitin.nl
Spreadsheet: https://docs.google.com/spreadsheets/d/14pX6dV6-5KLHYPuU1YsZSzu5SLHVbUxU78YQvIIRV_c/edit

**Estimated total setup time:** 15-20 minuten
**Status:** ✅ READY TO IMPORT!
