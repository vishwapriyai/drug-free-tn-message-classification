# ─────────────────────────────────────────
# app/routes/dashboard.py
# Add this file to your routes folder and
# include it in main.py (see bottom of file)
# ─────────────────────────────────────────

from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.database.db import get_connection
from collections import Counter
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/submit", response_class=HTMLResponse)
def complaint_submit_page():
    """Browser page for entering a single complaint and address."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Submit Complaint | Drug-Free TN</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg:#f4f6fb; --surface:#fff; --navy:#0f2044; --accent:#1a5eb8;
  --gold:#c07c1a; --green:#1a7a4a; --red:#c0392b; --text:#1a2340;
  --muted:#64748b; --border:#e2e8f4; --shadow:0 8px 32px rgba(26,50,90,.12);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Poppins,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
.wrap{max-width:980px;margin:0 auto;padding:28px}
.header{
  background:linear-gradient(135deg,var(--navy),#1a3560 60%,#1e4a8a);
  color:#fff;border-radius:12px;padding:26px 32px;margin-bottom:22px;
  display:flex;align-items:center;justify-content:space-between;gap:18px;box-shadow:var(--shadow)
}
.header h1{font-size:1.55rem;line-height:1.2;margin-bottom:6px}
.header p{font-size:.78rem;color:rgba(255,255,255,.68)}
.nav{display:flex;gap:10px;flex-wrap:wrap}
.nav a,.nav button{
  border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.1);
  color:#fff;text-decoration:none;border-radius:8px;padding:9px 14px;
  font:600 .78rem Poppins,sans-serif;cursor:pointer
}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;box-shadow:var(--shadow);padding:28px}
.grid{display:grid;grid-template-columns:1fr;gap:18px}
label{display:block;font-weight:600;font-size:.86rem;margin-bottom:8px;color:var(--navy)}
textarea,input{
  width:100%;border:1px solid #cbd5e8;border-radius:10px;background:#fff;
  font:400 .95rem Poppins,sans-serif;color:var(--text);padding:14px 15px;outline:none
}
textarea{min-height:170px;resize:vertical}
textarea:focus,input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(26,94,184,.1)}
.actions{display:flex;gap:12px;align-items:center;margin-top:22px;flex-wrap:wrap}
.submit{
  border:0;background:var(--accent);color:#fff;border-radius:10px;padding:12px 18px;
  font:700 .9rem Poppins,sans-serif;cursor:pointer
}
.submit:disabled{opacity:.6;cursor:not-allowed}
.clear{border:1px solid var(--border);background:#fff;color:var(--muted);border-radius:10px;padding:12px 18px;font-weight:600;cursor:pointer}
.status{font-size:.85rem;color:var(--muted)}
.result{display:none;margin-top:22px;border:1px solid var(--border);border-radius:12px;overflow:hidden}
.result-head{background:#f8fafc;padding:13px 16px;font-weight:700;color:var(--navy);border-bottom:1px solid var(--border)}
.summary{padding:18px;background:#fff}
.verdict{
  border-radius:10px;padding:14px 16px;margin-bottom:16px;font-weight:700;
  display:flex;align-items:center;justify-content:space-between;gap:12px
}
.verdict.valid{background:rgba(26,122,74,.09);color:var(--green)}
.verdict.junk{background:rgba(192,57,43,.08);color:var(--red)}
.pill{border-radius:999px;padding:5px 10px;background:rgba(255,255,255,.7);font-size:.72rem}
.result-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.result-item{border:1px solid var(--border);border-radius:10px;padding:13px 14px;background:#fbfdff}
.result-label{font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin-bottom:5px}
.result-value{font-size:.98rem;font-weight:700;color:var(--navy);word-break:break-word}
.result-note{margin-top:14px;color:var(--muted);font-size:.82rem;line-height:1.55}
.raw-toggle{margin-top:16px;border:0;background:transparent;color:var(--accent);font-weight:700;cursor:pointer}
.raw-json{display:none;white-space:pre-wrap;word-break:break-word;margin-top:10px;padding:14px;border-radius:10px;background:#f8fafc;font-size:.78rem;line-height:1.5}
.ok{color:var(--green)} .err{color:var(--red)}
@media(max-width:720px){.wrap{padding:16px}.header{align-items:flex-start;flex-direction:column}.card{padding:20px}.result-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<main class="wrap">
  <header class="header">
    <div>
      <h1>Complaint Entry</h1>
      <p>Enter complaint text and address. The same AI pipeline will classify it and save it to the database.</p>
    </div>
    <nav class="nav">
      <a href="/">Dashboard</a>
      <a href="/docs">Swagger</a>
    </nav>
  </header>

  <section class="card">
    <form id="complaintForm">
      <div class="grid">
        <div>
          <label for="complaint">Complaint Text</label>
          <textarea id="complaint" name="complaint" placeholder="Type the complaint here..." required></textarea>
        </div>
        <div>
          <label for="address">Address</label>
          <input id="address" name="address" placeholder="Enter address, city, area, or unknown" required/>
        </div>
      </div>
      <div class="actions">
        <button class="submit" id="submitBtn" type="submit">Submit Complaint</button>
        <button class="clear" type="button" onclick="resetForm()">Clear</button>
        <span class="status" id="statusText"></span>
      </div>
    </form>

    <div class="result" id="resultBox">
      <div class="result-head">Analysis Result</div>
      <div id="resultContent"></div>
    </div>
  </section>
</main>

<script>
const form = document.getElementById("complaintForm");
const submitBtn = document.getElementById("submitBtn");
const statusText = document.getElementById("statusText");
const resultBox = document.getElementById("resultBox");
const resultContent = document.getElementById("resultContent");

function resetForm() {
  form.reset();
  resultBox.style.display = "none";
  statusText.textContent = "";
  statusText.className = "status";
}

function displayValue(value) {
  if (value === null || value === undefined || value === "" || value === "unknown") {
    return "Not identified";
  }
  return String(value).replaceAll("_", " ");
}

function confidencePercent(value) {
  const number = Number(value || 0);
  return Math.round(number * 100) + "%";
}

function priorityFor(crimeType, isJunk) {
  if (isJunk) return "Not applicable";
  const crime = String(crimeType || "").toLowerCase();
  if (crime === "sale") return "High";
  if (crime === "usage") return "Medium";
  return "Low";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderResult(data) {
  const isJunk = Boolean(data.is_junk);
  const verdictText = isJunk
    ? "This looks like junk or an irrelevant message."
    : "This complaint was accepted and saved.";
  const verdictClass = isJunk ? "junk" : "valid";
  const statusLabel = isJunk ? "Junk" : "Valid";
  const rawJson = escapeHtml(JSON.stringify(data, null, 2));

  resultContent.innerHTML = `
    <div class="summary">
      <div class="verdict ${verdictClass}">
        <span>${verdictText}</span>
        <span class="pill">${statusLabel}</span>
      </div>
      <div class="result-grid">
        <div class="result-item">
          <div class="result-label">Drug Type</div>
          <div class="result-value">${displayValue(data.drug_type)}</div>
        </div>
        <div class="result-item">
          <div class="result-label">Crime Type</div>
          <div class="result-value">${displayValue(data.crime_type)}</div>
        </div>
        <div class="result-item">
          <div class="result-label">Priority</div>
          <div class="result-value">${priorityFor(data.crime_type, isJunk)}</div>
        </div>
        <div class="result-item">
          <div class="result-label">City</div>
          <div class="result-value">${displayValue(data.city)}</div>
        </div>
        <div class="result-item">
          <div class="result-label">Location Detail</div>
          <div class="result-value">${displayValue(data.location_detail)}</div>
        </div>
        <div class="result-item">
          <div class="result-label">Address</div>
          <div class="result-value">${displayValue(data.address)}</div>
        </div>
        <div class="result-item">
          <div class="result-label">Drug Confidence</div>
          <div class="result-value">${confidencePercent(data.drug_confidence)}</div>
        </div>
        <div class="result-item">
          <div class="result-label">Crime Confidence</div>
          <div class="result-value">${confidencePercent(data.crime_confidence)}</div>
        </div>
      </div>
      <div class="result-note">
        Complaint text: ${escapeHtml(data.complaint_text || "")}
      </div>
      <button class="raw-toggle" type="button" onclick="toggleRawJson()">Show technical details</button>
      <pre class="raw-json" id="rawJson">${rawJson}</pre>
    </div>
  `;
}

function toggleRawJson() {
  const raw = document.getElementById("rawJson");
  const button = document.querySelector(".raw-toggle");
  const isOpen = raw.style.display === "block";
  raw.style.display = isOpen ? "none" : "block";
  button.textContent = isOpen ? "Show technical details" : "Hide technical details";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    complaint: document.getElementById("complaint").value.trim(),
    address: document.getElementById("address").value.trim() || "unknown"
  };
  submitBtn.disabled = true;
  statusText.textContent = "Submitting...";
  statusText.className = "status";
  resultBox.style.display = "none";

  try {
    const response = await fetch("/api/analyze-complaint", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(JSON.stringify(data));
    renderResult(data);
    resultBox.style.display = "block";
    statusText.textContent = "Saved to database.";
    statusText.className = "status ok";
  } catch (error) {
    resultContent.innerHTML = `<div class="summary"><div class="verdict junk"><span>${escapeHtml(error.message || error)}</span><span class="pill">Error</span></div></div>`;
    resultBox.style.display = "block";
    statusText.textContent = "Submit failed.";
    statusText.className = "status err";
  } finally {
    submitBtn.disabled = false;
  }
});
</script>
</body>
</html>
"""


def fetch_all_complaints():
    """Fetch every row from complaints table."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@router.get("/data")
def get_dashboard_data():
    """
    Single endpoint consumed by the HTML dashboard.
    Returns KPIs, chart data, map data, hotspots and the full complaints list.
    """
    rows = fetch_all_complaints()

    # ── Classify ──────────────────────────────────────────────────
    valid  = [r for r in rows if not r.get("is_junk")]
    junk   = [r for r in rows if r.get("is_junk")]

    def priority(r):
        ct = (r.get("crime_type") or "").lower()
        if ct == "sale":    return "HIGH"
        if ct == "usage":   return "MEDIUM"
        return "LOW"

    for r in valid:
        r["priority"] = priority(r)

    high_risk = [r for r in valid if r["priority"] == "HIGH"]

    # ── KPIs ──────────────────────────────────────────────────────
    kpis = {
        "total":   len(rows),
        "junk":    len(junk),
        "valid":   len(valid),
        "high":    len(high_risk),
    }

    # ── City counts ───────────────────────────────────────────────
    city_counter = Counter(
        r["city"].strip().title() for r in valid if r.get("city")
    )
    city_chart = {
        "labels": list(city_counter.keys()),
        "values": list(city_counter.values()),
    }

    # ── Drug counts ───────────────────────────────────────────────
    drug_counter = Counter(
        r["drug_type"].strip() for r in valid if r.get("drug_type")
    )
    drug_chart = {
        "labels": list(drug_counter.keys()),
        "values": list(drug_counter.values()),
    }

    # ── Crime counts ──────────────────────────────────────────────
    crime_counter = Counter(
        r["crime_type"].strip() for r in valid if r.get("crime_type")
    )
    crime_chart = {
        "labels": list(crime_counter.keys()),
        "values": list(crime_counter.values()),
    }

    # ── Priority counts ───────────────────────────────────────────
    prio_counter = Counter(r["priority"] for r in valid)
    priority_chart = {
        "labels": ["HIGH", "MEDIUM", "LOW"],
        "values": [prio_counter.get("HIGH", 0),
                   prio_counter.get("MEDIUM", 0),
                   prio_counter.get("LOW", 0)],
    }

    # ── Trend: last 14 days ───────────────────────────────────────
    today = datetime.today().date()
    trend_labels, trend_values = [], []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        count = sum(
            1 for r in valid
            if r.get("created_at") and
               (r["created_at"].date() if hasattr(r["created_at"], "date")
                else datetime.strptime(str(r["created_at"])[:10], "%Y-%m-%d").date()) == d
        )
        trend_labels.append(d.strftime("%d %b"))
        trend_values.append(count)

    trend_chart = {"labels": trend_labels, "values": trend_values}

    # ── Map data ──────────────────────────────────────────────────
    CITY_COORDS = {
        "chennai":      (13.0827, 80.2707),
        "kancheepuram": (12.8342, 79.7036),
        "madurai":      (9.9252,  78.1198),
        "coimbatore":   (11.0168, 76.9558),
        "trichy":       (10.7905, 78.7047),
        "salem":        (11.6643, 78.1460),
        "vellore":      (12.9165, 79.1325),
        "tirunelveli":  (8.7139,  77.7567),
        "erode":        (11.3410, 77.7172),
        "thanjavur":    (10.7870, 79.1378),
    }

    city_map_agg = {}
    for r in valid:
        city_key = (r.get("city") or "").strip().lower()
        coords = CITY_COORDS.get(city_key)
        if not coords:
            continue
        if city_key not in city_map_agg:
            city_map_agg[city_key] = {
                "city": city_key.title(),
                "lat":  coords[0],
                "lon":  coords[1],
                "count": 0,
                "top_crime": Counter(),
            }
        city_map_agg[city_key]["count"] += 1
        city_map_agg[city_key]["top_crime"][r.get("crime_type", "unknown")] += 1

    map_data = []
    for v in city_map_agg.values():
        top_crime = v["top_crime"].most_common(1)
        map_data.append({
            "city":      v["city"],
            "lat":       v["lat"],
            "lon":       v["lon"],
            "count":     v["count"],
            "top_crime": top_crime[0][0] if top_crime else "unknown",
        })

    # ── Hotspots ──────────────────────────────────────────────────
    hs_counter = Counter(
        (r.get("city", ""), r.get("location_detail", ""))
        for r in valid if r.get("city") and r.get("location_detail")
    )
    hotspots = [
        {"city": k[0].title(), "location": k[1], "count": v}
        for k, v in hs_counter.most_common(15)
    ]

    # ── High-risk sale zones ──────────────────────────────────────
    sale_counter = Counter(
        (r.get("city", ""), r.get("location_detail", ""))
        for r in valid
        if (r.get("crime_type") or "").lower() == "sale"
        and r.get("city") and r.get("location_detail")
    )
    high_risk_zones = [
        {"city": k[0].title(), "location": k[1], "count": v}
        for k, v in sale_counter.most_common()
        if v >= 2
    ]

    # ── Complaints list (latest 200) ──────────────────────────────
    complaints = []
    for r in rows[:200]:
        created = r.get("created_at")
        complaints.append({
            "date":     str(created)[:10] if created else "",
            "city":     (r.get("city") or "").title(),
            "location": r.get("location_detail") or "",
            "drug":     r.get("drug_type") or "",
            "crime":    r.get("crime_type") or "",
            "priority": priority(r) if not r.get("is_junk") else "LOW",
            "junk":     bool(r.get("is_junk")),
        })

    return {
        "kpis":           kpis,
        "city_chart":     city_chart,
        "drug_chart":     drug_chart,
        "crime_chart":    crime_chart,
        "priority_chart": priority_chart,
        "trend_chart":    trend_chart,
        "map_data":       map_data,
        "hotspots":       hotspots,
        "high_risk_zones":high_risk_zones,
        "complaints":     complaints,
    }


# ─────────────────────────────────────────
# HOW TO WIRE THIS INTO main.py
# Add these two lines to your existing main.py:
#
#   from app.routes import dashboard
#   app.include_router(dashboard.router)
#
# And add CORS so the HTML file can call the API:
#
#   from fastapi.middleware.cors import CORSMiddleware
#   app.add_middleware(
#       CORSMiddleware,
#       allow_origins=["*"],       # tighten in production
#       allow_methods=["*"],
#       allow_headers=["*"],
#   )
# ─────────────────────────────────────────
