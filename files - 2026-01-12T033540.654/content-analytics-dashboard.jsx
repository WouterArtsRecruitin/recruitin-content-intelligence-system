import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, TrendingDown, Users, Eye, MessageSquare, Heart, Share2, Bookmark, Target, Zap } from 'lucide-react';

// Demo data - replace with actual Notion data
const weeklyData = [
  { week: 'W1', engagement: 3.2, impressions: 4200, followers: 12 },
  { week: 'W2', engagement: 4.1, impressions: 5100, followers: 18 },
  { week: 'W3', engagement: 3.8, impressions: 4800, followers: 15 },
  { week: 'W4', engagement: 5.2, impressions: 6200, followers: 24 },
  { week: 'W5', engagement: 4.5, impressions: 5500, followers: 20 },
  { week: 'W6', engagement: 5.8, impressions: 7100, followers: 28 },
];

const angleData = [
  { name: 'Contrarian', posts: 8, avgEngagement: 5.4, color: '#ef4444' },
  { name: 'Data Story', posts: 6, avgEngagement: 4.2, color: '#3b82f6' },
  { name: 'How-To', posts: 5, avgEngagement: 3.8, color: '#22c55e' },
  { name: 'Behind-Scenes', posts: 4, avgEngagement: 4.8, color: '#a855f7' },
];

const platformData = [
  { name: 'Wouter Personal', posts: 15, reach: 42000, engagement: 4.8 },
  { name: 'Recruitin Company', posts: 8, reach: 18000, engagement: 3.2 },
];

const topPosts = [
  { 
    title: '"Culture fit" is de luiste afwijzing', 
    date: '2026-01-08', 
    tier: 'A',
    engagement: 6.2,
    impressions: 8400,
    comments: 24,
    sentiment: 78,
    angle: 'Contrarian',
    platform: 'Wouter'
  },
  { 
    title: '47 vacatures in 90 dagen - onze data', 
    date: '2026-01-05', 
    tier: 'A',
    engagement: 5.8,
    impressions: 7200,
    comments: 19,
    sentiment: 82,
    angle: 'Data Story',
    platform: 'Wouter'
  },
  { 
    title: '5 dingen die technisch talent wil horen', 
    date: '2026-01-03', 
    tier: 'B',
    engagement: 4.5,
    impressions: 5600,
    comments: 12,
    sentiment: 71,
    angle: 'How-To',
    platform: 'Recruitin'
  },
];

const timingData = [
  { day: 'Ma', time08: 3.2, time12: 2.8, time17: 2.1 },
  { day: 'Di', time08: 4.8, time12: 3.5, time17: 2.9 },
  { day: 'Wo', time08: 3.9, time12: 5.2, time17: 3.1 },
  { day: 'Do', time08: 4.5, time12: 3.8, time17: 2.6 },
  { day: 'Vr', time08: 3.1, time12: 4.1, time17: 2.4 },
];

const COLORS = ['#ef4444', '#3b82f6', '#22c55e', '#a855f7'];

export default function ContentAnalyticsDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  
  const stats = {
    totalPosts: 23,
    avgEngagement: 4.6,
    totalImpressions: 45200,
    followersGained: 117,
    aTierPosts: 5,
    bestAngle: 'Contrarian',
    bestTime: 'Di 08:00',
  };

  const getTierColor = (tier) => {
    switch(tier) {
      case 'A': return 'bg-green-500';
      case 'B': return 'bg-blue-500';
      case 'C': return 'bg-yellow-500';
      case 'D': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">📊 Content Intelligence Dashboard</h1>
        <p className="text-gray-400">Recruitin B.V. | Last updated: {new Date().toLocaleDateString('nl-NL')}</p>
      </div>

      {/* Navigation Tabs */}
      <div className="flex gap-2 mb-6 border-b border-gray-700 pb-4">
        {['overview', 'performance', 'timing', 'experiments'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg transition-colors ${
              activeTab === tab 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {activeTab === 'overview' && (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
              <div className="flex items-center gap-2 text-gray-400 mb-2">
                <Target className="w-4 h-4" />
                <span className="text-sm">Posts This Month</span>
              </div>
              <div className="text-3xl font-bold">{stats.totalPosts}</div>
              <div className="text-green-400 text-sm flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +15% vs last month
              </div>
            </div>

            <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
              <div className="flex items-center gap-2 text-gray-400 mb-2">
                <Zap className="w-4 h-4" />
                <span className="text-sm">Avg Engagement</span>
              </div>
              <div className="text-3xl font-bold">{stats.avgEngagement}%</div>
              <div className="text-green-400 text-sm flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +0.8% vs target
              </div>
            </div>

            <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
              <div className="flex items-center gap-2 text-gray-400 mb-2">
                <Eye className="w-4 h-4" />
                <span className="text-sm">Total Impressions</span>
              </div>
              <div className="text-3xl font-bold">{(stats.totalImpressions/1000).toFixed(1)}K</div>
              <div className="text-green-400 text-sm flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +22% vs last month
              </div>
            </div>

            <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
              <div className="flex items-center gap-2 text-gray-400 mb-2">
                <Users className="w-4 h-4" />
                <span className="text-sm">Followers Gained</span>
              </div>
              <div className="text-3xl font-bold">+{stats.followersGained}</div>
              <div className="text-green-400 text-sm flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> Above 100 target
              </div>
            </div>
          </div>

          {/* Charts Row */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            {/* Engagement Trend */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h3 className="text-lg font-semibold mb-4">📈 Engagement Trend (6 Weeks)</h3>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={weeklyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="week" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Line type="monotone" dataKey="engagement" stroke="#3b82f6" strokeWidth={2} dot={{ fill: '#3b82f6' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Performance by Angle */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h3 className="text-lg font-semibold mb-4">🎯 Performance by Angle</h3>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={angleData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Bar dataKey="avgEngagement" fill="#3b82f6">
                    {angleData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Top Performers */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-8">
            <h3 className="text-lg font-semibold mb-4">🏆 Top Performers (A-Tier Posts)</h3>
            <div className="space-y-4">
              {topPosts.map((post, i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-gray-700/50 rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className={`w-8 h-8 ${getTierColor(post.tier)} rounded-full flex items-center justify-center font-bold text-sm`}>
                      {post.tier}
                    </div>
                    <div>
                      <div className="font-medium">{post.title}</div>
                      <div className="text-sm text-gray-400">{post.date} • {post.platform} • {post.angle}</div>
                    </div>
                  </div>
                  <div className="flex gap-6 text-sm">
                    <div className="text-center">
                      <div className="text-gray-400">Engagement</div>
                      <div className="font-bold text-green-400">{post.engagement}%</div>
                    </div>
                    <div className="text-center">
                      <div className="text-gray-400">Comments</div>
                      <div className="font-bold">{post.comments}</div>
                    </div>
                    <div className="text-center">
                      <div className="text-gray-400">Sentiment</div>
                      <div className="font-bold text-blue-400">{post.sentiment}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Insights */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-green-900/50 to-green-800/30 rounded-xl p-4 border border-green-700/50">
              <h4 className="font-semibold text-green-400 mb-2">✅ What Works</h4>
              <ul className="text-sm text-gray-300 space-y-1">
                <li>• Contrarian posts outperform by 32%</li>
                <li>• Tuesday 08:00 is best timing</li>
                <li>• Personal profile 50% more reach</li>
              </ul>
            </div>
            <div className="bg-gradient-to-br from-red-900/50 to-red-800/30 rounded-xl p-4 border border-red-700/50">
              <h4 className="font-semibold text-red-400 mb-2">❌ What Doesn't</h4>
              <ul className="text-sm text-gray-300 space-y-1">
                <li>• Friday afternoon posts: -40% eng</li>
                <li>• Posts without questions: -25%</li>
                <li>• Too many hashtags (&gt;5): -15%</li>
              </ul>
            </div>
            <div className="bg-gradient-to-br from-blue-900/50 to-blue-800/30 rounded-xl p-4 border border-blue-700/50">
              <h4 className="font-semibold text-blue-400 mb-2">🔬 This Week's Test</h4>
              <ul className="text-sm text-gray-300 space-y-1">
                <li>• Testing: Data vs Story hooks</li>
                <li>• Hypothesis: +20% with data</li>
                <li>• Status: Running (day 3/7)</li>
              </ul>
            </div>
          </div>
        </>
      )}

      {activeTab === 'performance' && (
        <div className="space-y-6">
          {/* Platform Comparison */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold mb-4">📱 Platform Performance</h3>
            <div className="grid md:grid-cols-2 gap-6">
              {platformData.map((platform, i) => (
                <div key={i} className="bg-gray-700/50 rounded-lg p-4">
                  <h4 className="font-semibold mb-4">{platform.name}</h4>
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold">{platform.posts}</div>
                      <div className="text-sm text-gray-400">Posts</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold">{(platform.reach/1000).toFixed(0)}K</div>
                      <div className="text-sm text-gray-400">Reach</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-green-400">{platform.engagement}%</div>
                      <div className="text-sm text-gray-400">Engagement</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Angle Distribution */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold mb-4">🎯 Content Angle Distribution</h3>
            <div className="flex items-center gap-8">
              <ResponsiveContainer width={200} height={200}>
                <PieChart>
                  <Pie
                    data={angleData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    dataKey="posts"
                  >
                    {angleData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="flex-1 space-y-3">
                {angleData.map((angle, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full" style={{backgroundColor: angle.color}} />
                      <span>{angle.name}</span>
                    </div>
                    <div className="flex gap-4 text-sm">
                      <span className="text-gray-400">{angle.posts} posts</span>
                      <span className="font-semibold">{angle.avgEngagement}% avg</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Tier Breakdown */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold mb-4">🏅 Performance Tier Breakdown</h3>
            <div className="grid grid-cols-4 gap-4">
              {[
                { tier: 'A', count: 5, desc: '>5% eng', color: 'green' },
                { tier: 'B', count: 8, desc: '3-5% eng', color: 'blue' },
                { tier: 'C', count: 7, desc: '2-3% eng', color: 'yellow' },
                { tier: 'D', count: 3, desc: '<2% eng', color: 'red' },
              ].map((item, i) => (
                <div key={i} className={`bg-${item.color}-900/30 border border-${item.color}-700/50 rounded-lg p-4 text-center`}>
                  <div className={`text-3xl font-bold text-${item.color}-400`}>{item.count}</div>
                  <div className="font-semibold">Tier {item.tier}</div>
                  <div className="text-sm text-gray-400">{item.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'timing' && (
        <div className="space-y-6">
          {/* Timing Heatmap */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold mb-4">📅 Best Posting Times (Avg Engagement %)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={timingData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="day" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Bar dataKey="time08" name="08:00" fill="#22c55e" />
                <Bar dataKey="time12" name="12:00" fill="#3b82f6" />
                <Bar dataKey="time17" name="17:00" fill="#a855f7" />
              </BarChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-6 mt-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-green-500" />
                <span className="text-sm">08:00</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-blue-500" />
                <span className="text-sm">12:00</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-purple-500" />
                <span className="text-sm">17:00</span>
              </div>
            </div>
          </div>

          {/* Best Timing Summary */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-gradient-to-br from-green-900/50 to-green-800/30 rounded-xl p-6 border border-green-700/50">
              <h4 className="text-xl font-bold text-green-400 mb-4">🏆 Beste Combinatie</h4>
              <div className="text-4xl font-bold mb-2">Dinsdag 08:00</div>
              <div className="text-gray-300">Gemiddeld 4.8% engagement</div>
              <div className="text-sm text-gray-400 mt-4">Gebaseerd op 23 posts over 6 weken</div>
            </div>
            <div className="bg-gradient-to-br from-red-900/50 to-red-800/30 rounded-xl p-6 border border-red-700/50">
              <h4 className="text-xl font-bold text-red-400 mb-4">⚠️ Vermijd</h4>
              <div className="text-4xl font-bold mb-2">Vrijdag 17:00</div>
              <div className="text-gray-300">Slechts 2.4% engagement</div>
              <div className="text-sm text-gray-400 mt-4">-50% vs beste tijd</div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'experiments' && (
        <div className="space-y-6">
          {/* Active Experiment */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-3 h-3 rounded-full bg-yellow-500 animate-pulse" />
              <h3 className="text-lg font-semibold">🔬 Active A/B Test</h3>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-gray-400 mb-2">Experiment</h4>
                <p className="text-xl">Data-driven vs Story-driven Contrarian Posts</p>
                <div className="mt-4">
                  <h4 className="font-semibold text-gray-400 mb-2">Hypothesis</h4>
                  <p>Data-driven contrarian posts (met cijfers) presteren 20% beter dan story-only.</p>
                </div>
              </div>
              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div>
                    <div className="text-sm text-gray-400 mb-1">Control</div>
                    <div className="text-2xl font-bold">3.8%</div>
                    <div className="text-sm text-gray-400">Story-only post</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-400 mb-1">Variant</div>
                    <div className="text-2xl font-bold text-green-400">4.6%</div>
                    <div className="text-sm text-gray-400">With 3 data points</div>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-600">
                  <div className="text-center">
                    <span className="text-green-400 font-bold">+21% improvement</span>
                    <span className="text-gray-400 ml-2">(day 5/7)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Past Experiments */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold mb-4">📋 Completed Experiments</h3>
            <div className="space-y-4">
              {[
                { name: 'Carousel vs Single Image', result: '+35%', winner: 'Carousel', status: 'Implemented' },
                { name: 'Question vs Statement CTA', result: '+28%', winner: 'Question', status: 'Implemented' },
                { name: '3 vs 5 Hashtags', result: '-8%', winner: '3 hashtags', status: 'Implemented' },
              ].map((exp, i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-gray-700/50 rounded-lg">
                  <div>
                    <div className="font-medium">{exp.name}</div>
                    <div className="text-sm text-gray-400">Winner: {exp.winner}</div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className={`font-bold ${exp.result.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>
                      {exp.result}
                    </div>
                    <div className="px-2 py-1 bg-green-900/50 text-green-400 rounded text-sm">
                      {exp.status}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Next Tests */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold mb-4">📝 Planned Experiments</h3>
            <div className="space-y-3">
              {[
                'Video thumbnail vs No preview (Week 3)',
                'Long-form (>1500 chars) vs Short-form (Week 4)',
                'Personal story intro vs Data intro (Week 5)',
              ].map((test, i) => (
                <div key={i} className="flex items-center gap-3 p-3 bg-gray-700/30 rounded-lg">
                  <div className="w-6 h-6 rounded bg-gray-600 flex items-center justify-center text-sm">
                    {i + 1}
                  </div>
                  <span>{test}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 pt-6 border-t border-gray-700 text-center text-gray-500 text-sm">
        <p>Content Analytics System v1.0 | Recruitin B.V. | Powered by Notion + HuggingFace</p>
        <p className="mt-1">
          <a href="https://www.notion.so/Content-Intelligence-Dashboard-2e62252cbb15818faf7ec06c3fae1a29" className="text-blue-400 hover:underline">
            Open in Notion →
          </a>
        </p>
      </div>
    </div>
  );
}
