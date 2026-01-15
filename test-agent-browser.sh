#!/bin/bash
# Test Agent-Browser met Indeed.nl
# Quick test om te zien of het werkt voor vacancy scraping

echo "🧪 Testing Agent-Browser met Indeed.nl"
echo "========================================"

cd /Users/wouterarts/recruitin-content-intelligence-system/agent-browser

# Check if agent-browser is installed
if ! command -v agent-browser &> /dev/null; then
    echo "⚠️  Agent-browser not found. Installing..."
    pnpm install
    pnpm build
    agent-browser install
fi

echo ""
echo "1️⃣ Opening Indeed.nl - PLC Programmeur Gelderland..."
agent-browser open "https://nl.indeed.com/jobs?q=PLC+Programmeur&l=Gelderland"

echo ""
echo "2️⃣ Waiting for page load..."
agent-browser wait 3000

echo ""
echo "3️⃣ Taking snapshot (accessibility tree)..."
agent-browser snapshot > /tmp/indeed-snapshot.txt
echo "   Snapshot saved: /tmp/indeed-snapshot.txt"

echo ""
echo "4️⃣ Taking screenshot..."
agent-browser screenshot /tmp/indeed-screenshot.png --full
echo "   Screenshot saved: /tmp/indeed-screenshot.png"

echo ""
echo "5️⃣ Getting page title..."
TITLE=$(agent-browser get title)
echo "   Title: $TITLE"

echo ""
echo "6️⃣ Getting vacancy count from snapshot..."
VACANCY_COUNT=$(grep -o '[0-9]\+ vacatures' /tmp/indeed-snapshot.txt | head -1)
echo "   Found: $VACANCY_COUNT"

echo ""
echo "7️⃣ Closing browser..."
agent-browser close

echo ""
echo "✅ Test Complete!"
echo "========================================"
echo "Next steps:"
echo "1. Check snapshot: cat /tmp/indeed-snapshot.txt | head -50"
echo "2. View screenshot: open /tmp/indeed-screenshot.png"
echo "3. If successful, upgrade scrapers to use agent-browser"
