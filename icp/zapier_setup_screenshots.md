# ZAPIER SETUP - SCREENSHOT GUIDE
## ICP Scoring Automation voor Recruitin

---

## 📸 STAP-VOOR-STAP MET SCREENSHOTS

### **STAP 1: CREATE ZAP**

1. Ga naar https://zapier.com/app/zaps
2. Klik **"Create Zap"** (oranje knop rechtsboven)
3. Naam: `Pipedrive ICP Auto-Scoring`

---

### **STAP 2: TRIGGER SETUP**

**App selecteren:**
- Zoek: `Pipedrive`
- Event: `Updated Deal`
- Klik **Continue**

**Account verbinden:**
- Klik **Sign in to Pipedrive**
- Log in met je Pipedrive account
- Authorize Zapier

**Trigger configureren:**
- Pipeline: `Sales Pipeline` (of jouw pipeline naam)
- Stage: `Leave blank` (alle stages)
- Test: Klik **Test trigger**
- Resultaat: Je ziet een lijst met recente deals
- Selecteer een test deal → **Continue**

**Screenshot locatie:** 
- Trigger app selector
- Pipedrive authorization screen
- Test trigger results

---

### **STAP 3: FILTER (OPTIONEEL)**

**App selecteren:**
- Klik **+** onder trigger step
- Zoek: `Filter by Zapier`
- Klik **Filter**

**Filter instellen:**
```
(Filter) Only continue if...

Condition 1:
- Field: Custom Fields Bedrijfsgrootte (FTE)
- Condition: (Number) Is not empty

AND

Condition 2:
- Field: Custom Fields Sector
- Condition: (Text) Is not empty
```

**Screenshot locatie:**
- Filter setup screen
- Condition configuration

---

### **STAP 4: CODE BY ZAPIER**

**App selecteren:**
- Klik **+** onder filter
- Zoek: `Code by Zapier`
- Action: `Run Python`

**Code configureren:**

**Input Data** tab:
```json
{
  "bedrijfsgrootte_fte": "{{Step 1: Custom Fields Bedrijfsgrootte (FTE)}}",
  "icp_sector": "{{Step 1: Custom Fields Sector}}",
  "icp_regio": "{{Step 1: Custom Fields Regio}}",
  "recruitment_type": "{{Step 1: Custom Fields Recruitment Type}}",
  "budget_range": "{{Step 1: Custom Fields Budget Range}}",
  "decision_maker_role": "{{Step 1: Custom Fields Contact Role}}",
  "urgentie": "{{Step 1: Custom Fields Decision Timeline}}"
}
```

**Code** tab:
- Plak de VOLLEDIGE code uit `icp_scoring_zapier.py`
- Klik **Test & Continue**

**Expected output:**
```json
{
  "icp_score": 18.5,
  "icp_match": "Yes",
  "score_percentage": 64.9,
  "breakdown_text": "bedrijfsgrootte: 2/3..."
}
```

**Screenshot locatie:**
- Input Data configuration
- Code editor with Python script
- Test results showing output

---

### **STAP 5: UPDATE PIPEDRIVE DEAL**

**App selecteren:**
- Klik **+**
- Zoek: `Pipedrive`
- Action: `Update Deal`

**Deal configureren:**
```
Deal ID: {{Step 1: ID}}

Fields to update:
- ICP Score: {{Step 3: icp_score}}
- ICP Match: {{Step 3: icp_match}}
- ICP Score Percentage: {{Step 3: score_percentage}}
```

**Test:**
- Klik **Test & Continue**
- Check in Pipedrive of fields zijn ge-update

**Screenshot locatie:**
- Update Deal configuration
- Field mapping screen
- Test results

---

### **STAP 6: FILTER LOW ICP**

**App selecteren:**
- Klik **+**
- Zoek: `Filter by Zapier`

**Filter instellen:**
```
(Filter) Only continue if...

ICP Match: {{Step 3: icp_match}}
Condition: (Text) Exactly matches
Value: No
```

**Screenshot locatie:**
- Filter configuration for low ICP

---

### **STAP 7: SLACK NOTIFICATION**

**App selecteren:**
- Klik **+**
- Zoek: `Slack`
- Action: `Send Channel Message`

**Slack configureren:**
- Channel: `#sales-alerts` (maak deze aan als die nog niet bestaat)
- Message Text:
```
⚠️ LOW ICP DEAL ALERT

Deal: {{Step 1: Title}}
Company: {{Step 1: Org Name}}
Owner: {{Step 1: Owner Name}}

ICP Score: {{Step 3: icp_score}}/28.5 ({{Step 3: score_percentage}}%)
Status: {{Step 3: icp_match}}

Breakdown:
{{Step 3: breakdown_text}}

➡️ View: {{Step 1: Deal URL}}
```

- Bot Name: `ICP Checker`
- Bot Icon Emoji: `:warning:`

**Test:**
- Klik **Test & Continue**
- Check #sales-alerts in Slack voor message

**Screenshot locatie:**
- Slack channel selector
- Message template editor
- Test notification in Slack

---

### **STAP 8: GOOGLE SHEETS (OPTIONEEL)**

**App selecteren:**
- Klik **+**
- Zoek: `Google Sheets`
- Action: `Create Spreadsheet Row`

**Sheets configureren:**
- Spreadsheet: `Recruitin_KPI_Dashboards_2026`
- Worksheet: `Sales Dashboard Weekly`

**Columns to map:**
```
Deal_ID: {{Step 1: ID}}
Deal_Name: {{Step 1: Title}}
Company: {{Step 1: Org Name}}
ICP_Score: {{Step 3: icp_score}}
ICP_Match: {{Step 3: icp_match}}
Stage: {{Step 1: Stage Name}}
Owner: {{Step 1: Owner Name}}
Created_Date: {{Step 1: Add Time}}
```

**Screenshot locatie:**
- Spreadsheet selector
- Column mapping screen
- Test row in Google Sheets

---

### **STAP 9: PUBLISH ZAP**

1. Klik **Publish** rechtsboven
2. Zap status: **ON** (groene toggle)
3. Test met live deal:
   - Open Pipedrive
   - Update een deal field (bijv. Bedrijfsgrootte)
   - Check of ICP Score automatisch updates
   - Check #sales-alerts voor low ICP notification

**Screenshot locatie:**
- Publish button
- Zap dashboard showing active status

---

## 🎬 VIDEO WALKTHROUGH (OPTIONEEL)

Als je liever een video wilt maken:

1. **Screen recording** met Loom/QuickTime
2. **Toon elke stap** langzaam
3. **Highlight key fields** waar je iets moet invullen
4. **Test aan het eind** met een live deal
5. **Upload** naar YouTube (unlisted) of Loom

Geschatte lengte: 10-15 minuten

---

## ✅ POST-SETUP CHECKLIST

Na publishing:

- [ ] Test met high ICP deal (score >14.25)
- [ ] Test met low ICP deal (score <14.25)
- [ ] Verify Slack notification werkt
- [ ] Check Google Sheets row verschijnt
- [ ] Pipedrive fields tonen correcte scores
- [ ] Filter werkt (geen notif voor high ICP)
- [ ] Zap history toont geen errors

---

## 🐛 TROUBLESHOOTING

**Error: "Custom field not found"**
→ Custom fields moeten EERST in Pipedrive aangemaakt zijn

**Error: "Invalid syntax in Python code"**
→ Check of je de HELE code hebt gekopieerd (inclusief laatste regels)

**Slack notification komt niet door**
→ Check filter condition (ICP Match = "No" exact)

**Score update niet zichtbaar in Pipedrive**
→ Refresh deal page, check field mapping in Step 5

**Zapier task limiet bereikt**
→ Upgrade naar Professional plan of verwijder Step 7 (Sheets)

