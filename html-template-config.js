// Customizable HTML Template Configuration for Recruitment News Reports
// Modify this file to change the HTML output without editing the generators

module.exports = {
  // Color scheme configuration
  colors: {
    headerGradientStart: '#003366',
    headerGradientEnd: '#0066cc',
    primaryText: '#003366',
    accentColor: '#0066cc',
    backgroundColor: '#f5f7fa',
    cardBackground: '#ffffff',
    borderColor: '#e1e4e8',
    textDark: '#555555',
    textMedium: '#666666',
    textLight: '#888888'
  },

  // Typography configuration
  typography: {
    fontFamily: 'Arial, sans-serif',
    headingSize: '28px',
    bodySize: '14px',
    statNumberSize: '32px',
    lineHeight: '1.5'
  },

  // Header configuration
  header: {
    title: '📊 Recruitment & Werkgelegenheid Nieuws',
    subtitle: 'Focus: Uitzendbranche, Vacatures & Arbeidsmarkt',
    showGeneratedTime: true,
    showSubtitle: true
  },

  // Statistics cards configuration
  stats: {
    show: true,
    cards: [
      {
        label: 'Recruitment Artikelen',
        icon: '📊',
        key: 'totalArticles'
      },
      {
        label: 'Bronnen Doorzocht',
        icon: '🔍',
        key: 'totalQueries'
      },
      {
        label: 'Relevante Bronnen',
        icon: '✅',
        key: 'relevantSources'
      }
    ]
  },

  // Article display configuration
  articles: {
    showDescriptions: true,
    showSourceUrl: true,
    emptyStateMessage: 'Geen artikelen gevonden'
  },

  // Layout configuration
  layout: {
    maxWidth: '1200px',
    containerPadding: '20px',
    cardBorderRadius: '8px',
    cardShadow: '0 2px 4px rgba(0,0,0,0.1)',
    gridColumns: 'repeat(auto-fit, minmax(200px, 1fr))'
  },

  // Footer configuration
  footer: {
    showGeneratedAt: true,
    customText: 'Powered by Brave Search API & Recruitment Intelligence System'
  }
};
