import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import pickle

st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Fixed dark theme colors ──────────────────────────────────
BG         = "#0f1117"
SURFACE    = "#1a1d2e"
SURFACE2   = "#252840"
BORDER     = "#2e3150"
TEXT       = "#f0f2ff"
MUTED      = "#8b90b8"
ACCENT     = "#4f8ef7"
ACCENT2    = "#f7c948"
GREEN      = "#2ecc71"
RED        = "#e74c3c"
FILL_BLUE  = "rgba(79,142,247,0.15)"
PTHEME     = "plotly_dark"

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main, .main > div {
    background-color: #0f1117 !important;
    color: #f0f2ff !important;
    font-family: 'Inter', sans-serif;
    scroll-behavior: auto !important;
}
/* Stop the page from auto-scrolling / jumping on every widget interaction */
[data-testid="stAppViewContainer"] {
    overflow-anchor: none !important;
}
.main .block-container {
    overflow-anchor: none !important;
}
* { overflow-anchor: none !important; }
/* Prevent layout shift while charts/widgets re-render */
[data-testid="stVerticalBlock"] { overflow-anchor: none !important; }
[data-testid="stSidebar"] {
    background-color: #1a1d2e !important;
    border-right: 1px solid #2e3150 !important;
}
[data-testid="stSidebar"] * { color: #f0f2ff !important; }
[data-testid="stHeader"] { background-color: #0f1117 !important; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px;
    background-color: #0f1117 !important;
}
section[data-testid="stSidebar"] > div { background-color: #1a1d2e !important; }

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f0f2ff !important;
}
p, li, span, div { color: #f0f2ff; }
[data-testid="stCaption"] { color: #8b90b8 !important; }

.stTabs [data-baseweb="tab-list"] {
    background-color: #252840 !important;
    border-radius: 12px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    border-radius: 8px !important;
    color: #8b90b8 !important;
    font-weight: 500;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background-color: #4f8ef7 !important;
    color: #ffffff !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: #0f1117 !important;
    padding-top: 20px !important;
}
div[data-testid="metric-container"] {
    background-color: #1a1d2e !important;
    border: 1px solid #2e3150 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}
div[data-testid="metric-container"] label {
    color: #8b90b8 !important;
    font-size: 13px !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f0f2ff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 26px !important;
}
.stSelectbox > div > div {
    background-color: #1a1d2e !important;
    border-color: #2e3150 !important;
    color: #f0f2ff !important;
    border-radius: 10px !important;
}
.stSelectbox svg { fill: #8b90b8 !important; }

/* ── Dropdown popup list ── */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] * {
    background-color: #1a1d2e !important;
    color: #f0f2ff !important;
}
[data-baseweb="select"] * {
    background-color: #1a1d2e !important;
    color: #f0f2ff !important;
}
ul[data-baseweb="menu"] {
    background-color: #1a1d2e !important;
    border: 1px solid #2e3150 !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
ul[data-baseweb="menu"] li {
    background-color: #1a1d2e !important;
    color: #f0f2ff !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
}
ul[data-baseweb="menu"] li:hover,
ul[data-baseweb="menu"] li[aria-selected="true"] {
    background-color: #252840 !important;
    color: #4f8ef7 !important;
}
/* Selected value text inside the box */
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: #f0f2ff !important;
}
/* Search input inside dropdown */
input[aria-autocomplete="list"] {
    background-color: #1a1d2e !important;
    color: #f0f2ff !important;
    border-color: #2e3150 !important;
}
/* Slider labels and numbers */
[data-testid="stSlider"] p,
[data-testid="stSlider"] span,
[data-testid="stSlider"] div {
    color: #f0f2ff !important;
}
/* Number input text */
[data-testid="stNumberInput"] input {
    background-color: #1a1d2e !important;
    color: #f0f2ff !important;
    border-color: #2e3150 !important;
    border-radius: 10px !important;
}
/* All text globally forced dark-safe */
.stMarkdown p, .stText, label, .stWidgetLabel {
    color: #f0f2ff !important;
}
[data-testid="stWidgetLabel"] p {
    color: #8b90b8 !important;
    font-size: 13px !important;
}
/* Radio buttons */
[data-testid="stRadio"] label {
    color: #f0f2ff !important;
}
[data-testid="stRadio"] div[role="radiogroup"] label {
    background-color: #1a1d2e !important;
    border: 1px solid #2e3150 !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    margin-right: 8px !important;
}
.stNumberInput > div > div > input {
    background-color: #1a1d2e !important;
    border-color: #2e3150 !important;
    color: #f0f2ff !important;
    border-radius: 10px !important;
}
.stSlider > div > div > div { background-color: #4f8ef7 !important; }
.stButton > button {
    background-color: #4f8ef7 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 8px 20px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover { background-color: #3a7de8 !important; }
hr { border-color: #2e3150 !important; }

.hero-banner {
    background: #1a1d2e;
    border: 1px solid #2e3150;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #f0f2ff;
    margin: 0 0 6px 0;
    line-height: 1.3;
}
.hero-sub { font-size: 14px; color: #8b90b8; margin: 0; }
.badge {
    display: inline-block;
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 999px;
    background: #252840;
    color: #8b90b8;
    border: 1px solid #2e3150;
    margin-right: 6px;
    margin-top: 10px;
}
.section-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8b90b8;
    margin-bottom: 12px;
    margin-top: 4px;
}
.prob-box {
    background: #1a1d2e;
    border: 1px solid #2e3150;
    border-radius: 16px;
    padding: 24px 28px;
    margin: 8px 0 16px;
}
.prob-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 56px;
    font-weight: 700;
    margin: 0;
    line-height: 1.1;
}
.prob-verdict { font-size: 15px; font-weight: 500; margin: 6px 0 16px; }
.win-bar-bg {
    background: #252840;
    border-radius: 999px;
    height: 12px;
    width: 100%;
    overflow: hidden;
    margin: 4px 0 6px;
}
.win-bar-fill { height: 12px; border-radius: 999px; }
.bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #8b90b8;
    margin-top: 2px;
}
.insight-box {
    background: #1a1d2e;
    border-left: 3px solid #4f8ef7;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 14px 0;
    font-size: 14px;
    color: #f0f2ff;
    line-height: 1.7;
}
.rec-box {
    background: #1a1d2e;
    border: 1px solid #2e3150;
    border-radius: 14px;
    padding: 22px 28px;
    margin: 8px 0 16px;
}
.rec-label { font-size: 12px; color: #8b90b8; margin-bottom: 6px; letter-spacing: 0.04em; }
.rec-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 700;
}
.sidebar-brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #f0f2ff;
    margin-bottom: 2px;
}
.sidebar-sub { font-size: 12px; color: #8b90b8; margin-bottom: 20px; }
.footer-note { font-size: 11px; color: #8b90b8; line-height: 1.8; }
.surprise-box {
    background: linear-gradient(135deg, #252840 0%, #1a1d2e 100%);
    border: 1px solid #4f8ef7;
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
}
.surprise-icon { font-size: 22px; line-height: 1.2; }
.surprise-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #f7c948;
    margin-bottom: 4px;
}
.surprise-text { font-size: 14px; color: #f0f2ff; line-height: 1.6; }
.compare-card {
    background: #1a1d2e;
    border: 1px solid #2e3150;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 8px;
}
.compare-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
}
.sim-arrow {
    font-size: 22px;
    color: #8b90b8;
    text-align: center;
    padding-top: 36px;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">IPL Analyser</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Win Predictor and Strategy Tool</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="footer-note">Python · scikit-learn · Streamlit · Plotly<br>Dataset: IPL 2007 to 2024</div>', unsafe_allow_html=True)

# ── Auto-build ipl.db from CSVs if it doesn't exist yet ──────
import os

def venue_map_lookup(v):
    VENUE_MAP = {
        "M Chinnaswamy Stadium": "Chinnaswamy",
        "M.Chinnaswamy Stadium": "Chinnaswamy",
        "M. Chinnaswamy Stadium": "Chinnaswamy",
        "Wankhede Stadium": "Wankhede",
        "Eden Gardens": "Eden Gardens",
        "Feroz Shah Kotla": "Kotla",
        "Arun Jaitley Stadium": "Kotla",
        "Arun Jaitley Stadium, Delhi": "Kotla",
        "MA Chidambaram Stadium": "Chepauk",
        "MA Chidambaram Stadium, Chepauk": "Chepauk",
        "MA Chidambaram Stadium, Chepauk, Chennai": "Chepauk",
        "Rajiv Gandhi International Stadium": "Hyderabad",
        "Rajiv Gandhi International Stadium, Uppal": "Hyderabad",
        "Punjab Cricket Association Stadium, Mohali": "Mohali",
        "Punjab Cricket Association IS Bindra Stadium": "Mohali",
        "Punjab Cricket Association IS Bindra Stadium, Mohali": "Mohali",
        "Sawai Mansingh Stadium": "Jaipur",
        "DY Patil Stadium": "DY Patil",
        "Brabourne Stadium": "Brabourne",
        "Narendra Modi Stadium": "Narendra Modi",
        "Narendra Modi Stadium, Ahmedabad": "Narendra Modi",
        "Maharashtra Cricket Association Stadium": "MCA Pune",
        "Himachal Pradesh Cricket Association Stadium": "HPCA Dharamsala",
    }
    return VENUE_MAP.get(v, v)

def build_database():
    m = pd.read_csv("matches.csv")
    d = pd.read_csv("deliveries.csv.gz", compression="gzip")

    m["date"]  = pd.to_datetime(m["date"], dayfirst=True)
    m["month"] = m["date"].dt.month
    m["year"]  = m["date"].dt.year
    m["venue_clean"] = m["venue"].apply(venue_map_lookup)
    m["toss_bat_first"]  = (m["toss_decision"] == "bat").astype(int)
    m["toss_winner_won"] = (m["toss_winner"] == m["winner"]).astype(int)
    m = m.dropna(subset=["winner"])
    d = d[d["match_id"].isin(m["id"])]

    conn = sqlite3.connect("ipl.db")
    m.to_sql("matches", conn, if_exists="replace", index=False)
    d.to_sql("deliveries", conn, if_exists="replace", index=False)

    d2 = d[d["inning"] == 2].copy()
    d2 = d2.merge(m[["id", "venue_clean", "season", "winner"]],
                  left_on="match_id", right_on="id", how="left")
    d2 = d2.sort_values(["match_id", "over", "ball"]).reset_index(drop=True)

    d2["runs_so_far"]  = d2.groupby("match_id")["total_runs"].cumsum()
    d2["wkts_fallen"]  = d2.groupby("match_id")["is_wicket"].transform(lambda x: x.cumsum())
    d2["balls_done"]   = d2.groupby("match_id").cumcount() + 1
    d2["overs_done"]   = (d2["balls_done"] / 6).round(2)
    d2["overs_left"]   = (20 - d2["overs_done"]).clip(lower=0.1)
    d2["wkts_left"]    = 10 - d2["wkts_fallen"]

    target_map = d[d["inning"] == 1].groupby("match_id")["total_runs"].sum() + 1
    d2["target"]      = d2["match_id"].map(target_map)
    d2["runs_needed"] = (d2["target"] - d2["runs_so_far"]).clip(lower=0)
    d2["rrr"] = (d2["runs_needed"] / d2["overs_left"]).round(2)
    d2["crr"] = (d2["runs_so_far"] / d2["overs_done"].clip(lower=0.1)).round(2)

    batting_team = d2.groupby("match_id")["batting_team"].first()
    d2["batting_team_name"] = d2["match_id"].map(batting_team)
    d2["won"] = (d2["winner"] == d2["batting_team_name"]).astype(int)

    features = d2[[
        "match_id", "overs_done", "overs_left", "wkts_left",
        "runs_needed", "rrr", "crr", "venue_clean", "won"
    ]].dropna()

    features.to_sql("win_features", conn, if_exists="replace", index=False)
    conn.close()

def ensure_database():
    needs_build = not os.path.exists("ipl.db")
    if not needs_build:
        try:
            conn = sqlite3.connect("ipl.db")
            tables = pd.read_sql(
                "SELECT name FROM sqlite_master WHERE type='table'", conn
            )["name"].tolist()
            conn.close()
            required = {"matches", "deliveries", "win_features"}
            if not required.issubset(set(tables)):
                needs_build = True
        except Exception:
            needs_build = True

    if needs_build:
        with st.spinner("Setting up the database for the first time, this takes a minute..."):
            build_database()

ensure_database()

# ── Load data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect("ipl.db")
    m  = pd.read_sql("SELECT * FROM matches",      conn)
    d  = pd.read_sql("SELECT * FROM deliveries",   conn)
    wf = pd.read_sql("SELECT * FROM win_features", conn)
    conn.close()
    return m, d, wf

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

m, d, wf = load_data()
mdl      = load_model()
model    = mdl["model"]
le       = mdl["label_encoder"]

total_matches    = len(m)
total_deliveries = len(d)
seasons          = m["season"].nunique()

st.markdown(
    '<div class="hero-banner">'
    '<div class="hero-title">IPL Win Predictor and Strategy Analyser</div>'
    '<div class="hero-sub">Data-driven cricket intelligence across 17 IPL seasons</div>'
    '<div style="margin-top:6px">'
    '<span class="badge">' + str(total_matches) + ' matches</span>'
    '<span class="badge">' + str(total_deliveries) + ' deliveries</span>'
    '<span class="badge">' + str(seasons) + ' seasons</span>'
    '<span class="badge">Logistic Regression</span>'
    '</div></div>',
    unsafe_allow_html=True
)

# ── Surprise finding callout ─────────────────────────────────
@st.cache_data
def compute_surprise_finding(m):
    vs = m.groupby("venue_clean").agg(
        matches=("id", "count"),
        bat_first_wins=("toss_bat_first", "sum"),
    ).reset_index()
    vs = vs[vs["matches"] >= 10]
    vs["bat_first_win_pct"] = (vs["bat_first_wins"] / vs["matches"] * 100).round(1)
    vs["distance_from_50"] = (vs["bat_first_win_pct"] - 50).abs()
    top = vs.sort_values("distance_from_50", ascending=False).iloc[0]

    venue_name = top["venue_clean"]
    pct        = top["bat_first_win_pct"]
    n_matches  = int(top["matches"])

    if pct < 50:
        text = (
            "At <strong>" + venue_name + "</strong>, teams that win the toss and choose to "
            "<strong>bat first</strong> only win <strong>" + str(pct) + "%</strong> of matches "
            "across " + str(n_matches) + " games — far below the 50% you'd expect by chance. "
            "Conventional cricket wisdom doesn't hold here."
        )
    else:
        text = (
            "At <strong>" + venue_name + "</strong>, teams that <strong>bat first</strong> win "
            "<strong>" + str(pct) + "%</strong> of matches across " + str(n_matches) + " games — "
            "a much stronger home advantage for first-innings batting than most venues show."
        )
    return text

surprise_text = compute_surprise_finding(m)
st.markdown(
    '<div class="surprise-box">'
    '<div class="surprise-icon">💡</div>'
    '<div><div class="surprise-label">Surprise finding from the data</div>'
    '<div class="surprise-text">' + surprise_text + '</div></div>'
    '</div>',
    unsafe_allow_html=True
)


# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Match Predictor",
    "Venue Intelligence",
    "Player Form",
    "Captain's Corner",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — MATCH PREDICTOR
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Enter current match situation</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        overs = st.slider("Overs completed", 0, 19, 10)
    with c2:
        wickets = st.slider("Wickets fallen", 0, 9, 3)
    with c3:
        runs_needed = st.number_input("Runs still needed", min_value=1, max_value=300, value=60)

    venues    = sorted(le.classes_.tolist())
    venue     = st.selectbox("Select venue", venues)

    overs_left  = max(20 - overs, 0.1)
    overs_done  = max(overs, 0.1)
    runs_scored = max(300 - runs_needed, 0)
    crr         = round(runs_scored / overs_done, 2)
    rrr         = round(runs_needed / overs_left, 2)
    wkts_left   = 10 - wickets

    try:
        venue_enc = int(le.transform([venue])[0])
    except Exception:
        venue_enc = 0

    X       = [[overs_done, overs_left, wkts_left, runs_needed, rrr, crr, venue_enc]]
    prob    = float(model.predict_proba(X)[0][1])
    prob_pct = round(prob * 100, 1)

    st.divider()
    st.markdown('<div class="section-label">Live win probability</div>', unsafe_allow_html=True)

    bar_color = GREEN if prob >= 0.5 else RED
    verdict   = "Batting team is WINNING" if prob >= 0.5 else "Batting team is LOSING"

    st.markdown(
        '<div class="prob-box">'
        '<div class="prob-number" style="color:' + bar_color + '">' + str(prob_pct) + '%</div>'
        '<div class="prob-verdict" style="color:' + bar_color + '">' + verdict + '</div>'
        '<div class="win-bar-bg"><div class="win-bar-fill" style="width:' + str(prob_pct) + '%;background:' + bar_color + '"></div></div>'
        '<div class="bar-labels"><span>0%  certain loss</span><span>50%</span><span>100%  certain win</span></div>'
        '</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Win probability",   str(prob_pct) + "%")
    m2.metric("Required run rate", str(rrr))
    m3.metric("Current run rate",  str(crr))
    m4.metric("Wickets remaining", str(wkts_left))

    if rrr < 8:
        rrr_txt = "The required rate of " + str(rrr) + " is very manageable."
    elif rrr < 12:
        rrr_txt = "The required rate of " + str(rrr) + " is challenging but possible."
    else:
        rrr_txt = "The required rate of " + str(rrr) + " is extremely difficult."

    st.markdown(
        '<div class="insight-box">At <strong>' + str(overs) + ' overs</strong>, needing '
        '<strong>' + str(runs_needed) + ' runs</strong> with <strong>' + str(wkts_left) +
        ' wickets</strong> left at <strong>' + venue + '</strong> — the batting team has a '
        '<strong>' + str(prob_pct) + '%</strong> chance of winning. ' + rrr_txt + '</div>',
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown('<div class="section-label">What-If Simulator — change one thing, see the impact</div>', unsafe_allow_html=True)
    st.write("Keep the same match situation but swap the venue. Does the ground actually change the odds?")

    sim_venue = st.selectbox("Compare against this venue instead", venues, key="sim_venue")

    try:
        sim_venue_enc = int(le.transform([sim_venue])[0])
    except Exception:
        sim_venue_enc = 0

    X_sim    = [[overs_done, overs_left, wkts_left, runs_needed, rrr, crr, sim_venue_enc]]
    sim_prob = float(model.predict_proba(X_sim)[0][1])
    sim_pct  = round(sim_prob * 100, 1)
    delta    = round(sim_pct - prob_pct, 1)

    sc1, sc2, sc3 = st.columns([1, 0.3, 1])
    with sc1:
        st.markdown(
            '<div class="compare-card"><div class="compare-name">' + venue + '</div>'
            '<div class="prob-number" style="font-size:36px;color:' + (GREEN if prob_pct >= 50 else RED) + '">'
            + str(prob_pct) + '%</div></div>',
            unsafe_allow_html=True
        )
    with sc2:
        st.markdown('<div class="sim-arrow">&#8594;</div>', unsafe_allow_html=True)
    with sc3:
        st.markdown(
            '<div class="compare-card"><div class="compare-name">' + sim_venue + '</div>'
            '<div class="prob-number" style="font-size:36px;color:' + (GREEN if sim_pct >= 50 else RED) + '">'
            + str(sim_pct) + '%</div></div>',
            unsafe_allow_html=True
        )

    if abs(delta) < 2:
        delta_txt = "Venue makes almost no difference here — the match situation itself is the dominant factor."
    elif delta > 0:
        delta_txt = "Win probability would be <strong>" + str(abs(delta)) + " points higher</strong> at " + sim_venue + " for the exact same match situation."
    else:
        delta_txt = "Win probability would be <strong>" + str(abs(delta)) + " points lower</strong> at " + sim_venue + " for the exact same match situation."

    st.markdown(
        '<div class="insight-box">' + delta_txt + '</div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════
# TAB 2 — VENUE INTELLIGENCE
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">How each ground behaves</div>', unsafe_allow_html=True)

    vstats = m.groupby("venue_clean").agg(
        matches        = ("id",              "count"),
        bat_first_wins = ("toss_bat_first",  "sum"),
        toss_wins      = ("toss_winner_won", "sum"),
    ).reset_index()
    vstats["bat_first_win_pct"] = (vstats["bat_first_wins"] / vstats["matches"] * 100).round(1)
    vstats["toss_win_pct"]      = (vstats["toss_wins"]      / vstats["matches"] * 100).round(1)
    vstats = vstats[vstats["matches"] >= 8].sort_values("bat_first_win_pct", ascending=True)

    fig1 = px.bar(
        vstats,
        x="bat_first_win_pct", y="venue_clean", orientation="h",
        color="bat_first_win_pct",
        color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
        range_color=[35, 65],
        text="bat_first_win_pct",
        title="Bat-first win % by venue",
        labels={"bat_first_win_pct": "Bat First Win %", "venue_clean": "Venue"},
    )
    fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig1.add_vline(x=50, line_dash="dash", line_color="#8b90b8",
                   annotation_text="50% line", annotation_position="top")
    fig1.update_layout(
        template=PTHEME,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        height=max(420, len(vstats) * 32),
        margin=dict(l=0, r=70, t=50, b=20),
        yaxis_title="",
        font=dict(family="Inter", color=TEXT),
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    st.markdown('<div class="section-label">Explore a specific venue</div>', unsafe_allow_html=True)
    sel  = st.selectbox("Choose venue", sorted(m["venue_clean"].unique()), key="v2")
    vrow = vstats[vstats["venue_clean"] == sel]
    if not vrow.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total matches",     int(vrow["matches"].values[0]))
        c2.metric("Bat first win %",   str(vrow["bat_first_win_pct"].values[0]) + "%")
        c3.metric("Toss winner win %", str(vrow["toss_win_pct"].values[0]) + "%")
        bp = float(vrow["bat_first_win_pct"].values[0])
        tip = "bat first" if bp >= 50 else "field first"
        st.markdown(
            '<div class="insight-box">At <strong>' + sel + '</strong>, teams that choose to '
            '<strong>' + tip + '</strong> have historically performed better. '
            'Bat-first teams win <strong>' + str(bp) + '%</strong> vs '
            '<strong>' + str(round(100 - bp, 1)) + '%</strong> for field-first teams.</div>',
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════
# TAB 3 — PLAYER FORM
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Rolling 5-match average tracker</div>', unsafe_allow_html=True)

    all_batters = sorted(d["batter"].dropna().unique().tolist())

    def get_player_runs(player_name):
        pdf = d[d["batter"] == player_name].merge(
            m[["id", "date", "season"]], left_on="match_id", right_on="id"
        )
        rpm = pdf.groupby(["match_id", "date"])["batsman_runs"].sum().reset_index().sort_values("date")
        rpm["rolling_avg"] = rpm["batsman_runs"].rolling(5, min_periods=1).mean().round(1)
        rpm["date"] = pd.to_datetime(rpm["date"])
        return rpm

    mode = st.radio("View mode", ["Single player", "Compare two players"], horizontal=True)

    if mode == "Single player":
        player  = st.selectbox("Select batter", all_batters)
        runs_pm = get_player_runs(player)
        career_avg = round(float(runs_pm["batsman_runs"].mean()), 1)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=runs_pm["date"], y=runs_pm["batsman_runs"],
            name="Runs per match", marker_color=ACCENT, opacity=0.4,
        ))
        fig2.add_trace(go.Scatter(
            x=runs_pm["date"], y=runs_pm["rolling_avg"],
            name="5-match rolling avg",
            line=dict(color=ACCENT2, width=2.5),
            mode="lines+markers", marker=dict(size=5),
        ))
        fig2.add_hline(y=career_avg, line_dash="dot", line_color="#8b90b8",
                       annotation_text="Career avg " + str(career_avg),
                       annotation_position="bottom right")
        fig2.update_layout(
            title=player + "  —  match runs and rolling form",
            template=PTHEME,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=0, r=0, t=50, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            font=dict(family="Inter", color=TEXT),
            xaxis_title="", yaxis_title="Runs",
        )
        st.plotly_chart(fig2, use_container_width=True)

        best     = int(runs_pm["batsman_runs"].max())
        innings  = len(runs_pm)
        fifties  = int((runs_pm["batsman_runs"] >= 50).sum())
        hundreds = int((runs_pm["batsman_runs"] >= 100).sum())
        recent   = round(float(runs_pm.tail(5)["batsman_runs"].mean()), 1)
        form_txt = "In form — last 5 avg above career average." if recent > career_avg else "Below average form — last 5 avg below career average."

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Career avg",    str(career_avg))
        c2.metric("Best score",    str(best))
        c3.metric("50s / 100s",    str(fifties) + " / " + str(hundreds))
        c4.metric("Total innings", str(innings))

        st.markdown(
            '<div class="insight-box"><strong>' + player + '</strong> last 5 innings avg: '
            '<strong>' + str(recent) + '</strong> vs career avg of '
            '<strong>' + str(career_avg) + '</strong>. ' + form_txt + '</div>',
            unsafe_allow_html=True
        )

    else:
        cc1, cc2 = st.columns(2)
        with cc1:
            player_a = st.selectbox("Player A", all_batters, index=0, key="player_a")
        with cc2:
            default_idx = 1 if len(all_batters) > 1 else 0
            player_b = st.selectbox("Player B", all_batters, index=default_idx, key="player_b")

        runs_a = get_player_runs(player_a)
        runs_b = get_player_runs(player_b)
        avg_a  = round(float(runs_a["batsman_runs"].mean()), 1)
        avg_b  = round(float(runs_b["batsman_runs"].mean()), 1)

        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Scatter(
            x=runs_a["date"], y=runs_a["rolling_avg"],
            name=player_a + " (rolling avg)",
            line=dict(color=ACCENT, width=2.5),
            mode="lines",
        ))
        fig_cmp.add_trace(go.Scatter(
            x=runs_b["date"], y=runs_b["rolling_avg"],
            name=player_b + " (rolling avg)",
            line=dict(color=ACCENT2, width=2.5),
            mode="lines",
        ))
        fig_cmp.update_layout(
            title=player_a + "  vs  " + player_b + "  —  5-match rolling form",
            template=PTHEME,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=0, r=0, t=50, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            font=dict(family="Inter", color=TEXT),
            xaxis_title="", yaxis_title="Rolling avg runs",
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                '<div class="compare-card"><div class="compare-name" style="color:' + ACCENT + '">' + player_a + '</div>'
                '<div style="font-size:13px;color:#8b90b8">Career avg</div>'
                '<div class="prob-number" style="font-size:30px">' + str(avg_a) + '</div>'
                '<div style="font-size:13px;color:#8b90b8;margin-top:8px">Innings: ' + str(len(runs_a))
                + ' &nbsp; · &nbsp; Best: ' + str(int(runs_a["batsman_runs"].max())) + '</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col_b:
            st.markdown(
                '<div class="compare-card"><div class="compare-name" style="color:' + ACCENT2 + '">' + player_b + '</div>'
                '<div style="font-size:13px;color:#8b90b8">Career avg</div>'
                '<div class="prob-number" style="font-size:30px">' + str(avg_b) + '</div>'
                '<div style="font-size:13px;color:#8b90b8;margin-top:8px">Innings: ' + str(len(runs_b))
                + ' &nbsp; · &nbsp; Best: ' + str(int(runs_b["batsman_runs"].max())) + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        better    = player_a if avg_a >= avg_b else player_b
        diff      = round(abs(avg_a - avg_b), 1)
        st.markdown(
            '<div class="insight-box"><strong>' + better + '</strong> has the higher career average, '
            'by <strong>' + str(diff) + ' runs</strong> per innings, across the full dataset.</div>',
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════
# TAB 4 — CAPTAIN'S CORNER
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-label">Toss decision intelligence</div>', unsafe_allow_html=True)
    st.write("Should you bat or field after winning the toss? 17 seasons of data decides.")

    sel_venue = st.selectbox("Choose venue", sorted(m["venue_clean"].unique()), key="cap")
    vdata     = m[m["venue_clean"] == sel_venue]
    bat_d     = vdata[vdata["toss_decision"] == "bat"]
    field_d   = vdata[vdata["toss_decision"] == "field"]

    bat_pct   = round(float(bat_d["toss_winner_won"].mean())   * 100, 1) if len(bat_d)   > 0 else 0.0
    field_pct = round(float(field_d["toss_winner_won"].mean()) * 100, 1) if len(field_d) > 0 else 0.0
    rec       = "Bat First" if bat_pct >= field_pct else "Field First"
    rec_color = GREEN if bat_pct >= field_pct else ACCENT

    st.markdown(
        '<div class="rec-box">'
        '<div class="rec-label">Recommendation at ' + sel_venue + '</div>'
        '<div class="rec-value" style="color:' + rec_color + '">' + rec + '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Bat-first win rate",   str(bat_pct) + "%")
    c2.metric("Field-first win rate", str(field_pct) + "%")
    c3.metric("Total matches",        str(len(vdata)))

    monthly = vdata.groupby("month")["toss_winner_won"].mean().reset_index()
    monthly["win_pct"] = (monthly["toss_winner_won"] * 100).round(1)
    month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                 7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    monthly["month_name"] = monthly["month"].map(month_map)

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=monthly["month_name"], y=monthly["win_pct"],
        mode="lines+markers",
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=8, color=ACCENT),
        fill="tozeroy",
        fillcolor=FILL_BLUE,
        name="Toss winner win %",
    ))
    fig4.add_hline(y=50, line_dash="dash", line_color="#8b90b8",
                   annotation_text="50% baseline", annotation_position="bottom right")
    fig4.update_layout(
        title="Toss winner win % by month at " + sel_venue,
        template=PTHEME,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=0, r=0, t=50, b=20),
        font=dict(family="Inter", color=TEXT),
        xaxis_title="Month", yaxis_title="Win %",
        yaxis_range=[0, 100],
    )
    st.plotly_chart(fig4, use_container_width=True)

    dew_note = (
        "The dew effect in evening matches likely explains why fielding first is better here."
        if field_pct > bat_pct else
        "Pitches here tend to favour early batting conditions."
    )
    st.markdown(
        '<div class="insight-box">At <strong>' + sel_venue + '</strong>: bat-first teams win '
        '<strong>' + str(bat_pct) + '%</strong>, field-first teams win '
        '<strong>' + str(field_pct) + '%</strong> across '
        '<strong>' + str(len(vdata)) + '</strong> matches. ' + dew_note + '</div>',
        unsafe_allow_html=True
    )