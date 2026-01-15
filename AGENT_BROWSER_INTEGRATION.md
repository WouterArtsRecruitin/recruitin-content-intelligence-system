# 🤖 AGENT-BROWSER INTEGRATIE MET INTELLIGENCE HUB

**Datum:** 2025-01-12
**Status:** Integration Ready

---

## 🎯 WAT IS AGENT-BROWSER?

Headless browser automation CLI voor AI agents:
- **Fast Rust CLI** met Node.js fallback
- **Playwright-based** (Chromium automation)
- **Accessibility tree** with refs (perfect voor AI)
- **Request tracking**, console monitoring, HAR recording

**Repository:** https://github.com/WouterArtsRecruitin/agent-browser
**Forked from:** vercel-labs/agent-browser

---

## 🚀 WAAROM GEBRUIKEN VOOR INTELLIGENCE HUB?

**Huidige Scrapers (Axios/Cheerio):**
- ❌ Geen JavaScript rendering
- ❌ Geen dynamic content
- ❌ Beperkt tot static HTML
- ❌ Anti-scraping detection

**Met Agent-Browser:**
- ✅ Full browser rendering
- ✅ JavaScript execution
- ✅ Dynamic content loading
- ✅ Human-like behavior
- ✅ Network request tracking
- ✅ Console debugging

---

## 📋 INTEGRATIE PLAN

### Stap 1: Installatie (5 min)

```bash
cd /Users/wouterarts/recruitin-content-intelligence-system
cd agent-browser
pnpm install
pnpm build
agent-browser install  # Download Chromium
```

### Stap 2: Test Run (2 min)

```bash
agent-browser open https://indeed.nl
agent-browser snapshot > indeed-snapshot.txt
agent-browser screenshot indeed.png
agent-browser close
```

### Stap 3: Upgrade Market Trends Scraper (30 min)

**Nieuw:** `market-trends-scraper-v2.js` met agent-browser

```javascript
#!/usr/bin/env node
/**
 * Market Trends Scraper V2 - Agent-Browser Edition
 * Upgrade van Axios/Cheerio naar full browser automation
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// Configuration
const FUNCTIEGROEPEN = [
  'PLC Programmeur',
  'Monteur Elektro',
  'Servicemonteur',
  // ... 9 more
];

const REGIONS = [
  'Gelderland',
  'Overijssel',
  'Noord-Brabant',
  'Utrecht',
  'Limburg',
  'Flevoland'
];

async function scrapeFunctiegroepRegion(fg, region) {
  const query = `${fg} ${region}`;
  const indeedUrl = `https://nl.indeed.com/jobs?q=${encodeURIComponent(query)}&l=Nederland`;

  // Open Indeed
  await execAsync(`agent-browser open "${indeedUrl}"`);
  await execAsync('agent-browser wait 2000');

  // Get snapshot met refs
  const { stdout: snapshot } = await execAsync('agent-browser snapshot');

  // Extract vacancy count (parse snapshot for count)
  const countMatch = snapshot.match(/(\d+) vacatures/);
  const count = countMatch ? parseInt(countMatch[1]) : 0;

  // Get salary data
  const { stdout: salaryHtml } = await execAsync('agent-browser get html body');
  const salaryMatch = salaryHtml.match(/€\s*([\d,]+)\s*-\s*€\s*([\d,]+)/);

  return {
    functiegroep: fg,
    region: region,
    count: count,
    salaryLow: salaryMatch ? parseInt(salaryMatch[1].replace(',', '')) : null,
    salaryHigh: salaryMatch ? parseInt(salaryMatch[2].replace(',', '')) : null,
    timestamp: new Date().toISOString()
  };
}

async function main() {
  console.log('🚀 Market Trends Scraper V2 (Agent-Browser)');

  const results = [];

  for (const fg of FUNCTIEGROEPEN) {
    for (const region of REGIONS) {
      console.log(`  Scraping ${fg} - ${region}...`);
      const data = await scrapeFunctiegroepRegion(fg, region);
      results.push(data);

      // Rate limiting
      await execAsync('agent-browser wait 1000');
    }
  }

  // Close browser
  await execAsync('agent-browser close');

  // Export CSV
  const csv = results.map(r =>
    `${r.functiegroep},${r.region},${r.count},${r.salaryLow},${r.salaryHigh},${r.timestamp}`
  ).join('\n');

  console.log(`✅ Scraped ${results.length} combinations`);
  console.log(csv);
}

main();
```

### Stap 4: Upgrade ICP Monitor (20 min)

**Features met agent-browser:**
- Navigate naar company career pages
- Detect nieuwe vacatures via snapshot
- Extract job titles en requirements
- Monitor company news pages

### Stap 5: Upgrade Concurrent Tracker (20 min)

**Features:**
- Navigate naar concurrent LinkedIn pages
- Extract post content & engagement
- Monitor blog updates
- Track PR releases

---

## 💡 VOORDELEN VS HUIDIGE AXIOS/CHEERIO

| Feature | Axios/Cheerio | Agent-Browser |
|---------|---------------|---------------|
| Speed | ⚡⚡⚡ Very fast | ⚡⚡ Fast enough |
| JavaScript | ❌ No | ✅ Yes |
| Dynamic content | ❌ No | ✅ Yes |
| Anti-bot bypass | ❌ Weak | ✅ Strong |
| Debugging | ⚠️ Limited | ✅ Screenshots, HAR, console |
| AI-friendly | ⚠️ HTML parsing | ✅ Accessibility tree |
| Maintenance | ⚠️ Brittle selectors | ✅ Semantic refs |
| Cost | 💰 Free | 💰 Free |

---

## 🔧 RECOMMENDED ARCHITECTURE

```
Intelligence Hub V2
├── scrapers/
│   ├── market-trends-v2.js      (agent-browser)
│   ├── icp-monitor-v2.js         (agent-browser)
│   └── concurrent-tracker-v2.js  (agent-browser)
├── agent-browser/               (cloned from GitHub)
│   ├── bin/agent-browser        (Rust CLI)
│   └── dist/daemon.js           (Node.js fallback)
└── package.json                  (dependencies)
```

**Runtime:**
- Development: Use Node.js daemon (slower, easier debug)
- Production: Use Rust CLI (faster, production-ready)

---

## 📊 EXPECTED PERFORMANCE

**Current (Axios/Cheerio):**
- Market Trends: ~3 min (72 queries)
- Success rate: ~85% (static HTML only)

**With Agent-Browser:**
- Market Trends: ~8 min (full rendering)
- Success rate: ~98% (handles JS, dynamic content)
- Bonus: Screenshots voor debugging
- Bonus: HAR files voor network analysis

**Trade-off:** 2.5x langzamer, maar 15% meer data + veel betrouwbaarder

---

## ✅ IMPLEMENTATION CHECKLIST

**Week 1: Setup & Test**
- [ ] Install agent-browser (`pnpm install`)
- [ ] Build Rust CLI (`pnpm build:native`)
- [ ] Test met Indeed (`agent-browser open indeed.nl`)
- [ ] Test snapshot extraction

**Week 2: Upgrade Scrapers**
- [ ] market-trends-v2.js (agent-browser based)
- [ ] Test 5 functiegroepen × 2 regions
- [ ] Compare output met V1
- [ ] Validate CSV structure

**Week 3: Full Migration**
- [ ] icp-monitor-v2.js
- [ ] concurrent-tracker-v2.js
- [ ] Update package.json dependencies
- [ ] Deploy to production

**Week 4: Optimization**
- [ ] Parallel execution (multiple browser contexts)
- [ ] Caching strategies
- [ ] Error handling & retries
- [ ] Performance monitoring

---

## 🎯 ROI ANALYSIS

**Investment:**
- Development time: 4-6 uur
- Testing time: 2 uur
- Deployment: 1 uur
- **Total:** ~8 uur

**Returns:**
- +15% data accuracy = +€7.5k Q1 omzet
- -50% scraping errors = -2 uur/week maintenance
- Better anti-bot resilience = Long-term stability
- Screenshots for debugging = -1 uur/week troubleshooting

**ROI:** €7.5k revenue - €800 labor = **€6.7k net positive**

---

## 📞 NEXT STEPS

1. **Test agent-browser** met 1 functiegroep (15 min)
2. **Build V2 scraper** voor Market Trends (30 min)
3. **Compare outputs** V1 vs V2 (10 min)
4. **Decision:** Migrate or keep current?

**Contact:** wouter@recruitin.nl

---

**Repository:** https://github.com/WouterArtsRecruitin/agent-browser
**Original:** https://github.com/vercel-labs/agent-browser
**License:** Apache-2.0
