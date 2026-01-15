# META ADS - GO LIVE CHECKLIST

**Account:** act_1443564313411457  
**Pixel:** 238226887541404  
**Budget:** €40/dag = €1,200/maand  
**Start:** Week 3 januari 2026

---

## ✅ PRE-LAUNCH CHECKLIST

### FASE 1: TECHNICAL SETUP (30 min)

**Meta Business Manager:**
- [ ] Pixel installed op kandidatentekort.nl
- [ ] Test pixel firing (PageView event)
- [ ] Custom conversions configured:
  - Lead (form submission)
  - CompleteRegistration (analysis requested)
  - Schedule (calendar booking clicked)
  - Contact (email reply/call initiated)
- [ ] Payment method verified (credit card/bankaansluiting)
- [ ] Billing threshold set (€50 initial)

**Pixel Test Commands:**
```bash
# Test via browser console op kandidatentekort.nl:
fbq('track', 'PageView');
fbq('track', 'ViewContent', {content_name: 'Homepage'});
fbq('track', 'Lead', {content_name: 'Analysis Request'});

# Verify in Events Manager (15 min latency)
```

**Landing Pages:**
- [ ] kandidatentekort.nl live + SSL
- [ ] UTM parameters tested: `?utm_source=meta&utm_medium=cpc&utm_campaign=tofu-awareness&utm_content=ad-1a`
- [ ] Forms werkend (Jotform/Typeform)
- [ ] Thank you pages configured
- [ ] Mobile responsive check

**Tracking Setup:**
- [ ] Google Analytics 4 connected
- [ ] Conversion goals set in GA4
- [ ] GTM container deployed (if used)
- [ ] URL builder spreadsheet ready

---

### FASE 2: CREATIVE ASSETS (2-3 uur)

**Minimaal nodig om te starten:**

**TOFU Assets (Week 1 priority):**
- [ ] Logo Recruitin (PNG, 1080x1080)
- [ ] 5 Carousel cards "5 Signalen PLC Tekort" (1080x1080 each)
  - Card 1: "Overwerkte technici"
  - Card 2: "Vertraagde projecten"
  - Card 3: "Concurrentie pikt mensen"
  - Card 4: "HR frustratie hoog"
  - Card 5: "Kosten exploderen"
- [ ] Video thumbnail "Data-Driven" (1920x1080)
- [ ] Infographic "Top 10 Functies" (1080x1920 vertical)

**MOFU Assets (Week 2):**
- [ ] PDF cover "Salaris Benchmark" preview (1080x1080)
- [ ] Calculator screenshot mockup (1080x1080)
- [ ] Logo grid: ASML, Philips, VDL, Siemens (1080x1080)
- [ ] Case study header "ASML Success" (1200x628)

**BOFU Assets (Week 3):**
- [ ] Calendar widget screenshot (1080x1080)
- [ ] Guarantee badge design (500x500)
- [ ] Team photo Wouter + Sander (1080x1080)
- [ ] Before/after comparison graphic (1080x1080)

**Design Tools:**
- Option A: Canva templates (snelst)
- Option B: Freelance designer (Fiverr €50-100)
- Option C: Leonardo AI MCP (gegenereerd, dan edit in Canva)

**Brand Guidelines:**
- Kleuren: Recruitin blauw (#0066CC) + oranje accent (#FF6B35)
- Font: Inter/Roboto (professional sans-serif)
- Style: Clean, data-focused, tech industry

---

### FASE 3: CAMPAIGN UPLOAD (1 uur)

**Option A: Bulk CSV Upload (Recommended)**
```
File: /home/claude/meta-ads-campaign-structure.csv
Method: Meta Ads Manager → Import → Upload CSV
Status: ✅ READY (20 ads structured)
```

**Import Steps:**
1. Open Ads Manager → https://business.facebook.com/adsmanager
2. Click "Create" → "Import & Export"
3. Upload `meta-ads-campaign-structure.csv`
4. Map columns (auto-detected)
5. Review preview (20 ads)
6. Attach creative assets per ad
7. Confirm & publish

**Option B: Manual Creation**
- Use copy from `/home/claude/meta-ads-copy-library.md`
- Create campaigns 1-by-1 in Ads Manager UI
- Time: 3-4 hours (niet aanbevolen)

**Campaign Structure Preview:**
```
Campaign 1: TOFU - Awareness (€16/dag)
├── Ad Set 1: Mid-Market Manufacturing
│   ├── Ad 1A: 5 Signalen PLC Tekort
│   └── Ad 1B: Data-Driven Video
├── Ad Set 2: Construction Sector
│   ├── Ad 2A: Top 10 Functies
│   └── Ad 2B: Bouw Tekort
├── Ad Set 3: Tech Automation
│   ├── Ad 3A: Automation Fails
│   └── Ad 3B: Thought Leader
└── Ad Set 4: Oil & Gas Energy
    ├── Ad 4A: Oil & Gas Branding
    └── Ad 4B: Renewable Growth

Campaign 2: MOFU - Lead Gen (€14/dag)
├── Ad Set 1: Website Visitors 30d
├── Ad Set 2: Video Engagers 75%
├── Ad Set 3: Lookalike 1%
└── Ad Set 4: Page Activity 90d

Campaign 3: BOFU - Conversions (€10/dag)
├── Ad Set 1: Form Openers
└── Ad Set 2: High Intent 7d
```

---

### FASE 4: ZAPIER AUTOMATION (2 uur)

**Setup volgorde:**

**1. Connect Apps (15 min)**
```
Zapier → My Apps → Add Connection:
- Facebook Lead Ads (account: act_1443564313411457)
- Pipedrive (subdomain: recruitin)
- Resend (API key: re_...)
- Notion (workspace: Recruitin)
- Google Sheets (account: wouter@recruitin.nl)
- Slack (workspace: recruitin-team) [optional]
```

**2. Create Workflows (30 min each)**

**Workflow 1: Lead Capture** (Critical - build first)
```
Trigger: Facebook Lead Ads → New Lead
Filter: Email contains "@" AND Bedrijfsnaam not empty
Actions:
1. Create Pipedrive Deal
2. Send Resend Welcome Email
3. Log to Notion
4. Add row to Google Sheets
5. Create Pipedrive Call Task (+2 days)

Status: LIVE immediately
```

**Workflow 2: Welcome Sequence** (Build second)
```
Trigger: Pipedrive → New Deal (Stage 1, Meta source)
Actions:
1. Delay 1 day → Send Day 1 Email (Analysis)
2. Delay 2 days → Send Day 3 Email (Case Study)
3. Delay 4 days → Send Day 7 Email (ROI)
4. Create Day 14 Call Task

Status: LIVE immediately
```

**Workflow 3: Lead Scoring** (Build third)
```
Trigger: Facebook Lead Ads → New Lead
Actions:
1. Run scoring code (0-100 calculation)
2. Route to owner (Wouter/Sander/Remco)
3. Update Pipedrive custom fields
4. Add tier labels
5. Slack alert if Tier A (score ≥80)

Status: LIVE immediately
```

**Workflow 4: Audience Sync** (Week 2)
```
Trigger: Pipedrive → Deal Updated
Paths based on stage:
- Stage 3 → Add to "Hot Prospects" audience
- Won → Add to "Customers", remove retargeting
- Lost → Add to "Disqualified" exclusion

Status: Test 1 week, LIVE Week 2
```

**Workflow 5: Daily Analytics** (Day 3)
```
Trigger: Schedule → Daily 08:00 CET
Actions:
1. Fetch Pipedrive deals (Meta source, 30d)
2. Calculate metrics (leads, stages, scores, conversion rates)
3. Fetch Meta API (spend, CPM, CTR, CPL)
4. Calculate ROI (spend vs won revenue)
5. Update Google Sheets dashboard
6. Send daily email summary to wouter@recruitin.nl

Status: LIVE Day 3
```

**Testing:**
```bash
# Test lead submission:
1. Submit test form (gebruik je eigen email)
2. Check Pipedrive deal created (binnen 2 min)
3. Verify welcome email received
4. Confirm Notion entry
5. Check Google Sheets row

# Verwijder test data na verificatie
```

---

### FASE 5: ZAPIER CONFIGURATIONS

**Pipedrive Custom Fields toevoegen:**
```
Settings → Data Fields → Deals → Add Custom Field:

1. Lead Source (Dropdown)
   Options: Meta Ads, LinkedIn, Website, Referral, Other

2. Lead Score (Number, 0-100)
   
3. Score Tier (Dropdown)
   Options: A, B, C, D

4. Campaign (Text, 100 chars)

5. Ad Content (Text, 200 chars)

6. Form Name (Text, 100 chars)

7. Submission Date (Date)

8. Nurture Stage (Dropdown)
   Options: Day 0, Day 1, Day 3, Day 7, Day 14, Completed

9. Last Contact (Date)

10. Grootste Uitdaging (Text, 500 chars)
```

**Pipedrive Labels aanmaken:**
```
Settings → Labels → Add Label:

Tiers: Tier A (green), Tier B (yellow), Tier C (orange), Tier D (red)
Campaigns: TOFU, MOFU, BOFU
Sectors: Manufacturing, Construction, Automation, Oil & Gas, Renewable
Priority: High, Medium, Low
```

**Notion Database setup:**
```
Create Database: "Meta Leads Tracker"

Properties:
- Naam (Title)
- Email (Email)
- Bedrijf (Text)
- Functie (Text)
- Campaign (Select: TOFU/MOFU/BOFU)
- Ad Set (Text)
- Ad Name (Text)
- Form (Text)
- Datum (Date)
- Status (Select: New/Contacted/Qualified/Proposal/Won/Lost)
- Lead Score (Number)
- Pipedrive Deal (URL)
```

**Google Sheets setup:**
```
Create Spreadsheet: "Meta Ads Performance Tracker"

Sheet 1: "Lead Log"
Columns: Timestamp, Campaign, Ad Set, Ad Name, Form, Lead Name, 
         Lead Email, Company, Score, Deal ID, Status

Sheet 2: "Daily Metrics"
Columns: Date, Total Leads, New Today, Stage 1-3, Won, Lost,
         TOFU/MOFU/BOFU counts, Avg Score, Tier A %, 
         Conversion rates, Meta Spend, CPM, CTR, CPC, CPL,
         Won Revenue, Pipeline Value, ROI %

Sheet 3: "Campaign Performance"
Columns: Campaign, Ad Set, Ad Name, Impressions, Reach, Clicks,
         CTR, CPC, Spend, Leads, CPL, Conversions, CPA, ROAS
```

---

## 🚀 GO-LIVE PLAN

### WEEK 1: TOFU LAUNCH (€16/dag)

**Dag 1 (Maandag):**
- [ ] 09:00 - Upload 8 TOFU ads via CSV
- [ ] 10:00 - Attach creative assets
- [ ] 11:00 - Review in draft mode
- [ ] 12:00 - Publish campaigns (start 13:00)
- [ ] 14:00 - First performance check (impressions flowing?)
- [ ] 18:00 - End-of-day review (CPM, Reach, CTR)

**Dag 2-3:**
- [ ] Monitor CPM (<€8 target)
- [ ] Check Reach vs Frequency (<2.0)
- [ ] Track CTR (>0.5% target)
- [ ] Verify Pixel events firing
- [ ] Pause any ad with CTR <0.3% after 24h

**Dag 4-7:**
- [ ] Identify winning ads (CTR >0.8%)
- [ ] Scale winners +20% budget
- [ ] Pause losers (<0.3% CTR sustained)
- [ ] Prepare MOFU creative assets
- [ ] Monitor lead quality (if any early leads)

**Week 1 Targets:**
- Impressions: 100k-150k
- Reach: 25k-35k unique
- Clicks: 500-750
- CTR: 0.5-0.8%
- CPM: €6-8
- Spend: ~€112 (€16/dag × 7)

---

### WEEK 2: ADD MOFU (€14/dag) = Total €30/dag

**Dag 8 (Maandag):**
- [ ] Review TOFU Week 1 data
- [ ] Upload 8 MOFU ads
- [ ] Set up retargeting audiences:
  - Website Visitors 30d
  - Video Engagers 75%
  - Page Activity 90d
- [ ] Launch MOFU campaigns (start 13:00)
- [ ] Total budget now €30/dag

**Dag 9-14:**
- [ ] Monitor MOFU CPL (<€15 target)
- [ ] Track form open rate (>40%)
- [ ] Track form completion (>60%)
- [ ] First qualified leads expected
- [ ] Test welcome sequence (Day 1/3 emails)
- [ ] Optimize TOFU based on Week 1 data

**Week 2 Targets:**
- Total Spend: ~€210 cumulative
- MOFU Leads: 10-15 expected
- MOFU CPL: €10-15
- Form completion: >60%
- Zapier workflows running smoothly

---

### WEEK 3: ADD BOFU (€10/dag) = Total €40/dag

**Dag 15:**
- [ ] Upload 4 BOFU ads
- [ ] Set up high-intent audiences:
  - Lead form openers (not submitted)
  - Website 7d + 2+ pages
- [ ] Launch BOFU campaigns
- [ ] Full budget active (€40/dag)

**Dag 16-21:**
- [ ] Monitor Cost/Meeting (<€100)
- [ ] Track booking rate from BOFU ads
- [ ] Optimize entire funnel end-to-end
- [ ] A/B test implementation (start Test 1-2)
- [ ] Scale best performers

**Week 3 Targets:**
- Total Spend: ~€480 cumulative
- Total Leads: 30-40
- Qualified Leads: 8-10
- Meetings Booked: 3-4
- First deal proposals expected

---

### WEEK 4: OPTIMIZATION

**Focus Areas:**
1. **Scale Winners**
   - Identify top 3 ads by CTR
   - Increase budget +50% on winners
   - Create variations of winning concepts

2. **Pause Losers**
   - Ad with CPL >€30 for 3+ days → pause
   - Ad with CTR <0.3% sustained → pause
   - Form with <40% completion → redesign

3. **A/B Testing**
   - Run Test 1: Urgency vs Value (MOFU)
   - Run Test 2: Direct vs Soft CTA (BOFU)
   - Measure: 7-day window, >50 leads per variant

4. **Audience Refinement**
   - Create Lookalike 1% from qualified leads
   - Exclude converters from TOFU/MOFU
   - Add job title targeting if performing well

5. **Creative Refresh**
   - New carousel for best-performing audience
   - Video ad (if static performing well)
   - User-generated content style test

---

## 📊 SUCCESS METRICS

### WEEK 1 (TOFU Only):
- ✅ Campaigns live without errors
- ✅ CPM <€8
- ✅ CTR >0.5%
- ✅ Pixel firing correctly
- ✅ Spend ~€112

### WEEK 2 (TOFU + MOFU):
- ✅ 10-15 leads generated
- ✅ CPL <€15
- ✅ Zapier workflows functioning
- ✅ First welcome emails sent
- ✅ Spend ~€210 cumulative

### WEEK 3 (Full Funnel):
- ✅ 30-40 total leads
- ✅ 8-10 qualified leads
- ✅ 3-4 meetings booked
- ✅ Cost/Meeting <€120
- ✅ Spend ~€480 cumulative

### MONTH 1 (Day 30):
- ✅ 80-120 total leads
- ✅ 20-30 qualified leads (25%)
- ✅ 8-12 meetings (33%)
- ✅ 2-4 deals won (25-33%)
- ✅ ROI positive (€9k revenue vs €1.2k spend)

---

## 🚨 RED FLAGS - PAUSE IF:

**Week 1:**
- CPM consistently >€12 (audience too narrow)
- CTR <0.3% after 48h (creative issue)
- Frequency >3.0 (audience exhaustion)
- Zero website traffic from ads (pixel broken)

**Week 2:**
- CPL >€30 for 3+ consecutive days
- Form open rate <25% (landing page issue)
- Form completion <40% (too many fields)
- Zero qualified leads after 50 total (ICP mismatch)

**Week 3:**
- Cost/Meeting >€150 (funnel broken)
- Show-up rate <50% (lead quality issue)
- Zero deals after 100 leads (offer mismatch)
- CPL increasing week-over-week (fatigue)

**Action:** Pause campaign, diagnose issue, fix, relaunch

---

## 🎯 QUICK WINS CHECKLIST

**Day 1 priorities:**
- [ ] CSV upload (20 ads)
- [ ] Zapier Workflow 1 live (Lead Capture)
- [ ] Pixel verified working
- [ ] Campaigns published

**Day 2-7 priorities:**
- [ ] Monitor daily (15 min morning check)
- [ ] Zapier Workflow 2 live (Welcome Sequence)
- [ ] Zapier Workflow 3 live (Lead Scoring)
- [ ] First creative optimizations

**Day 8-14 priorities:**
- [ ] MOFU launch
- [ ] First leads → meetings conversions
- [ ] Welcome sequence refinement
- [ ] Prepare BOFU assets

**Day 15-30 priorities:**
- [ ] Full funnel optimization
- [ ] A/B testing execution
- [ ] Scale winning campaigns
- [ ] First deals closed

---

**SAMENVATTING:**

✅ **Technical:** Pixel + Forms + UTM tracking  
✅ **Creative:** Minimaal 12 assets (TOFU priority)  
✅ **Campaign:** CSV klaar, upload in 1 uur  
✅ **Automation:** 5 Zapier workflows, 2-3 uur setup  
✅ **Launch:** Phased (Week 1 TOFU → Week 2 MOFU → Week 3 BOFU)  

**Total Setup Time:** 6-8 uur  
**Total Investment:** €1,200 eerste maand  
**Expected ROI:** 7.5x (€9k revenue)

**Ready to launch?**
