# import streamlit as st
# import pandas as pd
# import mysql.connector

# import time

# # st.set_page_config(page_title="Drug AI Dashboard", layout="wide")

# # # Refresh every 10 seconds safely
# # st_autorefresh = st.empty()

# # import time
# # time.sleep(10)
# # st.rerun()

# # Approx coordinates for TN cities (extend anytime)
# CITY_COORDS = {
#     "chennai": (13.0827, 80.2707),
#     "kancheepuram": (12.8342, 79.7036),
#     "madurai": (9.9252, 78.1198),
#     "coimbatore": (11.0168, 76.9558),
#     "trichy": (10.7905, 78.7047),
#     "salem": (11.6643, 78.1460),
#     "vellore": (12.9165, 79.1325)
# }
# # DB connection
# def get_data():
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="drug_user",
#         password="drug123",
#         database="drug_ai"
#     )

#     query = "SELECT * FROM complaints"
#     df = pd.read_sql(query, conn)
#     conn.close()

#     # ✅ Fix data types properly
#     df['is_junk'] = pd.to_numeric(df['is_junk'], errors='coerce').fillna(0).astype(int)

#     # Convert only text columns
#     text_cols = ['complaint_text', 'drug_type', 'crime_type', 'city', 'location_detail']
#     # for col in text_cols:
#     #     df[col] = df[col].astype(str)
#     for col in text_cols:
#         df[col] = df[col].fillna("unknown").astype(str)

#     return df



# st.set_page_config(page_title="Drug AI Dashboard", layout="wide")

# st.title("🚨 Drug-Free TN AI Dashboard")

# df = get_data()

# # Use only valid complaints
# map_df = df[df['is_junk'] == 0].copy()

# # Normalize city
# map_df['city'] = map_df['city'].str.lower().str.strip()

# # Map coordinates
# def get_lat(city):
#     return CITY_COORDS.get(city, (None, None))[0]

# def get_lon(city):
#     return CITY_COORDS.get(city, (None, None))[1]

# map_df['lat'] = map_df['city'].apply(get_lat)
# map_df['lon'] = map_df['city'].apply(get_lon)

# # Drop rows without coords
# map_df = map_df.dropna(subset=['lat', 'lon'])

# if df.empty:
#     st.warning("No data available")
#     st.stop()

# # ---------------- METRICS ----------------
# col1, col2, col3 = st.columns(3)

# total = len(df)
# junk = df['is_junk'].sum()
# valid = total - junk

# col1.metric("Total Complaints", total)
# col2.metric("Junk Complaints", junk)
# col3.metric("Valid Complaints", valid)


# st.sidebar.header("🔍 Filters")

# selected_city = st.sidebar.selectbox(
#     "Select City",
#     ["All"] + list(df['city'].unique())
# )

# if selected_city != "All":
#     df = df[df['city'] == selected_city]
# # ---------------- CITY ----------------
# st.subheader("📍 Complaints by City")

# city_data = (
#     df[df['is_junk'] == 0]['city']
#     .value_counts()
#     .reset_index()
# )
# city_data.columns = ['city', 'count']

# st.bar_chart(city_data.set_index('city'))

# # ---------------- DRUG ----------------
# st.subheader("💊 Drug Type Distribution")

# drug_data = (
#     df[df['is_junk'] == 0]['drug_type']
#     .value_counts()
#     .reset_index()
# )
# drug_data.columns = ['drug', 'count']

# st.bar_chart(drug_data.set_index('drug'))

# # ---------------- CRIME ----------------
# st.subheader("🚔 Crime Type Distribution")

# crime_data = (
#     df[df['is_junk'] == 0]['crime_type']
#     .value_counts()
#     .reset_index()
# )
# crime_data.columns = ['crime', 'count']

# st.bar_chart(crime_data.set_index('crime'))

# # ---------------- MAP ----------------

# # st.subheader("🗺️ Complaint Map")

# # if not map_df.empty:
# #     st.map(map_df[['lat', 'lon']])
# # else:
# #     st.warning("No location data available for map")
# import pydeck as pdk

# st.subheader("🗺️ Complaint Map (Intensity View)")

# if not map_df.empty:
#     map_grouped = (
#         map_df.groupby(['city', 'lat', 'lon'])
#         .size()
#         .reset_index(name='count')
#     )

#     layer = pdk.Layer(
#         "ScatterplotLayer",
#         data=map_grouped,
#         get_position='[lon, lat]',
#         get_radius='count * 20000',  # 🔥 intensity
#         get_fill_color='[255, 0, 0, 160]',
#         pickable=True
#     )

#     view_state = pdk.ViewState(
#         latitude=11.1271,
#         longitude=78.6569,
#         zoom=6,
#     )

#     st.pydeck_chart(pdk.Deck(
#         layers=[layer],
#         initial_view_state=view_state,
#         tooltip={"text": "{city}\nComplaints: {count}"}
#     ))

# else:
#     st.warning("No location data available")

# st.subheader("🔥 Hotspot Areas")

# hotspots = (
#     df[df['is_junk'] == 0]
#     .groupby(['city', 'location_detail'])
#     .size()
#     .reset_index(name='count')
#     .sort_values(by='count', ascending=False)
# )

# # Show only top hotspots
# # top_hotspots = hotspots[hotspots['count'] > 1]
# top_hotspots = hotspots[hotspots['count'] >= 1]

# if not top_hotspots.empty:
#     st.dataframe(top_hotspots)
# else:
#     st.info("No hotspots detected yet")

# st.subheader("🚨 High Risk Alerts")

# risk_data = (
#     df[(df['is_junk'] == 0) & (df['crime_type'] == 'sale')]
#     .groupby(['city', 'location_detail'])
#     .size()
#     .reset_index(name='count')
#     .sort_values(by='count', ascending=False)
# )

# high_risk = risk_data[risk_data['count'] >= 2]

# if not high_risk.empty:
#     st.error("⚠️ High Risk Drug Sale Areas Detected!")
#     st.dataframe(high_risk)
# else:
#     st.success("No high-risk areas currently")

# # ---------------- TABLE ----------------
# st.subheader("📋 All Complaints")



# def get_priority(row):
#     if row['crime_type'] == 'sale':
#         return "HIGH"
#     elif row['crime_type'] == 'usage':
#         return "MEDIUM"
#     return "LOW"

# df['priority'] = df.apply(get_priority, axis=1)

# st.dataframe(df.sort_values(by="created_at", ascending=False))



import streamlit as st
import pandas as pd
import mysql.connector
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# ─────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Drug-Free Tamil Nadu | AI Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --navy:      #0B1C3B;
    --navy-mid:  #122347;
    --navy-card: #172a52;
    --gold:      #C9941A;
    --gold-lt:   #E8B84B;
    --red-alert: #D94040;
    --green-ok:  #2E7D5C;
    --text-main: #EEF2FF;
    --text-muted:#A8B8D8;
    --border:    rgba(201,148,26,0.25);
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy) !important;
    color: var(--text-main) !important;
}

/* ── App background ── */
.stApp {
    background: linear-gradient(160deg, #0B1C3B 0%, #0d1f42 50%, #111933 100%) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2050 0%, #0B1C3B 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-main) !important; }

/* ── Header banner ── */
.gov-header {
    background: linear-gradient(135deg, #0d2354 0%, #122347 60%, #0B1C3B 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 4px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(201,148,26,0.15);
    position: relative;
    overflow: hidden;
}
.gov-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.gov-header-text h1 {
    font-family: 'Crimson Pro', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #fff !important;
    margin: 0 0 4px 0;
    letter-spacing: 0.02em;
}
.gov-header-text p {
    font-size: 0.82rem;
    color: var(--text-muted) !important;
    margin: 0;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.gov-emblem {
    font-size: 3.5rem;
    filter: drop-shadow(0 0 12px rgba(201,148,26,0.5));
}
.live-badge {
    margin-left: auto;
    background: rgba(46,125,92,0.2);
    border: 1px solid var(--green-ok);
    color: #4ade80 !important;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    animation: pulse-green 2s infinite;
}
@keyframes pulse-green {
    0%,100% { box-shadow: 0 0 0 0 rgba(46,125,92,0.5); }
    50%      { box-shadow: 0 0 0 6px rgba(46,125,92,0); }
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, var(--navy-card), #1a3060);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.metric-card::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
}
.metric-card.total::after  { background: linear-gradient(90deg, var(--gold), transparent); }
.metric-card.junk::after   { background: linear-gradient(90deg, #6B7280, transparent); }
.metric-card.valid::after  { background: linear-gradient(90deg, var(--green-ok), transparent); }
.metric-card.high::after   { background: linear-gradient(90deg, var(--red-alert), transparent); }
.metric-number {
    font-family: 'Crimson Pro', serif;
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted) !important;
}
.metric-icon {
    position: absolute; top: 16px; right: 20px;
    font-size: 2rem; opacity: 0.18;
}

/* ── Section headings ── */
.section-title {
    font-family: 'Crimson Pro', serif;
    font-size: 1.35rem;
    font-weight: 600;
    color: #fff !important;
    border-left: 4px solid var(--gold);
    padding-left: 14px;
    margin: 28px 0 16px 0;
    letter-spacing: 0.01em;
}

/* ── Alert boxes ── */
.alert-high {
    background: rgba(217,64,64,0.12);
    border: 1px solid rgba(217,64,64,0.5);
    border-left: 4px solid var(--red-alert);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.alert-ok {
    background: rgba(46,125,92,0.1);
    border: 1px solid rgba(46,125,92,0.4);
    border-left: 4px solid var(--green-ok);
    border-radius: 8px;
    padding: 14px 18px;
}

/* ── Table styling ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Plotly chart backgrounds ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── Selectbox / widgets ── */
.stSelectbox > div > div {
    background: var(--navy-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-main) !important;
    border-radius: 8px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 3px; }

/* ── Footer ── */
.gov-footer {
    text-align: center;
    padding: 24px;
    margin-top: 40px;
    border-top: 1px solid var(--border);
    color: var(--text-muted) !important;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
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

PRIORITY_COLOR = {"HIGH": "#D94040", "MEDIUM": "#E8B84B", "LOW": "#4ade80"}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#A8B8D8", size=12),
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.1)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#A8B8D8")),
)


# ─────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────
@st.cache_data(ttl=30)
def get_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="drug_user",
            password="drug123",
            database="drug_ai"
        )
        df = pd.read_sql("SELECT * FROM complaints", conn)
        conn.close()
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()

    df['is_junk'] = pd.to_numeric(df['is_junk'], errors='coerce').fillna(0).astype(int)
    for col in ['complaint_text', 'drug_type', 'crime_type', 'city', 'location_detail']:
        df[col] = df[col].fillna("unknown").astype(str)

    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

    return df


def enrich(df):
    df = df.copy()
    df['city_norm'] = df['city'].str.lower().str.strip()

    def coords(city):
        return CITY_COORDS.get(city, (None, None))

    df['lat'] = df['city_norm'].apply(lambda c: coords(c)[0])
    df['lon'] = df['city_norm'].apply(lambda c: coords(c)[1])

    def priority(row):
        if row['crime_type'] == 'sale':   return "HIGH"
        if row['crime_type'] == 'usage':  return "MEDIUM"
        return "LOW"

    df['priority'] = df.apply(priority, axis=1)
    return df


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="gov-header">
    <div class="gov-emblem">🛡️</div>
    <div class="gov-header-text">
        <h1>Drug-Free Tamil Nadu — AI Intelligence Dashboard</h1>
        <p>Tamil Nadu Government &nbsp;·&nbsp; Social Defence Department &nbsp;·&nbsp; Narcotics Intelligence Unit</p>
    </div>
    <div class="live-badge">● Live</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
df_raw = get_data()
if df_raw.empty:
    st.warning("No data available. Please check your database connection.")
    st.stop()

df_all = enrich(df_raw)
valid_all = df_all[df_all['is_junk'] == 0]


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 20px 0;'>
        <div style='font-size:2.2rem;'>🛡️</div>
        <div style='font-family: Crimson Pro, serif; font-size:1.1rem; color:#E8B84B; font-weight:600;'>
            Drug-Free TN
        </div>
        <div style='font-size:0.7rem; color:#A8B8D8; letter-spacing:0.08em; text-transform:uppercase;'>
            Intelligence Platform
        </div>
    </div>
    <hr style='border-color:rgba(201,148,26,0.2);'>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔍 Filters")

    city_options = ["All Cities"] + sorted(df_all['city'].str.title().unique().tolist())
    selected_city = st.selectbox("District / City", city_options)

    crime_options = ["All Types"] + sorted(valid_all['crime_type'].unique().tolist())
    selected_crime = st.selectbox("Crime Type", crime_options)

    drug_options = ["All Drugs"] + sorted(valid_all['drug_type'].unique().tolist())
    selected_drug = st.selectbox("Drug Category", drug_options)

    priority_options = ["All Priorities", "HIGH", "MEDIUM", "LOW"]
    selected_priority = st.selectbox("Priority Level", priority_options)

    st.markdown("<hr style='border-color:rgba(201,148,26,0.2);'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.72rem; color:#A8B8D8; text-align:center;'>
        Last refreshed<br>
        <span style='color:#E8B84B;'>{datetime.now().strftime('%d %b %Y, %H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("""
    <div style='margin-top:20px; font-size:0.7rem; color:#A8B8D8; text-align:center;'>
        <a href='https://drugfreetamilnadu.tn.gov.in/en' target='_blank'
           style='color:#C9941A; text-decoration:none;'>
           🌐 drugfreetamilnadu.tn.gov.in
        </a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────
df = df_all.copy()

if selected_city != "All Cities":
    df = df[df['city'].str.title() == selected_city]
if selected_crime != "All Types":
    df = df[df['crime_type'] == selected_crime]
if selected_drug != "All Drugs":
    df = df[df['drug_type'] == selected_drug]
if selected_priority != "All Priorities":
    df = df[df['priority'] == selected_priority]

valid = df[df['is_junk'] == 0]


# ─────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────
total   = len(df)
junk_n  = int(df['is_junk'].sum())
valid_n = total - junk_n
high_n  = int((valid['priority'] == 'HIGH').sum())

c1, c2, c3, c4 = st.columns(4)

for col, label, value, css_cls, icon, color in [
    (c1, "Total Complaints",  total,   "total", "📋", "#E8B84B"),
    (c2, "Junk / Spam",       junk_n,  "junk",  "🗑️", "#6B7280"),
    (c3, "Valid Complaints",  valid_n, "valid", "✅", "#4ade80"),
    (c4, "High-Risk Cases",   high_n,  "high",  "⚠️", "#D94040"),
]:
    col.markdown(f"""
    <div class="metric-card {css_cls}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-number" style="color:{color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# ROW 1 — City bar + Drug donut
# ─────────────────────────────────────────
st.markdown('<div class="section-title">📊 Complaint Analytics</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    city_data = (
        valid['city'].str.title().value_counts().reset_index()
    )
    city_data.columns = ['City', 'Complaints']

    fig_city = px.bar(
        city_data, x='City', y='Complaints',
        color='Complaints',
        color_continuous_scale=[[0, '#1a3060'], [0.5, '#C9941A'], [1, '#E8B84B']],
        title="Complaints by District",
    )
    fig_city.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                           title_font=dict(family="Crimson Pro", size=16, color="#fff"))
    fig_city.update_traces(marker_line_width=0)
    st.plotly_chart(fig_city, use_container_width=True)

with col_right:
    drug_data = valid['drug_type'].value_counts().reset_index()
    drug_data.columns = ['Drug', 'Count']

    fig_drug = px.pie(
        drug_data, names='Drug', values='Count',
        title="Drug Category Breakdown",
        hole=0.55,
        color_discrete_sequence=['#C9941A','#E8B84B','#4B8FD4','#D94040','#2E7D5C','#7C5CBF'],
    )
    fig_drug.update_layout(**PLOTLY_LAYOUT,
                           title_font=dict(family="Crimson Pro", size=16, color="#fff"))
    fig_drug.update_traces(textfont_color="#fff", pull=[0.04]*len(drug_data))
    st.plotly_chart(fig_drug, use_container_width=True)


# ─────────────────────────────────────────
# ROW 2 — Crime type + Priority breakdown
# ─────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    crime_data = valid['crime_type'].value_counts().reset_index()
    crime_data.columns = ['Crime Type', 'Count']

    fig_crime = px.bar(
        crime_data, x='Count', y='Crime Type', orientation='h',
        title="Crime Type Distribution",
        color='Count',
        color_continuous_scale=[[0,'#1a3060'],[1,'#D94040']],
    )
    fig_crime.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                            title_font=dict(family="Crimson Pro", size=16, color="#fff"))
    fig_crime.update_traces(marker_line_width=0)
    st.plotly_chart(fig_crime, use_container_width=True)

with col_b:
    priority_data = valid['priority'].value_counts().reset_index()
    priority_data.columns = ['Priority', 'Count']
    p_colors = {'HIGH': '#D94040', 'MEDIUM': '#E8B84B', 'LOW': '#4ade80'}
    colors = [p_colors.get(p, '#6B7280') for p in priority_data['Priority']]

    fig_priority = go.Figure(go.Bar(
        x=priority_data['Priority'], y=priority_data['Count'],
        marker_color=colors,
        text=priority_data['Count'],
        textposition='outside',
        textfont=dict(color='#fff'),
    ))
    fig_priority.update_layout(
        **PLOTLY_LAYOUT, title="Cases by Priority Level",
        title_font=dict(family="Crimson Pro", size=16, color="#fff"),
    )
    st.plotly_chart(fig_priority, use_container_width=True)


# ─────────────────────────────────────────
# ROW 3 — Trend over time (DATE ONLY FIXED)
# ─────────────────────────────────────────
if 'created_at' in valid.columns and valid['created_at'].notna().sum() > 1:
    st.markdown('<div class="section-title">📈 Complaint Trend</div>', unsafe_allow_html=True)

    # Remove time
    valid['created_at'] = pd.to_datetime(valid['created_at']).dt.floor('D')

    trend = (
        valid.set_index('created_at')
        .resample('D')
        .size()
        .reset_index(name='Complaints')
        .rename(columns={'created_at': 'Date'})
    )

    fig_trend = px.area(
        trend, x='Date', y='Complaints',
        title="Daily Complaint Volume",
        color_discrete_sequence=['#C9941A'],
    )

    fig_trend.update_traces(
        fillcolor='rgba(201,148,26,0.12)',
        line=dict(color='#C9941A', width=2),
    )

    fig_trend.update_layout(
        **PLOTLY_LAYOUT,
        title_font=dict(family="Crimson Pro", size=16, color="#fff")
    )

    # ✅ FIX: Remove time from x-axis display
    fig_trend.update_xaxes(
        tickformat="%d %b %Y"
    )

    st.plotly_chart(fig_trend, use_container_width=True)
# ─────────────────────────────────────────
# MAP (ENHANCED VERSION)
# ─────────────────────────────────────────
import pydeck as pdk
import streamlit as st

st.markdown('<div class="section-title">🗺️ Geographic Intelligence Map</div>', unsafe_allow_html=True)

map_df = valid.dropna(subset=['lat', 'lon'])

if not map_df.empty:

    map_grouped = (
        map_df.groupby(['city', 'lat', 'lon'])
        .size()
        .reset_index(name='count')
    )

    # Normalize radius so large cities don't dominate
    max_count = map_grouped['count'].max()
    map_grouped['radius'] = map_grouped['count'] / max_count * 40000 + 5000  # min 5km, max 45km

    # ── Scatter layer ──────────────────────────────────
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_grouped,
        get_position='[lon, lat]',
        get_radius='radius',
        get_fill_color='[217, 64, 64, 160]',
        get_line_color='[255, 200, 0, 220]',
        line_width_min_pixels=2,
        pickable=True,
        auto_highlight=True,
    )

    # ── Text label layer ───────────────────────────────
    text_layer = pdk.Layer(
        "TextLayer",
        data=map_grouped,
        get_position='[lon, lat]',
        get_text='city',
        get_size=13,
        get_color='[255, 255, 255, 220]',
        get_alignment_baseline='"bottom"',
        pickable=False,
    )

    view = pdk.ViewState(
        latitude=11.1271,
        longitude=78.6569,
        zoom=6,
        pitch=0,
        bearing=0,
    )

    # ✅ FIX 1: Use a valid open-source tile style (no Mapbox token needed)
    # ✅ FIX 2: Proper style URL format
    deck = pdk.Deck(
        layers=[scatter_layer, text_layer],
        initial_view_state=view,
        tooltip={
            "html": """
                <div style='font-family:sans-serif; padding:6px 10px;
                            background:#1a1a2e; border-radius:6px;
                            border:1px solid #e53e3e; color:white;'>
                    <b style='color:#f6ad55'>📍 {city}</b><br/>
                    <span style='color:#fc8181'>🔴 Complaints:</span>
                    <b style='color:white'> {count}</b>
                </div>
            """,
            "style": {"backgroundColor": "transparent", "color": "white"}
        },
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        # ↑ FREE, no token needed. Other options:
        # "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"  ← light theme
        # "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"   ← colorful
    )

    st.pydeck_chart(deck, use_container_width=True)

    # ── Summary below the map ──────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("📍 Cities Mapped", len(map_grouped))
    col2.metric("🔺 Highest Complaints", f"{map_grouped['count'].max()} — {map_grouped.loc[map_grouped['count'].idxmax(), 'city']}")
    col3.metric("📊 Total Geo-tagged", int(map_grouped['count'].sum()))

else:
    st.info("No geo-tagged complaints available.")
# ─────────────────────────────────────────
# HOTSPOTS
# ─────────────────────────────────────────
st.markdown('<div class="section-title">🔥 Hotspot Intelligence</div>', unsafe_allow_html=True)

hotspots = (
    valid.groupby(['city', 'location_detail'])
    .size()
    .reset_index(name='Incidents')
    .sort_values(by='Incidents', ascending=False)
)
hotspots.columns = ['District', 'Location', 'Incidents']

col_hot, col_risk = st.columns(2)

with col_hot:
    st.markdown("**All Hotspot Areas**")
    st.dataframe(
        hotspots.head(15).style
        .background_gradient(subset=['Incidents'], cmap='YlOrRd')
        .set_properties(**{'background-color': '#ffffff', 'color': '#000000'}),
        use_container_width=True,
    )

with col_risk:
    risk_data = (
        valid[valid['crime_type'] == 'sale']
        .groupby(['city', 'location_detail'])
        .size()
        .reset_index(name='Sale Incidents')
        .sort_values(by='Sale Incidents', ascending=False)
    )
    risk_data.columns = ['District', 'Location', 'Sale Incidents']
    high_risk = risk_data[risk_data['Sale Incidents'] >= 2]

    st.markdown("**🚨 High-Risk Drug Sale Zones**")
    if not high_risk.empty:
        st.markdown(f"""
        <div class="alert-high">
            ⚠️ <strong>{len(high_risk)} high-risk drug sale zone(s) detected</strong>
            — immediate attention required.
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(high_risk.style
                     .highlight_max(subset=['Sale Incidents'], color='rgba(217,64,64,0.3)')
                     .set_properties(**{'background-color': '#ffffff', 'color': '#000000'}),
                     use_container_width=True)
    else:
        st.markdown("""
        <div class="alert-ok">
            ✅ No high-risk drug sale zones detected under current filters.
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# FULL COMPLAINTS TABLE
# ─────────────────────────────────────────
st.markdown('<div class="section-title">📋 Complaints Registry</div>', unsafe_allow_html=True)

display_cols = ['city', 'location_detail', 'drug_type', 'crime_type', 'priority', 'is_junk']
if 'created_at' in df.columns:
    display_cols = ['created_at'] + display_cols

show_df = df[display_cols].copy()
show_df.columns = [c.replace('_', ' ').title() for c in display_cols]

if 'Priority' in show_df.columns:
    def style_priority(val):
        color = PRIORITY_COLOR.get(val, '#fff')
        return f'color: {color}; font-weight: 600;'

    # styled = show_df.style.applymap(style_priority, subset=['Priority'])
    styled = show_df.style.map(style_priority, subset=['Priority'])
else:
    styled = show_df.style

# st.dataframe(styled, use_container_width=True, height=400)
st.dataframe(show_df, width="stretch", height=400)

# Export button
csv = show_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Export to CSV",
    data=csv,
    file_name=f"drugfreetn_complaints_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv",
)


# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div class="gov-footer">
    Government of Tamil Nadu &nbsp;·&nbsp; Social Defence Department &nbsp;·&nbsp; Narcotics Intelligence Unit<br>
    <a href='https://drugfreetamilnadu.tn.gov.in/en' target='_blank'
       style='color:#C9941A; text-decoration:none;'>
       drugfreetamilnadu.tn.gov.in
    </a>
    &nbsp;·&nbsp; All data is confidential and for official use only.
</div>
""", unsafe_allow_html=True)