<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Drug-Free Tamil Nadu | AI Intelligence Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
/* ══════════════════════════════════════
   DESIGN TOKENS
══════════════════════════════════════ */
:root {
  --navy:       #080f1e;
  --navy-mid:   #0d1a30;
  --navy-card:  #101e36;
  --gold:       #c9941a;
  --gold-lt:    #e8b84b;
  --gold-dim:   rgba(201,148,26,0.18);
  --red:        #d94040;
  --red-dim:    rgba(217,64,64,0.13);
  --green:      #2e7d5c;
  --green-lt:   #4ade80;
  --blue:       #4b8fd4;
  --text:       #eef2ff;
  --muted:      #8899bb;
  --border:     rgba(201,148,26,0.22);
  --border-lt:  rgba(255,255,255,0.06);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  font-family: 'Outfit', sans-serif;
  background: #919eb9;
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
body::before {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(201,148,26,0.055) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(75,143,212,0.04) 0%, transparent 60%);
}

/* ══════════════════════════════════════
   LOADING OVERLAY
══════════════════════════════════════ */
#loadOverlay {
  position:fixed; inset:0; z-index:999;
  background:var(--navy);
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  gap:20px; transition:opacity 0.5s;
}
#loadOverlay.hidden { opacity:0; pointer-events:none; }
.spinner {
  width:48px; height:48px;
  border:3px solid rgba(201,148,26,0.2);
  border-top-color:var(--gold);
  border-radius:50%;
  animation:spin 0.8s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }
.load-text {
  font-family:'Cormorant Garamond',serif;
  font-size:1.1rem; color:var(--gold-lt); letter-spacing:0.05em;
}
.load-sub { font-size:0.75rem; color:var(--muted); }

/* ══════════════════════════════════════
   ERROR BANNER
══════════════════════════════════════ */
#errorBanner {
  display:none; position:sticky; top:0; z-index:100;
  background:rgba(217,64,64,0.92); color:#fff;
  padding:10px 20px; font-size:0.83rem; text-align:center;
  backdrop-filter:blur(4px);
}

/* ══════════════════════════════════════
   LAYOUT
══════════════════════════════════════ */
.wrapper { position:relative; z-index:1; max-width:1420px; margin:0 auto; padding:0 24px 60px; }

/* ══════════════════════════════════════
   HEADER
══════════════════════════════════════ */
.gov-header {
  display:flex; align-items:center; gap:24px;
  background:linear-gradient(135deg,#0d2254 0%,#0f1e3a 70%,var(--navy) 100%);
  border:1px solid var(--border); border-radius:14px;
  padding:28px 36px; margin:28px 0 32px;
  position:relative; overflow:hidden;
  box-shadow:0 8px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(201,148,26,0.1);
  animation:fadeUp 0.5s ease both;
}
.gov-header::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,var(--gold),var(--gold-lt),transparent);
}
.gov-header::after {
  content:''; position:absolute; bottom:0; right:-40px;
  width:280px; height:280px; pointer-events:none;
  background:radial-gradient(circle,rgba(201,148,26,0.055) 0%,transparent 70%);
}
.emblem { font-size:3.8rem; filter:drop-shadow(0 0 16px rgba(201,148,26,0.6)); flex-shrink:0; }
.header-text h1 {
  font-family:'Cormorant Garamond',serif; font-size:2.1rem; font-weight:700;
  color:#fff; letter-spacing:0.015em; line-height:1.1; margin-bottom:5px;
}
.header-text p { font-size:0.73rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.1em; }
.header-right { margin-left:auto; display:flex; flex-direction:column; align-items:flex-end; gap:8px; }
.live-badge {
  background:rgba(46,125,92,0.18); border:1px solid var(--green);
  color:var(--green-lt); padding:5px 14px; border-radius:20px;
  font-size:0.7rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase;
  animation:pulseBadge 2s infinite;
}
@keyframes pulseBadge {
  0%,100% { box-shadow:0 0 0 0 rgba(46,125,92,0.5); }
  50%      { box-shadow:0 0 0 6px rgba(46,125,92,0); }
}
.timestamp { font-size:0.7rem; color:var(--muted); }
.timestamp span { color:var(--gold-lt); }
.refresh-btn {
  background:var(--gold-dim); border:1px solid var(--border);
  color:var(--gold-lt); padding:5px 14px; border-radius:7px;
  font-size:0.72rem; font-weight:600; cursor:pointer;
  font-family:'Outfit',sans-serif; transition:background 0.2s;
}
.refresh-btn:hover { background:rgba(201,148,26,0.3); }

/* ══════════════════════════════════════
   SECTION TITLE
══════════════════════════════════════ */
.section-title {
  font-family:'Cormorant Garamond',serif;
  font-size:1.4rem; font-weight:600; color:#fff;
  border-left:4px solid var(--gold); padding-left:14px;
  margin:36px 0 18px; letter-spacing:0.01em;
}

/* ══════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════ */
.grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:8px; }

.metric-card {
  background:linear-gradient(135deg,var(--navy-card),#12233f);
  border:1px solid var(--border); border-radius:12px; padding:22px 26px;
  position:relative; overflow:hidden;
  box-shadow:0 4px 24px rgba(0,0,0,0.35);
  transition:transform 0.2s, box-shadow 0.2s;
  animation:fadeUp 0.5s ease both;
}
.metric-card:nth-child(1){animation-delay:0.08s}
.metric-card:nth-child(2){animation-delay:0.16s}
.metric-card:nth-child(3){animation-delay:0.24s}
.metric-card:nth-child(4){animation-delay:0.32s}
.metric-card:hover { transform:translateY(-3px); box-shadow:0 10px 36px rgba(0,0,0,0.5); }
.metric-card::after { content:''; position:absolute; bottom:0; left:0; right:0; height:3px; }
.metric-card.total::after { background:linear-gradient(90deg,var(--gold),transparent); }
.metric-card.junk::after  { background:linear-gradient(90deg,#6b7280,transparent); }
.metric-card.valid::after { background:linear-gradient(90deg,var(--green),transparent); }
.metric-card.high::after  { background:linear-gradient(90deg,var(--red),transparent); }
.metric-icon { position:absolute; top:16px; right:20px; font-size:2rem; opacity:0.14; }
.metric-number { font-family:'Cormorant Garamond',serif; font-size:3rem; font-weight:700; line-height:1; margin-bottom:5px; }
.metric-label { font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--muted); }

/* ══════════════════════════════════════
   CHART CARDS
══════════════════════════════════════ */
.grid-2   { display:grid; grid-template-columns:3fr 2fr; gap:20px; margin-bottom:20px; }
.grid-2eq { display:grid; grid-template-columns:1fr 1fr;  gap:20px; margin-bottom:20px; }

.chart-card {
  background:var(--navy-card); border:1px solid var(--border-lt);
  border-radius:12px; padding:22px;
  box-shadow:0 4px 20px rgba(0,0,0,0.3);
  animation:fadeUp 0.5s ease 0.3s both;
}
.chart-card h3 {
  font-family:'Cormorant Garamond',serif; font-size:1.05rem; font-weight:600; color:#fff;
  margin-bottom:16px; padding-bottom:10px; border-bottom:1px solid var(--border-lt);
}

/* ══════════════════════════════════════
   MAP
══════════════════════════════════════ */
.map-card {
  background:var(--navy-card); border:1px solid var(--border-lt);
  border-radius:12px; padding:22px;
  box-shadow:0 4px 20px rgba(0,0,0,0.3);
  animation:fadeUp 0.5s ease 0.35s both;
}
.map-card h3 {
  font-family:'Cormorant Garamond',serif; font-size:1.05rem; font-weight:600; color:#fff;
  margin-bottom:16px;
}
.map-container {
  position:relative; background:#0a1628;
  border-radius:10px; overflow:hidden;
  height:420px; border:1px solid rgba(255,255,255,0.05);
}
#tnMap { width:100%; height:100%; }
.city-dot { cursor:pointer; }

.map-legend {
  display:flex; gap:20px; margin-top:14px; font-size:0.75rem; color:var(--muted);
  align-items:center; flex-wrap:wrap;
}
.legend-dot {
  width:11px; height:11px; border-radius:50%;
  display:inline-block; margin-right:5px; vertical-align:middle;
}
.map-stats { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:14px; }
.map-stat {
  background:rgba(255,255,255,0.03); border:1px solid var(--border-lt);
  border-radius:8px; padding:10px 14px; text-align:center;
}
.map-stat .v { font-size:1.35rem; font-family:'Cormorant Garamond',serif; font-weight:700; color:var(--gold-lt); }
.map-stat .l { font-size:0.65rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; margin-top:2px; }

/* ══════════════════════════════════════
   ALERTS
══════════════════════════════════════ */
.alert-high {
  background:var(--red-dim); border:1px solid rgba(217,64,64,0.45);
  border-left:4px solid var(--red); border-radius:8px;
  padding:13px 18px; margin-bottom:12px; font-size:0.85rem;
}
.alert-ok {
  background:rgba(46,125,92,0.1); border:1px solid rgba(46,125,92,0.4);
  border-left:4px solid var(--green); border-radius:8px;
  padding:13px 18px; font-size:0.85rem;
}

/* ══════════════════════════════════════
   HOTSPOT TABLE
══════════════════════════════════════ */
.hs-table { width:100%; border-collapse:collapse; font-size:0.82rem; }
.hs-table th {
  padding:9px 14px; text-align:left; font-size:0.67rem;
  letter-spacing:0.08em; text-transform:uppercase; color:var(--muted);
  border-bottom:1px solid var(--border-lt);
}
.hs-table td { padding:9px 14px; border-bottom:1px solid rgba(255,255,255,0.03); }
.intensity-bar {
  height:6px; background:linear-gradient(90deg,var(--red),var(--gold));
  border-radius:3px; min-width:6px;
}

/* ══════════════════════════════════════
   MAIN TABLE
══════════════════════════════════════ */
.table-wrap {
  background:var(--navy-card); border:1px solid var(--border-lt);
  border-radius:12px; overflow:hidden;
  box-shadow:0 4px 20px rgba(0,0,0,0.3);
  animation:fadeUp 0.5s ease 0.4s both;
}
.table-toolbar {
  display:flex; align-items:center; gap:12px;
  padding:16px 20px; border-bottom:1px solid var(--border-lt); flex-wrap:wrap;
}
.table-toolbar h3 { font-family:'Cormorant Garamond',serif; font-size:1.05rem; font-weight:600; color:#fff; flex:1; }
.search-box {
  background:rgba(255,255,255,0.05); border:1px solid var(--border-lt);
  border-radius:7px; padding:7px 14px; color:var(--text); font-size:0.82rem;
  outline:none; width:220px; font-family:'Outfit',sans-serif; transition:border 0.2s;
}
.search-box:focus { border-color:var(--gold); }
.search-box::placeholder { color:var(--muted); }
.btn-export {
  background:var(--gold-dim); border:1px solid var(--border);
  color:var(--gold-lt); padding:7px 16px; border-radius:7px;
  font-size:0.78rem; font-weight:600; letter-spacing:0.05em;
  cursor:pointer; transition:background 0.2s; font-family:'Outfit',sans-serif;
  text-transform:uppercase;
}
.btn-export:hover { background:rgba(201,148,26,0.3); }
.table-scroll { overflow-x:auto; max-height:420px; overflow-y:auto; }

table.main { width:100%; border-collapse:collapse; font-size:0.82rem; }
table.main thead th {
  background:rgba(255,255,255,0.04); padding:11px 16px; text-align:left;
  font-size:0.68rem; font-weight:600; letter-spacing:0.09em; text-transform:uppercase;
  color:var(--muted); border-bottom:1px solid var(--border-lt);
  position:sticky; top:0; z-index:1;
}
table.main tbody tr { border-bottom:1px solid rgba(255,255,255,0.03); transition:background 0.15s; }
table.main tbody tr:hover { background:rgba(255,255,255,0.03); }
table.main tbody td { padding:10px 16px; color:var(--text); vertical-align:middle; }
.no-rows { text-align:center; padding:30px; color:var(--muted); }

.badge {
  display:inline-block; padding:3px 10px; border-radius:20px;
  font-size:0.68rem; font-weight:600; letter-spacing:0.05em;
}
.badge.HIGH   { background:rgba(217,64,64,0.2);   color:#fc8181; border:1px solid rgba(217,64,64,0.4); }
.badge.MEDIUM { background:rgba(232,184,75,0.15); color:#e8b84b; border:1px solid rgba(232,184,75,0.4); }
.badge.LOW    { background:rgba(74,222,128,0.12); color:#4ade80; border:1px solid rgba(74,222,128,0.3); }
.badge.junk   { background:rgba(107,114,128,0.2); color:#9ca3af; border:1px solid rgba(107,114,128,0.3); }
.badge.valid  { background:rgba(74,222,128,0.1);  color:#4ade80; border:1px solid rgba(74,222,128,0.25); }

/* ══════════════════════════════════════
   CITY MODAL
══════════════════════════════════════ */
#cityModal {
  display:none; position:fixed; inset:0; z-index:200;
  background:rgba(0,0,0,0.72); backdrop-filter:blur(4px);
  align-items:center; justify-content:center;
}
.modal-box {
  background:#101e36; border:1px solid rgba(201,148,26,0.4);
  border-radius:14px; padding:28px; min-width:300px; max-width:400px;
  position:relative; animation:fadeUp 0.2s ease both;
}
.modal-close {
  position:absolute; top:14px; right:16px; background:none; border:none;
  color:var(--muted); font-size:1.3rem; cursor:pointer;
}

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
.gov-footer {
  text-align:center; padding:28px; margin-top:40px;
  border-top:1px solid rgb(201 143 9); font-size:0.73rem;
  color:#000000; letter-spacing:0.04em; line-height:1.8;
}
.gov-footer a { color:var(--gold); text-decoration:none; }
.gov-footer a:hover { color:var(--gold-lt); }

/* ══════════════════════════════════════
   UTILS
══════════════════════════════════════ */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--navy); }
::-webkit-scrollbar-thumb { background:var(--gold); border-radius:3px; }

@keyframes fadeUp {
  from { opacity:0; transform:translateY(16px); }
  to   { opacity:1; transform:translateY(0); }
}

@media(max-width:900px){
  .grid-4 { grid-template-columns:1fr 1fr; }
  .grid-2,.grid-2eq { grid-template-columns:1fr; }
  .gov-header { flex-wrap:wrap; }
  .header-right { margin-left:0; }
}
@media(max-width:520px){
  .grid-4 { grid-template-columns:1fr; }
  .header-text h1 { font-size:1.5rem; }
}
</style>
</head>
<body>

<!-- ═══ LOADING OVERLAY ═══ -->
<div id="loadOverlay">
  <div class="spinner"></div>
  <div class="load-text">🛡️ Drug-Free Tamil Nadu</div>
  <div class="load-sub">Connecting to intelligence backend…</div>
</div>

<!-- ═══ ERROR BANNER ═══ -->
<div id="errorBanner">
  ⚠️ Could not connect to backend API. Showing last cached data or check that FastAPI is running on
  <strong id="apiUrlDisplay"></strong>
</div>

<div class="wrapper">

  <!-- ═══ HEADER ═══ -->
  <header class="gov-header">
    <div class="emblem">🛡️</div>
    <div class="header-text">
      <h1>Drug-Free Tamil Nadu — AI Intelligence Dashboard</h1>
      <p>Tamil Nadu Government &nbsp;·&nbsp; Social Defence Department &nbsp;·&nbsp; Narcotics Intelligence Unit</p>
    </div>
    <div class="header-right">
      <div class="live-badge">● Live</div>
      <div class="timestamp">Updated: <span id="ts">—</span></div>
      <button class="refresh-btn" onclick="loadData()">🔄 Refresh</button>
    </div>
  </header>

  <!-- ═══ KPI METRICS ═══ -->
  <div class="grid-4">
    <div class="metric-card total">
      <div class="metric-icon">📋</div>
      <div class="metric-number" style="color:#e8b84b;" id="m-total">—</div>
      <div class="metric-label">Total Complaints</div>
    </div>
    <div class="metric-card junk">
      <div class="metric-icon">🗑️</div>
      <div class="metric-number" style="color:#9ca3af;" id="m-junk">—</div>
      <div class="metric-label">Junk / Spam</div>
    </div>
    <div class="metric-card valid">
      <div class="metric-icon">✅</div>
      <div class="metric-number" style="color:#4ade80;" id="m-valid">—</div>
      <div class="metric-label">Valid Complaints</div>
    </div>
    <div class="metric-card high">
      <div class="metric-icon">⚠️</div>
      <div class="metric-number" style="color:#d94040;" id="m-high">—</div>
      <div class="metric-label">High-Risk Cases</div>
    </div>
  </div>

  <!-- ═══ ANALYTICS ═══ -->
  <div class="section-title">📊 Complaint Analytics</div>
  <div class="grid-2">
    <div class="chart-card">
      <h3>Complaints by District</h3>
      <div style="height:240px;"><canvas id="cityChart"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Drug Category Breakdown</h3>
      <div style="height:240px;"><canvas id="drugChart"></canvas></div>
    </div>
  </div>

  <div class="grid-2eq">
    <div class="chart-card">
      <h3>Crime Type Distribution</h3>
      <div style="height:200px;"><canvas id="crimeChart"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Cases by Priority Level</h3>
      <div style="height:200px;"><canvas id="priorityChart"></canvas></div>
    </div>
  </div>

  <!-- ═══ TREND ═══ -->
  <div class="section-title">📈 Complaint Trend</div>
  <div class="chart-card">
    <h3>Daily Complaint Volume — Last 14 Days</h3>
    <div style="height:200px;"><canvas id="trendChart"></canvas></div>
  </div>

  <!-- ═══ MAP ═══ -->
  <div class="section-title">🗺️ Geographic Intelligence Map</div>
  <div class="map-card">
    <h3>Tamil Nadu District Heat-Map</h3>
    <div class="map-container">
      <svg id="tnMap" viewBox="0 0 500 560" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="mapBg" cx="50%" cy="50%" r="60%">
            <stop offset="0%"   stop-color="#0d2040"/>
            <stop offset="100%" stop-color="#080f1e"/>
          </radialGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <rect width="500" height="560" fill="url(#mapBg)"/>
        <!-- grid -->
        <g stroke="rgba(255,255,255,0.035)" stroke-width="1">
          <line x1="0" y1="80"  x2="500" y2="80"/>
          <line x1="0" y1="160" x2="500" y2="160"/>
          <line x1="0" y1="240" x2="500" y2="240"/>
          <line x1="0" y1="320" x2="500" y2="320"/>
          <line x1="0" y1="400" x2="500" y2="400"/>
          <line x1="0" y1="480" x2="500" y2="480"/>
          <line x1="100" y1="0" x2="100" y2="560"/>
          <line x1="200" y1="0" x2="200" y2="560"/>
          <line x1="300" y1="0" x2="300" y2="560"/>
          <line x1="400" y1="0" x2="400" y2="560"/>
        </g>
        <!-- TN outline -->
        <path d="M230,20 L280,30 L310,55 L330,80 L340,110 L350,140
                 L355,170 L360,200 L358,240 L350,280 L335,320
                 L320,360 L300,400 L270,430 L240,460 L210,480
                 L185,500 L175,520 L180,535 L195,540 L210,530
                 L230,510 L250,490 L265,470 L275,450
                 L300,415 L325,375 L340,340 L348,300
                 L352,260 L352,220 L345,185 L335,155
                 L320,125 L300,95 L275,65 L250,42 Z"
              fill="rgba(16,40,80,0.65)"
              stroke="rgba(201,148,26,0.4)" stroke-width="1.5"/>
        <!-- sea labels -->
        <text x="395" y="260" font-size="11" fill="rgba(255,255,255,0.16)"
              font-family="Outfit,sans-serif" font-style="italic" transform="rotate(15,395,260)">Bay of Bengal</text>
        <text x="50" y="320" font-size="11" fill="rgba(255,255,255,0.16)"
              font-family="Outfit,sans-serif" font-style="italic" transform="rotate(-10,50,320)">Arabian Sea</text>
        <!-- city dots rendered by JS -->
        <g id="cityDots"></g>
      </svg>
    </div>
    <div class="map-legend">
      <span><span class="legend-dot" style="background:#d94040;"></span>High Risk — Sale</span>
      <span><span class="legend-dot" style="background:#e8b84b;"></span>Medium Risk — Usage</span>
      <span><span class="legend-dot" style="background:#4b8fd4;"></span>Low Risk — Possession</span>
      <span style="margin-left:auto;font-size:0.7rem;color:#555;">Click a dot for details</span>
    </div>
    <div class="map-stats" id="mapStats"></div>
  </div>

  <!-- ═══ HOTSPOTS ═══ -->
  <div class="section-title">🔥 Hotspot Intelligence</div>
  <div class="grid-2eq">
    <div class="chart-card">
      <h3>All Hotspot Areas</h3>
      <table class="hs-table">
        <thead><tr><th>District</th><th>Location</th><th>Incidents</th><th>Intensity</th></tr></thead>
        <tbody id="hotspotBody"></tbody>
      </table>
    </div>
    <div class="chart-card">
      <h3>🚨 High-Risk Drug Sale Zones</h3>
      <div id="riskAlert"></div>
      <table class="hs-table">
        <thead><tr><th>District</th><th>Location</th><th>Sale Incidents</th></tr></thead>
        <tbody id="riskBody"></tbody>
      </table>
    </div>
  </div>

  <!-- ═══ COMPLAINTS TABLE ═══ -->
  <div class="section-title">📋 Complaints Registry</div>
  <div class="table-wrap">
    <div class="table-toolbar">
      <h3>All Complaints</h3>
      <input class="search-box" type="text" id="tableSearch"
             placeholder="🔍 Search complaints…" oninput="filterTable()"/>
      <button class="btn-export" onclick="exportCSV()">⬇️ Export CSV</button>
    </div>
    <div class="table-scroll">
      <table class="main" id="mainTable">
        <thead>
          <tr>
            <th>Date</th><th>City</th><th>Location</th>
            <th>Drug Type</th><th>Crime Type</th>
            <th>Priority</th><th>Status</th>
          </tr>
        </thead>
        <tbody id="mainBody"></tbody>
      </table>
    </div>
  </div>

  <!-- ═══ FOOTER ═══ -->
  <footer class="gov-footer">
    Government of Tamil Nadu &nbsp;·&nbsp; Social Defence Department &nbsp;·&nbsp; Narcotics Intelligence Unit<br>
    <a href="https://drugfreetamilnadu.tn.gov.in/en" target="_blank">drugfreetamilnadu.tn.gov.in</a>
    &nbsp;·&nbsp; All data is confidential and for official use only.
  </footer>
</div>

<!-- ═══ CITY DETAIL MODAL ═══ -->
<div id="cityModal">
  <div class="modal-box">
    <button class="modal-close" onclick="document.getElementById('cityModal').style.display='none'">✕</button>
    <div id="modalContent"></div>
  </div>
</div>

<!-- ══════════════════════════════════════
     JAVASCRIPT — API INTEGRATION
══════════════════════════════════════ -->
<script>
// ─────────────────────────────────────────
// CONFIG — change this to match your server
// ─────────────────────────────────────────
const API_BASE = "http://localhost:8080";   // ← FastAPI server
const API_URL  = `${API_BASE}/api/dashboard/data`;

document.getElementById("apiUrlDisplay").textContent = API_URL;

// ─────────────────────────────────────────
// Chart.js global defaults
// ─────────────────────────────────────────
Chart.defaults.color         = "#8899bb";
Chart.defaults.borderColor   = "rgba(255,255,255,0.05)";
Chart.defaults.font.family   = "Outfit, sans-serif";

const GOLD="#c9941a", GOLD_LT="#e8b84b", RED="#d94040",
      BLUE="#4b8fd4", GREEN="#2e7d5c", PURPLE="#7c5cbf";

// Chart instance refs so we can destroy/rebuild on refresh
let charts = {};

// Full complaints array for client-side search
let allComplaints = [];

// ─────────────────────────────────────────
// CITY → SVG pixel position mapping
// (mirrors CITY_COORDS from Python backend)
// ─────────────────────────────────────────
const CITY_SVG = {
  "Chennai":      {x:312, y:88},
  "Kancheepuram": {x:285, y:122},
  "Vellore":      {x:258, y:110},
  "Salem":        {x:240, y:212},
  "Erode":        {x:220, y:237},
  "Coimbatore":   {x:192, y:262},
  "Trichy":       {x:265, y:280},
  "Thanjavur":    {x:295, y:298},
  "Madurai":      {x:268, y:355},
  "Tirunelveli":  {x:255, y:440},
};

// ─────────────────────────────────────────
// FETCH DATA FROM FASTAPI
// ─────────────────────────────────────────
async function loadData() {
  showLoading(true);
  try {
    const resp = await fetch(API_URL, { cache: "no-store" });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    document.getElementById("errorBanner").style.display = "none";
    renderAll(data);
  } catch (err) {
    console.error("API error:", err);
    document.getElementById("errorBanner").style.display = "block";
  } finally {
    showLoading(false);
    document.getElementById("ts").textContent =
      new Date().toLocaleString("en-IN", {
        day:"2-digit", month:"short", year:"numeric",
        hour:"2-digit", minute:"2-digit"
      });
  }
}

function showLoading(on) {
  const ov = document.getElementById("loadOverlay");
  if (on) { ov.classList.remove("hidden"); }
  else    { ov.classList.add("hidden"); }
}

// ─────────────────────────────────────────
// MASTER RENDER
// ─────────────────────────────────────────
function renderAll(data) {
  renderKPIs(data.kpis);
  renderCityChart(data.city_chart);
  renderDrugChart(data.drug_chart);
  renderCrimeChart(data.crime_chart);
  renderPriorityChart(data.priority_chart);
  renderTrendChart(data.trend_chart);
  renderMap(data.map_data);
  renderHotspots(data.hotspots, data.high_risk_zones);
  allComplaints = data.complaints;
  renderTable(allComplaints);
}

// ─────────────────────────────────────────
// KPIs
// ─────────────────────────────────────────
function animateCount(el, target) {
  let cur = 0;
  const step = Math.max(1, Math.ceil(target / 30));
  const iv = setInterval(() => {
    cur = Math.min(cur + step, target);
    el.textContent = cur;
    if (cur >= target) clearInterval(iv);
  }, 35);
}

function renderKPIs(k) {
  animateCount(document.getElementById("m-total"), k.total);
  animateCount(document.getElementById("m-junk"),  k.junk);
  animateCount(document.getElementById("m-valid"), k.valid);
  animateCount(document.getElementById("m-high"),  k.high);
}

// ─────────────────────────────────────────
// CHART HELPERS
// ─────────────────────────────────────────
function destroyChart(key) {
  if (charts[key]) { charts[key].destroy(); delete charts[key]; }
}

function renderCityChart(d) {
  destroyChart("city");
  charts.city = new Chart(document.getElementById("cityChart"), {
    type: "bar",
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: d.values.map((_,i) => `rgba(201,148,26,${0.35 + i * 0.06})`),
        borderColor: GOLD_LT, borderWidth: 1, borderRadius: 5,
      }]
    },
    options: {
      responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{display:false} },
      scales:{
        x:{ grid:{color:"rgba(255,255,255,0.04)"}, ticks:{color:"#8899bb",font:{size:11}} },
        y:{ grid:{color:"rgba(255,255,255,0.04)"}, ticks:{color:"#8899bb",font:{size:11}}, beginAtZero:true }
      }
    }
  });
}

function renderDrugChart(d) {
  destroyChart("drug");
  charts.drug = new Chart(document.getElementById("drugChart"), {
    type: "doughnut",
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: [GOLD, GOLD_LT, BLUE, RED, GREEN, PURPLE,"#f97316","#a3e635"],
        borderColor: "#101e36", borderWidth: 3, hoverOffset: 8,
      }]
    },
    options: {
      responsive:true, maintainAspectRatio:false, cutout:"60%",
      plugins:{ legend:{ position:"right", labels:{ color:"#a8b8d8", padding:12, font:{size:11} } } }
    }
  });
}

function renderCrimeChart(d) {
  destroyChart("crime");
  charts.crime = new Chart(document.getElementById("crimeChart"), {
    type: "bar",
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: [RED, GOLD_LT, BLUE, GREEN],
        borderRadius: 5, borderWidth: 0,
      }]
    },
    options: {
      indexAxis:"y", responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{display:false} },
      scales:{
        x:{ grid:{color:"rgba(255,255,255,0.04)"}, ticks:{color:"#8899bb",font:{size:11}} },
        y:{ grid:{display:false}, ticks:{color:"#8899bb",font:{size:11}} }
      }
    }
  });
}

function renderPriorityChart(d) {
  destroyChart("priority");
  charts.priority = new Chart(document.getElementById("priorityChart"), {
    type: "bar",
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values,
        backgroundColor: ["rgba(217,64,64,0.75)","rgba(232,184,75,0.75)","rgba(74,222,128,0.6)"],
        borderColor: [RED, GOLD_LT, "#4ade80"],
        borderWidth: 1, borderRadius: 5,
      }]
    },
    options: {
      responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{display:false} },
      scales:{
        x:{ grid:{display:false}, ticks:{color:"#8899bb"} },
        y:{ grid:{color:"rgba(255,255,255,0.04)"}, ticks:{color:"#8899bb"}, beginAtZero:true }
      }
    }
  });
}

function renderTrendChart(d) {
  destroyChart("trend");
  charts.trend = new Chart(document.getElementById("trendChart"), {
    type: "line",
    data: {
      labels: d.labels,
      datasets: [{
        data: d.values, label: "Complaints",
        fill: true,
        backgroundColor: "rgba(201,148,26,0.1)",
        borderColor: GOLD_LT, borderWidth: 2,
        pointBackgroundColor: GOLD_LT, pointRadius: 4,
        tension: 0.4,
      }]
    },
    options: {
      responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{display:false} },
      scales:{
        x:{ grid:{color:"rgba(255,255,255,0.04)"}, ticks:{color:"#8899bb",font:{size:10}} },
        y:{ grid:{color:"rgba(255,255,255,0.04)"}, ticks:{color:"#8899bb"}, beginAtZero:true }
      }
    }
  });
}

// ─────────────────────────────────────────
// MAP — dynamic dots from API data
// ─────────────────────────────────────────
function crimeColor(crime) {
  if (!crime) return ["rgba(75,143,212,0.7)","#4b8fd4"];
  const c = crime.toLowerCase();
  if (c === "sale")      return ["rgba(217,64,64,0.75)", "#ffd700"];
  if (c === "usage")     return ["rgba(232,184,75,0.7)", "#e8b84b"];
  return ["rgba(75,143,212,0.65)", "#4b8fd4"];
}

function renderMap(mapData) {
  const g = document.getElementById("cityDots");
  g.innerHTML = "";

  if (!mapData || !mapData.length) {
    const t = document.createElementNS("http://www.w3.org/2000/svg","text");
    t.setAttribute("x","250"); t.setAttribute("y","280");
    t.setAttribute("text-anchor","middle"); t.setAttribute("fill","#8899bb");
    t.setAttribute("font-size","13"); t.textContent = "No geo-tagged complaints";
    g.appendChild(t); return;
  }

  const maxCount = Math.max(...mapData.map(d => d.count));

  mapData.forEach(d => {
    const pos = CITY_SVG[d.city];
    if (!pos) return;

    const [fill, stroke] = crimeColor(d.top_crime);
    // radius scaled 8–22px
    const r = 8 + (d.count / maxCount) * 14;
    const ns = "http://www.w3.org/2000/svg";

    const grp = document.createElementNS(ns, "g");
    grp.setAttribute("class","city-dot");
    grp.style.cursor = "pointer";

    // glow halo
    const halo = document.createElementNS(ns,"circle");
    halo.setAttribute("cx",pos.x); halo.setAttribute("cy",pos.y);
    halo.setAttribute("r",r+8); halo.setAttribute("fill",fill.replace("0.7","0.25").replace("0.75","0.25"));

    // main dot
    const dot = document.createElementNS(ns,"circle");
    dot.setAttribute("cx",pos.x); dot.setAttribute("cy",pos.y);
    dot.setAttribute("r",r); dot.setAttribute("fill",fill);
    dot.setAttribute("stroke",stroke); dot.setAttribute("stroke-width","1.5");
    dot.setAttribute("filter","url(#glow)");

    // inner dot
    const core = document.createElementNS(ns,"circle");
    core.setAttribute("cx",pos.x); core.setAttribute("cy",pos.y);
    core.setAttribute("r","3"); core.setAttribute("fill","#fff");

    // label
    const lbl = document.createElementNS(ns,"text");
    lbl.setAttribute("x", pos.x + r + 5);
    lbl.setAttribute("y", pos.y - 2);
    lbl.setAttribute("font-size","10"); lbl.setAttribute("fill","#e8b84b");
    lbl.setAttribute("font-family","Outfit,sans-serif"); lbl.setAttribute("font-weight","600");
    lbl.textContent = d.city;

    const cnt = document.createElementNS(ns,"text");
    cnt.setAttribute("x", pos.x + r + 5);
    cnt.setAttribute("y", pos.y + 10);
    cnt.setAttribute("font-size","9"); cnt.setAttribute("fill","#a8b8d8");
    cnt.setAttribute("font-family","Outfit,sans-serif");
    cnt.textContent = `${d.count} case${d.count!==1?"s":""}`;

    grp.appendChild(halo); grp.appendChild(dot); grp.appendChild(core);
    grp.appendChild(lbl); grp.appendChild(cnt);

    // click → modal
    grp.addEventListener("click", () => showCityModal(d));
    g.appendChild(grp);
  });

  // map stats
  const total = mapData.reduce((s,d) => s+d.count, 0);
  const top   = mapData.reduce((a,b) => a.count > b.count ? a : b, {city:"—",count:0});
  document.getElementById("mapStats").innerHTML = `
    <div class="map-stat"><div class="v">${mapData.length}</div><div class="l">Cities Mapped</div></div>
    <div class="map-stat"><div class="v">${top.city} — ${top.count}</div><div class="l">Highest Complaints</div></div>
    <div class="map-stat"><div class="v">${total}</div><div class="l">Total Geo-Tagged</div></div>`;
}

function showCityModal(d) {
  document.getElementById("modalContent").innerHTML = `
    <div style="margin-bottom:14px;">
      <div style="font-size:0.7rem;color:#a8b8d8;text-transform:uppercase;letter-spacing:0.1em;">District</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:700;color:#e8b84b;">${d.city}</div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;">
      <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:1.8rem;font-family:'Cormorant Garamond',serif;color:#d94040;font-weight:700;">${d.count}</div>
        <div style="font-size:0.68rem;color:#8899bb;text-transform:uppercase;letter-spacing:0.08em;">Total Cases</div>
      </div>
      <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:1rem;font-weight:600;color:#e8b84b;text-transform:capitalize;">${d.top_crime}</div>
        <div style="font-size:0.68rem;color:#8899bb;text-transform:uppercase;letter-spacing:0.08em;">Primary Crime</div>
      </div>
    </div>
    <div style="font-size:0.78rem;color:#a8b8d8;text-align:center;">Lat ${d.lat.toFixed(4)} · Lon ${d.lon.toFixed(4)}</div>`;
  document.getElementById("cityModal").style.display = "flex";
}

document.getElementById("cityModal").addEventListener("click", function(e) {
  if (e.target === this) this.style.display = "none";
});

// ─────────────────────────────────────────
// HOTSPOTS
// ─────────────────────────────────────────
function renderHotspots(hotspots, highRisk) {
  const maxHs = hotspots[0]?.count || 1;
  const hb = document.getElementById("hotspotBody");
  hb.innerHTML = "";
  if (!hotspots.length) {
    hb.innerHTML = `<tr><td colspan="4" class="no-rows">No hotspots detected.</td></tr>`;
  } else {
    hotspots.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r.city}</td><td style="color:var(--muted);">${r.location}</td>
        <td style="color:#e8b84b;font-weight:600;">${r.count}</td>
        <td><div class="intensity-bar" style="width:${Math.max(6,(r.count/maxHs)*90)}px;"></div></td>`;
      hb.appendChild(tr);
    });
  }

  const ra = document.getElementById("riskAlert");
  const rb = document.getElementById("riskBody");
  rb.innerHTML = "";
  if (!highRisk.length) {
    ra.innerHTML = `<div class="alert-ok">✅ No high-risk drug sale zones under current data.</div>`;
    rb.innerHTML = `<tr><td colspan="3" class="no-rows">No high-risk zones.</td></tr>`;
  } else {
    ra.innerHTML = `<div class="alert-high">⚠️ <strong>${highRisk.length} high-risk sale zone(s) detected</strong> — immediate action required.</div>`;
    highRisk.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${r.city}</td><td style="color:var(--muted);">${r.location}</td>
        <td><span style="color:#fc8181;font-weight:700;">${r.count}</span></td>`;
      rb.appendChild(tr);
    });
  }
}

// ─────────────────────────────────────────
// COMPLAINTS TABLE
// ─────────────────────────────────────────
function renderTable(data) {
  const tb = document.getElementById("mainBody");
  tb.innerHTML = "";
  if (!data.length) {
    tb.innerHTML = `<tr><td colspan="7" class="no-rows">No records found.</td></tr>`;
    return;
  }
  data.forEach(r => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="color:var(--muted);font-size:0.78rem;">${r.date}</td>
      <td>${r.city}</td>
      <td style="color:var(--muted);">${r.location}</td>
      <td style="color:#a8b8d8;">${r.drug}</td>
      <td style="text-transform:capitalize;">${r.crime}</td>
      <td><span class="badge ${r.junk ? "LOW" : r.priority}">${r.junk ? "—" : r.priority}</span></td>
      <td><span class="badge ${r.junk ? "junk" : "valid"}">${r.junk ? "Junk" : "Valid"}</span></td>`;
    tb.appendChild(tr);
  });
}

function filterTable() {
  const q = document.getElementById("tableSearch").value.toLowerCase();
  renderTable(allComplaints.filter(r =>
    Object.values(r).some(v => String(v).toLowerCase().includes(q))
  ));
}

function exportCSV() {
  const h = ["Date","City","Location","Drug Type","Crime Type","Priority","Status"];
  const rows = allComplaints.map(r =>
    [r.date, r.city, r.location, r.drug, r.crime, r.priority, r.junk ? "Junk" : "Valid"]
  );
  const csv = [h, ...rows].map(r => r.join(",")).join("\n");
  const a = document.createElement("a");
  a.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
  a.download = `drugfreetn_${new Date().toISOString().slice(0,10)}.csv`;
  a.click();
}

// ─────────────────────────────────────────
// AUTO REFRESH every 30 seconds
// ─────────────────────────────────────────
// loadData();
// setInterval(loadData, 30000);

window.onload = () => {
  loadData();   // ✅ run only once
};
</script>
</body>
</html>