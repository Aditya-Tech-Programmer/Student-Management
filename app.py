
import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================
# STUDENT NEXUS — 3D STUDENT MANAGEMENT DASHBOARD
# Run: streamlit run app.py
# Data is saved locally in students.json
# ============================================================

st.set_page_config(
    page_title="Student Nexus | Management Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).with_name("students.json")

DEFAULT_STUDENTS = {
    "101": {"name": "Avinash", "age": 18, "marks": 100, "skills": ["Python", "Communication"]},
    "102": {"name": "Rahul", "age": 19, "marks": 75, "skills": ["C", "Problem Solving"]},
    "103": {"name": "Arun", "age": 17, "marks": 65, "skills": ["HTML", "Teamwork"]},
    "104": {"name": "Baban", "age": 14, "marks": 99, "skills": ["Python", "Design"]},
    "105": {"name": "Pooja", "age": 17, "marks": 89, "skills": ["Java", "Leadership"]},
}


def load_students():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                # Supports both the original student dictionary and the newer
                # structured backup containing students + attendance.
                if "students" in data and isinstance(data.get("students"), dict):
                    st.session_state.attendance = data.get("attendance", {})
                    st.session_state.subject_marks = data.get("subject_marks", {})
                    return data["students"]
                return data
        except (json.JSONDecodeError, OSError):
            st.warning("The saved data file could not be read. Starting with demo records.")
    return {key: value.copy() for key, value in DEFAULT_STUDENTS.items()}


def save_students():
    payload = {
        "students": st.session_state.students,
        "attendance": st.session_state.get("attendance", {}),
        "subject_marks": st.session_state.get("subject_marks", {}),
    }
    DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if "students" not in st.session_state:
    st.session_state.students = load_students()

students = st.session_state.students
if "attendance" not in st.session_state:
    st.session_state.attendance = {}


def cgpa(marks):
    return round(float(marks) / 10, 2)


def student_rows():
    rows = []
    for sid, record in students.items():
        rows.append({
            "Student ID": sid,
            "Name": record.get("name", ""),
            "Age": record.get("age", ""),
            "Marks": record.get("marks", 0),
            "CGPA": cgpa(record.get("marks", 0)),
            "Skills": ", ".join(record.get("skills", [])),
        })
    return rows


def metric_card(label, value, note, icon):
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-top"><span>{icon}</span><span class="metric-label">{label}</span></div>
          <div class="metric-value">{value}</div>
          <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root {
  --ink:#f4f1e8; --muted:#b8b1a2; --panel:rgba(29,31,33,.92);
  --line:rgba(218,185,115,.24); --gold:#d6b36a; --gold-light:#f5df9b;
  --bg:#111315; --green:#6e9b83;
}
* { box-sizing:border-box; }
.stApp {
  background:
    radial-gradient(ellipse at 8% 0%, rgba(214,179,106,.14), transparent 34%),
    radial-gradient(ellipse at 94% 16%, rgba(91,133,111,.15), transparent 31%),
    radial-gradient(ellipse at 50% 100%, rgba(155,125,67,.09), transparent 36%),
    linear-gradient(135deg,#101214 0%,#191b1d 50%,#111315 100%);
  background-size:140% 140%; animation:ambientShift 22s ease-in-out infinite alternate;
  color:var(--ink); font-family:'DM Sans',sans-serif; overflow-x:hidden;
}
@keyframes ambientShift { 0%{background-position:0% 0%} 100%{background-position:100% 100%} }
.stApp::before {
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:radial-gradient(circle at 12% 28%,rgba(245,223,155,.18) 0 1px,transparent 2px),radial-gradient(circle at 76% 72%,rgba(110,155,131,.18) 0 1px,transparent 2px),radial-gradient(circle at 52% 12%,rgba(255,255,255,.09) 0 1px,transparent 2px);
  background-size:170px 170px,230px 230px,130px 130px; animation:particleDrift 34s linear infinite;
}
@keyframes particleDrift { from{transform:translate3d(0,0,0)} to{transform:translate3d(-70px,40px,0)} }
.block-container { position:relative; z-index:1; max-width:1500px; padding-top:1.7rem; padding-bottom:3rem; }
[data-testid="stHeader"] {background:rgba(16,18,20,.72);}
[data-testid="stSidebar"] {background:linear-gradient(180deg,rgba(31,33,34,.99),rgba(17,19,21,.99));border-right:1px solid var(--line);}
[data-testid="stSidebar"] * { color:#eee8da; }
h1,h2,h3 {font-family:'Space Grotesk',sans-serif!important;color:#f6f0e2!important;letter-spacing:.15px;}
p,label,.stMarkdown,[data-testid="stCaptionContainer"] {color:#ded8ca;}
.hero {
  position:relative; overflow:hidden; padding:30px 32px 29px; margin-bottom:22px;
  border:1px solid rgba(214,179,106,.38); border-radius:25px;
  background:linear-gradient(125deg,rgba(49,47,40,.96),rgba(29,33,31,.95) 58%,rgba(26,37,31,.94));
  box-shadow:0 25px 48px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.10),inset 0 -2px 0 rgba(0,0,0,.25);
  transform:perspective(1100px) rotateX(1.2deg); isolation:isolate;
}
.hero::before {content:"";position:absolute;inset:-1px;z-index:-1;background:linear-gradient(115deg,transparent 10%,rgba(245,223,155,.12) 38%,transparent 60%);transform:translateX(-65%);animation:heroShine 9s ease-in-out infinite;}
.hero::after {content:"";position:absolute;width:240px;height:240px;right:-70px;top:-115px;border-radius:50%;border:1px solid rgba(245,223,155,.15);box-shadow:0 0 0 20px rgba(245,223,155,.025),0 0 0 45px rgba(245,223,155,.018);}
@keyframes heroShine {0%,35%{transform:translateX(-80%)}70%,100%{transform:translateX(90%)}}
.hero-kicker {color:#e0c681;letter-spacing:2.5px;font-size:11px;font-weight:800;text-transform:uppercase;}
.hero-title {
  position:relative; width:fit-content; max-width:100%;
  font-family:'Space Grotesk',sans-serif;font-size:clamp(32px,4.2vw,48px);font-weight:700;line-height:1.16;margin:11px 0 12px;
  color:#f8e8b5; letter-spacing:-1.2px;
  text-shadow:1px 1px 0 #b99a56,2px 2px 0 #927744,3px 3px 0 #665532,4px 4px 0 #3d3424,7px 9px 14px rgba(0,0,0,.62),0 0 24px rgba(214,179,106,.18);
  transform:perspective(500px) rotateX(3deg);
}
.hero-sub {color:#c9c3b5;font-size:14px;max-width:760px;line-height:1.65;}
.metric-card {
  position:relative;min-height:143px;padding:19px 20px;border-radius:19px;overflow:hidden;
  border:1px solid rgba(214,179,106,.29);
  background:linear-gradient(145deg,rgba(53,52,46,.98),rgba(29,31,31,.98) 62%,rgba(24,30,27,.98));
  box-shadow:0 12px 0 #101211,0 17px 27px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.11),inset 0 -2px 0 rgba(0,0,0,.35);
  transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;
}
.metric-card::before {content:"";position:absolute;top:0;left:10%;width:80%;height:1px;background:linear-gradient(90deg,transparent,rgba(245,223,155,.65),transparent);}
.metric-card:hover {transform:translateY(-6px) perspective(800px) rotateX(3deg) rotateY(-1deg);border-color:rgba(245,223,155,.65);box-shadow:0 17px 0 #101211,0 25px 34px rgba(0,0,0,.43),0 0 24px rgba(214,179,106,.10),inset 0 1px 0 rgba(255,255,255,.13);}
.metric-top {display:flex;justify-content:space-between;align-items:center;font-size:22px;}
.metric-label {font-size:11px;color:#c6bda8;text-transform:uppercase;letter-spacing:1.25px;font-weight:700;}
.metric-value {font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:700;color:#f5df9b;margin-top:9px;text-shadow:0 3px 0 rgba(0,0,0,.3),0 0 16px rgba(214,179,106,.14);}
.metric-note {font-size:12px;color:#aaa697;margin-top:2px;}
.panel {padding:19px 21px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(145deg,rgba(43,44,40,.88),rgba(24,27,26,.94));box-shadow:0 13px 26px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.045);}
/* 3D buttons */
div.stButton>button,div.stFormSubmitButton>button,div.stDownloadButton>button {
  border:1px solid rgba(245,223,155,.42);border-radius:11px;
  background:linear-gradient(135deg,#d0ad62,#a98643 60%,#8d7139);color:#171713!important;font-weight:800;
  box-shadow:0 5px 0 #66512b,0 9px 18px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.3);transition:all .18s ease;
}
div.stButton>button:hover,div.stFormSubmitButton>button:hover,div.stDownloadButton>button:hover {transform:translateY(-3px);border-color:#f5df9b;background:linear-gradient(135deg,#f0d58e,#c5a052);box-shadow:0 8px 0 #66512b,0 14px 24px rgba(0,0,0,.32);color:#171713!important;}
div.stButton>button:active,div.stFormSubmitButton>button:active,div.stDownloadButton>button:active {transform:translateY(2px);box-shadow:0 2px 0 #66512b,0 4px 9px rgba(0,0,0,.24);}
.stTextInput input,.stNumberInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"],.stDateInput input {
  background-color:#202321!important;color:#f5f0e4!important;border:1px solid rgba(214,179,106,.28)!important;border-radius:10px!important;
}
.stTextInput input:focus,.stNumberInput input:focus,.stTextArea textarea:focus {border-color:#d6b36a!important;box-shadow:0 0 0 2px rgba(214,179,106,.14)!important;}
[data-testid="stDataFrame"],[data-testid="stTable"] {border:1px solid var(--line);border-radius:13px;overflow:hidden;box-shadow:0 10px 22px rgba(0,0,0,.16);}
[data-testid="stMetric"] {background:linear-gradient(145deg,rgba(46,47,42,.9),rgba(27,29,28,.92));border:1px solid var(--line);border-radius:14px;padding:12px;box-shadow:0 7px 0 rgba(0,0,0,.18),0 12px 20px rgba(0,0,0,.15);}
[data-testid="stMetricValue"] {color:#f5df9b!important;}
.stTabs [data-baseweb="tab-list"] {gap:8px;}
.stTabs [data-baseweb="tab"] {background:rgba(214,179,106,.07);border:1px solid rgba(214,179,106,.14);border-radius:9px 9px 0 0;padding:9px 15px;}
.stTabs [aria-selected="true"] {background:rgba(214,179,106,.16)!important;border-bottom:2px solid #d6b36a!important;}
details {background:rgba(35,37,34,.85);border:1px solid var(--line);border-radius:12px;padding:5px;}
hr {border-color:var(--line)!important;}
.small-muted {color:#aaa697;font-size:12px;}
footer {visibility:hidden;}
::-webkit-scrollbar {width:9px;} ::-webkit-scrollbar-track {background:#111315;} ::-webkit-scrollbar-thumb {background:linear-gradient(#d6b36a,#6e9b83);border-radius:10px;}
/* ADVANCED 3D LAYER — depth, glass, holographic edges and floating elements */
.stApp { perspective: 1200px; }
.block-container > div { transform-style: preserve-3d; }
.hero {
  min-height: 220px;
  box-shadow: 0 28px 0 -17px rgba(0,0,0,.42), 0 38px 55px rgba(0,0,0,.42),
              inset 0 1px 0 rgba(255,255,255,.13), inset 0 -3px 0 rgba(0,0,0,.32);
}
.hero-title {
  filter: drop-shadow(0 8px 7px rgba(0,0,0,.24));
  animation: titleFloat 5s ease-in-out infinite;
  transform-origin: left center;
}
@keyframes titleFloat {
  0%,100% { transform: perspective(650px) rotateX(4deg) translateY(0); }
  50% { transform: perspective(650px) rotateX(0deg) translateY(-3px); }
}
/* A dimensional orb is placed inside the hero banner */
.hero-orb {
  position:absolute; width:148px; height:148px; right:7%; top:34px;
  border-radius:50%; z-index:-0; pointer-events:none;
  background: radial-gradient(circle at 31% 24%, #fff1c4 0 2%, #e8c875 8%, #a47c36 29%, #4b3b20 53%, #171a18 72%);
  border:1px solid rgba(255,235,178,.62);
  box-shadow: inset -17px -18px 30px rgba(0,0,0,.66), inset 8px 8px 19px rgba(255,255,255,.26),
              0 0 30px rgba(214,179,106,.2), 0 24px 26px rgba(0,0,0,.35);
  transform: perspective(500px) rotateY(-22deg) rotateX(13deg);
  animation: orbFloat 7s ease-in-out infinite;
}
.hero-orb::before,.hero-orb::after {
  content:""; position:absolute; inset:20px -19px; border:1px solid rgba(245,223,155,.48);
  border-radius:50%; transform:rotate(-28deg) rotateX(62deg);
  box-shadow:0 0 13px rgba(214,179,106,.12);
}
.hero-orb::after { inset:34px -27px; transform:rotate(48deg) rotateX(62deg); border-color:rgba(110,155,131,.62); }
@keyframes orbFloat { 0%,100%{transform:perspective(500px) translateY(0) rotateY(-22deg) rotateX(13deg)} 50%{transform:perspective(500px) translateY(-9px) rotateY(16deg) rotateX(7deg)} }
/* Elevation and subtle tilt for dashboard surfaces */
.metric-card { transform:perspective(900px) rotateX(1.2deg); transform-style:preserve-3d; }
.metric-card::after {
  content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background:linear-gradient(135deg,rgba(255,255,255,.065),transparent 33%,transparent 70%,rgba(214,179,106,.045));
}
.panel {
  position:relative; overflow:hidden;
  box-shadow:0 5px 0 rgba(7,8,8,.45), 0 19px 32px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.075);
  transform:perspective(1200px) rotateX(.5deg);
  transition:transform .28s ease, border-color .28s ease, box-shadow .28s ease;
}
.panel:hover { transform:perspective(1200px) translateY(-3px) rotateX(0deg); border-color:rgba(245,223,155,.42); box-shadow:0 7px 0 rgba(7,8,8,.42),0 24px 38px rgba(0,0,0,.3),0 0 20px rgba(214,179,106,.07); }
/* Glassy containers across Streamlit widgets */
div[data-testid="stForm"], div[data-testid="stExpander"], div[data-testid="stFileUploader"] section,
div[data-testid="stDataFrame"], div[data-testid="stTable"] {
  backdrop-filter:blur(12px);
}
/* A tiny gold edge highlight on all cards */
.metric-card, .panel, div[data-testid="stMetric"] { isolation:isolate; }
/* 3D sidebar navigation */
section[data-testid="stSidebar"] [role="radiogroup"] label {
  border:1px solid transparent; border-radius:11px; transition:all .2s ease;
}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
  transform:translateX(4px); border-color:rgba(214,179,106,.32); background:linear-gradient(100deg,rgba(214,179,106,.16),rgba(110,155,131,.06));
}
/* Inputs feel inset into the interface */
.stTextInput input,.stNumberInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"],.stDateInput input {
  box-shadow:inset 0 3px 8px rgba(0,0,0,.22),0 1px 0 rgba(255,255,255,.035);
}
/* Tabs as raised metal plates */
.stTabs [data-baseweb="tab"] { box-shadow:0 3px 0 rgba(0,0,0,.2); transition:transform .2s ease,background .2s ease; }
.stTabs [data-baseweb="tab"]:hover { transform:translateY(-2px); }
/* Progress indicators */
div[data-testid="stProgressBar"] > div { background:rgba(214,179,106,.14); border-radius:999px; }
div[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#6e9b83,#d6b36a,#f5df9b); box-shadow:0 0 12px rgba(214,179,106,.24); }
/* Gold selection glow */
::selection { background:rgba(214,179,106,.36); color:#fff9e8; }
@media(max-width:768px) {.block-container{padding-left:1rem;padding-right:1rem}.hero{padding:23px 20px}.hero-title{font-size:32px}.metric-card{margin-bottom:7px}.hero-orb{width:82px;height:82px;right:5%;top:16px;opacity:.55}.hero-sub{max-width:95%}}
@media(prefers-reduced-motion:reduce) {*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}

/* ============================================================
   PREMIUM 3D UI UPGRADE — glass surfaces, metallic edges,
   holographic highlights, depth layers and responsive motion
   ============================================================ */
:root {
  --gold-hot:#ffe7a1;
  --gold-mid:#d6b36a;
  --sage:#8fbea2;
  --glass:rgba(34,38,35,.72);
}

/* A more dimensional background with soft spotlight pools */
.stApp {
  background-image:
    radial-gradient(ellipse at 15% 8%, rgba(214,179,106,.19), transparent 28%),
    radial-gradient(ellipse at 88% 28%, rgba(110,155,131,.18), transparent 29%),
    radial-gradient(ellipse at 62% 95%, rgba(214,179,106,.10), transparent 32%),
    linear-gradient(135deg,#0b0d0e 0%,#1c201e 48%,#111513 100%);
}

/* Hero becomes a layered glass-and-metal display panel */
.hero {
  border:1px solid rgba(255,231,161,.48);
  background:
    linear-gradient(115deg,rgba(55,53,43,.96),rgba(28,35,31,.94) 54%,rgba(20,31,26,.97));
  box-shadow:
    0 2px 0 rgba(255,255,255,.08),
    0 10px 0 -4px rgba(0,0,0,.32),
    0 32px 58px rgba(0,0,0,.48),
    inset 0 1px 0 rgba(255,255,255,.16),
    inset 0 -2px 0 rgba(0,0,0,.38);
}
.hero-title {
  background:linear-gradient(180deg,#fff2c6 0%,#f5df9b 32%,#d0a951 68%,#9a7938 100%);
  -webkit-background-clip:text;
  background-clip:text;
  -webkit-text-fill-color:transparent;
  text-shadow:3px 3px 0 rgba(107,82,36,.9),6px 6px 0 rgba(59,48,29,.86),
              9px 12px 17px rgba(0,0,0,.58),0 0 28px rgba(245,223,155,.20);
  letter-spacing:-1.35px;
}
.hero-orb {
  background:radial-gradient(circle at 28% 22%,#fff9df 0 2%,#f5df9b 7%,#d0a951 20%,#80612d 40%,#3b382b 61%,#141815 75%);
  box-shadow:inset -20px -21px 32px rgba(0,0,0,.72),inset 8px 8px 18px rgba(255,255,255,.38),
             0 0 38px rgba(214,179,106,.25),0 26px 30px rgba(0,0,0,.42);
}

/* Metric cards: raised metal blocks with a luminous top edge */
.metric-card {
  border:1px solid rgba(245,223,155,.34);
  background:linear-gradient(145deg,rgba(62,60,50,.98) 0%,rgba(35,39,35,.98) 48%,rgba(22,29,25,.99) 100%);
  box-shadow:0 7px 0 #111411,0 15px 0 -4px rgba(0,0,0,.36),0 26px 34px rgba(0,0,0,.34),
             inset 0 1px 0 rgba(255,255,255,.15),inset 0 -2px 0 rgba(0,0,0,.35);
  transform:perspective(1000px) rotateX(2deg) translateZ(0);
}
.metric-card:hover {
  transform:perspective(1000px) rotateX(0deg) rotateY(-2deg) translateY(-8px) scale(1.012);
  box-shadow:0 9px 0 #111411,0 17px 0 -4px rgba(0,0,0,.36),0 34px 42px rgba(0,0,0,.46),
             0 0 30px rgba(214,179,106,.15),inset 0 1px 0 rgba(255,255,255,.19);
}
.metric-value {color:var(--gold-hot);}

/* Glass panels across charts, reports and content sections */
.panel {
  border:1px solid rgba(214,179,106,.25);
  background:linear-gradient(145deg,rgba(49,52,46,.79),rgba(24,29,26,.93));
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  box-shadow:0 5px 0 rgba(5,7,6,.40),0 22px 34px rgba(0,0,0,.27),
             inset 0 1px 0 rgba(255,255,255,.08);
}

/* Streamlit's native metric boxes, containers and expanders */
[data-testid="stMetric"] {
  background:linear-gradient(145deg,rgba(54,57,49,.95),rgba(25,30,27,.96))!important;
  border:1px solid rgba(214,179,106,.30)!important;
  border-radius:16px!important;
  box-shadow:0 5px 0 rgba(0,0,0,.25),0 15px 24px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.09)!important;
  transition:transform .25s ease,box-shadow .25s ease!important;
}
[data-testid="stMetric"]:hover {transform:translateY(-4px);box-shadow:0 8px 0 rgba(0,0,0,.25),0 22px 32px rgba(0,0,0,.28)!important;}
[data-testid="stExpander"] {
  border:1px solid rgba(214,179,106,.25)!important;border-radius:14px!important;
  background:linear-gradient(145deg,rgba(38,42,37,.80),rgba(21,25,22,.88))!important;
  box-shadow:0 9px 18px rgba(0,0,0,.15)!important;
}

/* Sidebar navigation has a recessed, premium console feel */
[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#252923 0%,#171c19 52%,#101412 100%)!important;
  box-shadow:inset -1px 0 0 rgba(245,223,155,.10),8px 0 28px rgba(0,0,0,.12);
}
[data-testid="stSidebar"] [role="radiogroup"] label {
  border:1px solid transparent;border-radius:11px;padding:7px 9px;
  transition:all .2s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
  background:linear-gradient(135deg,rgba(214,179,106,.16),rgba(110,155,131,.10));
  border-color:rgba(214,179,106,.22);transform:translateX(3px);
}

/* Buttons with real visual depth: top highlight + lower extrusion */
div.stButton>button,div.stFormSubmitButton>button,div.stDownloadButton>button {
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,#f0d58e 0%,#c9a457 52%,#98783c 100%);
  border:1px solid rgba(255,239,189,.70);
  box-shadow:0 5px 0 #66512b,0 10px 18px rgba(0,0,0,.30),inset 0 1px 0 rgba(255,255,255,.45);
  letter-spacing:.1px;
}
div.stButton>button::after,div.stFormSubmitButton>button::after,div.stDownloadButton>button::after {
  content:"";position:absolute;top:0;left:-120%;width:65%;height:100%;
  background:linear-gradient(100deg,transparent,rgba(255,255,255,.32),transparent);
  transform:skewX(-20deg);transition:left .55s ease;pointer-events:none;
}
div.stButton>button:hover::after,div.stFormSubmitButton>button:hover::after,div.stDownloadButton>button:hover::after {left:150%;}

/* Input fields look inset into a control deck */
.stTextInput input,.stNumberInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"],.stDateInput input {
  border-color:rgba(214,179,106,.35)!important;
  box-shadow:inset 0 3px 9px rgba(0,0,0,.30),0 1px 0 rgba(255,255,255,.04)!important;
}

/* Charts and tables sit on a subtle glass platform */
[data-testid="stDataFrame"],[data-testid="stTable"],[data-testid="stVegaLiteChart"],[data-testid="stArrowVegaLiteChart"] {
  border:1px solid rgba(214,179,106,.22);border-radius:15px;overflow:hidden;
  box-shadow:0 12px 25px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.04);
}
.stTabs [data-baseweb="tab"] {transition:transform .2s ease,box-shadow .2s ease,background .2s ease;}
.stTabs [data-baseweb="tab"]:hover {transform:translateY(-3px);box-shadow:0 5px 0 rgba(0,0,0,.20);}

/* Fine metallic scrollbar and visible keyboard focus */
::-webkit-scrollbar-thumb {background:linear-gradient(180deg,#f5df9b,#b08c48 55%,#6e9b83);border:2px solid #111513;}
*:focus-visible {outline:2px solid #f5df9b!important;outline-offset:2px!important;}

@media(max-width:768px) {
  .hero {min-height:190px;padding:22px 18px;}
  .hero-title {font-size:31px;max-width:75%;}
  .hero-orb {width:76px;height:76px;right:4%;top:20px;opacity:.62;}
  .metric-card {min-height:125px;padding:16px;}
}

/* PREMIUM HERO TITLE — metallic gold, deep extrusion, animated shimmer */
.hero { overflow: hidden; isolation: isolate; }
.hero-kicker {
  display: inline-flex; align-items: center; gap: 9px;
  padding: 8px 13px; margin-bottom: 5px; border-radius: 999px;
  border: 1px solid rgba(245,223,155,.27);
  background: linear-gradient(110deg,rgba(245,223,155,.12),rgba(110,155,131,.08));
  box-shadow: inset 0 1px 0 rgba(255,255,255,.08), 0 7px 20px rgba(0,0,0,.15);
  letter-spacing: 2.7px; font-size: 10px;
}
.hero-kicker::before {
  content: ''; width: 7px; height: 7px; flex: 0 0 7px; border-radius: 50%;
  background: #f5df9b; box-shadow: 0 0 12px rgba(245,223,155,.85);
}
.hero-title {
  display: block; width: fit-content; max-width: 100%;
  margin: 15px 0 17px; padding: 0 12px 12px 0;
  font-size: clamp(38px,5.2vw,66px); font-weight: 800;
  letter-spacing: -2.4px; line-height: 1.08;
  color: #fff0bd;
  background: linear-gradient(180deg,#fff9df 0%,#f5df9b 28%,#d6b36a 55%,#a47c36 72%,#f5df9b 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 1px 0 #f9e7ad, 0 2px 0 #d5b66e, 0 3px 0 #a98745,
               0 4px 0 #79602f, 0 5px 0 #574522, 0 8px 0 #322819,
               0 13px 14px rgba(0,0,0,.52), 0 0 32px rgba(245,223,155,.18);
  filter: drop-shadow(0 0 18px rgba(214,179,106,.13));
  transform: perspective(900px) rotateX(7deg);
  transform-origin: left center;
  animation: titleReveal 900ms cubic-bezier(.2,.8,.2,1) both, titleFloat 6s ease-in-out 1s infinite;
}
.hero-title span {
  display: inline-block; margin-left: 4px;
  -webkit-text-fill-color: #f5df9b;
  color: #f5df9b !important;
  text-shadow: 1px 1px 0 #d6b36a, 3px 3px 0 #8c6b31, 6px 7px 0 #3c301d,
               0 0 24px rgba(245,223,155,.48);
  animation: arrowPulse 2.8s ease-in-out infinite;
}
.hero-sub {
  position: relative; max-width: 760px; padding-left: 15px;
  border-left: 2px solid rgba(245,223,155,.62);
  color: #e2ddcf; font-size: clamp(14px,1.3vw,17px); line-height: 1.8;
  text-shadow: 0 2px 8px rgba(0,0,0,.25);
}
.hero-orb { right: 8%; top: 28px; width: 172px; height: 172px; }
.hero::after {
  border-color: rgba(245,223,155,.22);
  box-shadow: 0 0 0 20px rgba(245,223,155,.035), 0 0 0 45px rgba(245,223,155,.025),
              0 0 0 72px rgba(110,155,131,.018);
}
@keyframes titleReveal {
  from { opacity: 0; transform: perspective(900px) rotateX(18deg) translateY(15px); filter: blur(5px); }
  to { opacity: 1; transform: perspective(900px) rotateX(7deg) translateY(0); filter: blur(0); }
}
@keyframes arrowPulse { 0%,100% { transform: translate3d(0,0,0); } 50% { transform: translate3d(4px,-4px,0); } }
@media (max-width: 768px) {
  .hero-title { font-size: clamp(33px,8vw,48px); letter-spacing: -1.5px; }
  .hero-orb { width: 82px; height: 82px; right: 5%; top: 18px; opacity: .52; }
  .hero-kicker { max-width: 85%; letter-spacing: 1.4px; font-size: 9px; }
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎓 Student Nexus")
    st.caption("STUDENT MANAGEMENT SUITE")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Add Student", "View Students", "Search Student",
         "Update Student", "Delete Student", "Calculate CGPA", "Find Topper",
         "Sort Students", "Student Skills", "Attendance Tracker",
         "Subject Marks", "Report Cards", "Class Insights", "Import / Export"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("**🟢 Local storage active**")
    st.caption("Records are saved to students.json on this device.")
    if st.button("↻ Restore demo data", use_container_width=True):
        st.session_state.students = {key: value.copy() for key, value in DEFAULT_STUDENTS.items()}
        save_students()
        st.success("Demo data restored.")
        st.rerun()

st.markdown("""
<div class="hero">
  <div class="hero-orb" aria-hidden="true"></div>
  <div class="hero-kicker">Academic intelligence • Student records</div>
  <div class="hero-title" aria-label="Student Nexus">Student Nexus <span aria-hidden="true">↗</span></div>
  <div class="hero-sub">A smarter space to manage student records, track academic performance,
  discover top performers, and keep useful skills in one clean dashboard.</div>
</div>
""", unsafe_allow_html=True)

if page == "Dashboard":
    rows = student_rows()
    total = len(rows)
    average = round(sum(r["Marks"] for r in rows) / total, 1) if total else 0
    top = max(rows, key=lambda r: r["Marks"]) if rows else None
    skill_count = len({skill.strip() for s in students.values() for skill in s.get("skills", []) if skill.strip()})
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Students", total, "Total registered records", "👥")
    with c2: metric_card("Average marks", f"{average}%", "Across all students", "📈")
    with c3: metric_card("Top score", f"{top['Marks']}%" if top else "—", top["Name"] if top else "No records yet", "🏆")
    with c4: metric_card("Unique skills", skill_count, "Skills across the student body", "⚡")

    st.markdown("### 📊 Academic overview")
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Marks leaderboard")
        if rows:
            df = pd.DataFrame(rows).sort_values("Marks", ascending=False)
            st.bar_chart(df.set_index("Name")[["Marks"]], height=270)
        else:
            st.info("Add a student to start building the leaderboard.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("✨ Top performer")
        if top:
            st.markdown(f"## 🥇 {top['Name']}")
            st.markdown(f"**Student ID:** `{top['Student ID']}`")
            st.markdown(f"**Marks:** {top['Marks']} / 100")
            st.markdown(f"**CGPA:** {top['CGPA']} / 10")
            st.progress(min(float(top["Marks"]) / 100, 1.0))
        else:
            st.info("No student data available.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🗂️ Recently available records")
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("Your student directory is empty. Use **Add Student** to create the first record.")

elif page == "Add Student":
    st.subheader("➕ Register a student")
    st.caption("Enter a unique ID and complete the student's profile.")
    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sid = st.text_input("Student ID", placeholder="e.g. 106").strip()
            name = st.text_input("Full name", placeholder="Enter student name").strip()
            age = st.number_input("Age", min_value=1, max_value=100, value=18)
        with col2:
            marks = st.number_input("Marks (out of 100)", min_value=0, max_value=100, value=75)
            skills_text = st.text_input("Skills", placeholder="Python, DSA, Communication")
            st.caption("Separate multiple skills with commas.")
        submitted = st.form_submit_button("＋ Add student", use_container_width=True)
        if submitted:
            if not sid or not sid.isdigit():
                st.error("Student ID must contain numbers only.")
            elif sid in students:
                st.error("That Student ID already exists. Use a unique ID.")
            elif not name:
                st.error("Please enter the student's name.")
            else:
                skills = [x.strip() for x in skills_text.split(",") if x.strip()]
                students[sid] = {"name": name, "age": int(age), "marks": int(marks), "skills": skills}
                save_students()
                st.success(f"{name} (ID {sid}) was added successfully.")
                st.rerun()

elif page == "View Students":
    st.subheader("👥 Student directory")
    rows = student_rows()
    if rows:
        query = st.text_input("Filter by name, ID, or skill", placeholder="Start typing to filter records...")
        filtered = [r for r in rows if query.lower() in " ".join(str(v) for v in r.values()).lower()] if query else rows
        st.caption(f"Showing {len(filtered)} of {len(rows)} student(s)")
        st.dataframe(pd.DataFrame(filtered), use_container_width=True, hide_index=True)
        csv = pd.DataFrame(filtered).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download visible records as CSV", csv, "students.csv", "text/csv")
    else:
        st.info("No students found. Add a student to get started.")

elif page == "Search Student":
    st.subheader("🔎 Find a student")
    sid = st.text_input("Enter Student ID", placeholder="e.g. 101").strip()
    if st.button("Search record"):
        record = students.get(sid)
        if record:
            a, b = st.columns(2)
            with a:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown(f"## 👤 {record['name']}")
                st.write(f"**Student ID:** {sid}")
                st.write(f"**Age:** {record.get('age', '—')}")
                st.write(f"**Marks:** {record.get('marks', 0)} / 100")
                st.write(f"**CGPA:** {cgpa(record.get('marks', 0))} / 10")
                st.markdown("</div>", unsafe_allow_html=True)
            with b:
                st.markdown('<div class="panel">', unsafe_allow_html=True)
                st.markdown("### 🧠 Skills")
                skills = record.get("skills", [])
                st.write(", ".join(skills) if skills else "No skills added yet.")
                st.progress(min(float(record.get("marks", 0)) / 100, 1.0))
                st.caption("Academic marks")
                st.markdown("</div>", unsafe_allow_html=True)
        elif sid:
            st.warning("No student found with that ID.")

elif page == "Update Student":
    st.subheader("✏️ Update student profile")
    if not students:
        st.info("There are no records to update.")
    else:
        sid = st.selectbox("Choose Student ID", list(students.keys()), format_func=lambda x: f"{x} — {students[x]['name']}")
        record = students[sid]
        with st.form("update_student_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Student name", value=record.get("name", ""))
                age = st.number_input("Age", min_value=1, max_value=100, value=int(record.get("age", 18)))
            with col2:
                marks = st.number_input("Marks (out of 100)", min_value=0, max_value=100, value=int(record.get("marks", 0)))
                skills_text = st.text_input("Skills", value=", ".join(record.get("skills", [])))
            if st.form_submit_button("Save changes", use_container_width=True):
                if not name.strip():
                    st.error("Student name cannot be empty.")
                else:
                    students[sid] = {
                        "name": name.strip(), "age": int(age), "marks": int(marks),
                        "skills": [x.strip() for x in skills_text.split(",") if x.strip()],
                    }
                    save_students()
                    st.success("Student profile updated.")
                    st.rerun()

elif page == "Delete Student":
    st.subheader("🗑️ Remove a student record")
    if not students:
        st.info("There are no records to delete.")
    else:
        sid = st.selectbox("Select student to delete", list(students.keys()), format_func=lambda x: f"{x} — {students[x]['name']}")
        st.warning(f"You are about to delete **{students[sid]['name']}** (ID {sid}). This cannot be undone.")
        confirm = st.checkbox("I confirm that I want to delete this record.")
        if st.button("Delete student", disabled=not confirm):
            name = students[sid]["name"]
            del students[sid]
            save_students()
            st.success(f"{name}'s record was deleted.")
            st.rerun()

elif page == "Calculate CGPA":
    st.subheader("🎯 CGPA calculator")
    st.caption("This project uses a simple conversion: CGPA = marks ÷ 10. Adjust the formula if your college uses a different grading rule.")
    if students:
        sid = st.selectbox("Select student", list(students.keys()), format_func=lambda x: f"{x} — {students[x]['name']}")
        record = students[sid]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(f"### {record['name']}")
            st.metric("Marks", f"{record.get('marks', 0)} / 100")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("### Calculated result")
            st.metric("Estimated CGPA", f"{cgpa(record.get('marks', 0))} / 10")
            st.progress(min(float(record.get("marks", 0)) / 100, 1.0))
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Add a student before calculating CGPA.")

elif page == "Find Topper":
    st.subheader("🏆 Find the class topper")
    rows = student_rows()
    if rows:
        top = max(rows, key=lambda r: (r["Marks"], r["CGPA"], r["Name"]))
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"## 🥇 {top['Name']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Student ID", top["Student ID"])
        c2.metric("Marks", f"{top['Marks']} / 100")
        c3.metric("CGPA", f"{top['CGPA']} / 10")
        st.markdown("</div>", unsafe_allow_html=True)
        ties = [r for r in rows if r["Marks"] == top["Marks"]]
        if len(ties) > 1:
            st.info("There is a tie for the highest marks: " + ", ".join(r["Name"] for r in ties))
    else:
        st.info("No student records are available yet.")

elif page == "Sort Students":
    st.subheader("↕️ Sort student records")
    rows = student_rows()
    if rows:
        col1, col2 = st.columns(2)
        sort_by = col1.selectbox("Sort by", ["Name", "Student ID", "Age", "Marks", "CGPA"])
        order = col2.selectbox("Order", ["Descending", "Ascending"])
        df = pd.DataFrame(rows).sort_values(sort_by, ascending=(order == "Ascending"), kind="stable")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No records to sort.")

elif page == "Student Skills":
    st.subheader("⚡ Student skills explorer")
    if students:
        all_skills = sorted({skill for record in students.values() for skill in record.get("skills", [])})
        if all_skills:
            selected_skill = st.selectbox("Choose a skill", all_skills)
            matches = [
                {"Student ID": sid, "Name": record["name"], "Age": record.get("age", "—"),
                 "Marks": record.get("marks", 0), "Skills": ", ".join(record.get("skills", []))}
                for sid, record in students.items()
                if selected_skill.lower() in [s.lower() for s in record.get("skills", [])]
            ]
            st.markdown(f"### Students with **{selected_skill}**")
            st.dataframe(pd.DataFrame(matches), use_container_width=True, hide_index=True)
            st.success(f"{len(matches)} student(s) have this skill.")
        else:
            st.info("No skills have been recorded. Add skills in Add Student or Update Student.")
        st.markdown("### All skills")
        skill_counts = {}
        for record in students.values():
            for skill in record.get("skills", []):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        if skill_counts:
            st.bar_chart(pd.DataFrame({"Students": skill_counts}).sort_values("Students", ascending=False))
    else:
        st.info("Add students to explore their skills.")

elif page == "Attendance Tracker":
    st.subheader("🗓️ Attendance tracker")
    st.caption("Record daily attendance for each student. Attendance history is saved in students.json.")
    if "attendance" not in st.session_state:
        st.session_state.attendance = {}
    attendance = st.session_state.attendance
    attendance_date = st.date_input("Attendance date")
    date_key = attendance_date.isoformat()
    if not students:
        st.info("Add students before taking attendance.")
    else:
        saved_for_date = attendance.get(date_key, {})
        with st.form("attendance_form"):
            attendance_choices = {}
            cols = st.columns(2)
            for idx, (sid, record) in enumerate(students.items()):
                with cols[idx % 2]:
                    attendance_choices[sid] = st.radio(
                        f"{record.get('name', 'Student')} · ID {sid}",
                        ["Present", "Absent", "Late"],
                        index=["Present", "Absent", "Late"].index(saved_for_date.get(sid, "Present")),
                        horizontal=True,
                        key=f"att_{date_key}_{sid}",
                    )
            if st.form_submit_button("💾 Save attendance", use_container_width=True):
                attendance[date_key] = attendance_choices
                students_meta = {
                    "students": students,
                    "attendance": attendance,
                    "subject_marks": st.session_state.get("subject_marks", {}),
                }
                DATA_FILE.write_text(json.dumps(students_meta, indent=2), encoding="utf-8")
                st.success(f"Attendance saved for {attendance_date.strftime('%d %b %Y')}.")
                st.rerun()
        if saved_for_date:
            counts = pd.Series(list(saved_for_date.values())).value_counts()
            a, b, c = st.columns(3)
            a.metric("Present", int(counts.get("Present", 0)))
            b.metric("Absent", int(counts.get("Absent", 0)))
            c.metric("Late", int(counts.get("Late", 0)))
            st.dataframe(pd.DataFrame([
                {"Student ID": sid, "Name": students.get(sid, {}).get("name", "Unknown"), "Status": status}
                for sid, status in saved_for_date.items()
            ]), use_container_width=True, hide_index=True)

elif page == "Subject Marks":
    st.subheader("📚 Subject-wise marks")
    st.caption("Add marks for multiple subjects and see a calculated average for a selected student.")
    if "subject_marks" not in st.session_state:
        st.session_state.subject_marks = {}
    subject_marks = st.session_state.subject_marks
    if students:
        sid = st.selectbox("Select student", list(students.keys()), format_func=lambda x: f"{x} — {students[x]['name']}")
        current = subject_marks.get(sid, {})
        with st.form("subject_marks_form"):
            subject_names = st.text_input("Subjects (comma-separated)", value=", ".join(current.keys()), placeholder="Python, Maths, Physics")
            marks_text = st.text_input("Marks for those subjects (comma-separated)", value=", ".join(str(v) for v in current.values()), placeholder="85, 90, 78")
            if st.form_submit_button("Save subject marks", use_container_width=True):
                names = [n.strip() for n in subject_names.split(",") if n.strip()]
                values = [v.strip() for v in marks_text.split(",") if v.strip()]
                try:
                    parsed = [float(v) for v in values]
                    if not names or len(names) != len(parsed):
                        st.error("Enter the same number of subjects and marks.")
                    elif any(v < 0 or v > 100 for v in parsed):
                        st.error("Each subject mark must be between 0 and 100.")
                    else:
                        subject_marks[sid] = dict(zip(names, parsed))
                        st.success("Subject marks saved for this session.")
                        st.rerun()
                except ValueError:
                    st.error("Marks must be numeric values.")
        if current:
            df_subjects = pd.DataFrame([{"Subject": k, "Marks": v} for k, v in current.items()])
            avg = sum(current.values()) / len(current)
            a, b = st.columns([1, 2])
            a.metric("Subject average", f"{avg:.1f}%")
            a.metric("Subject CGPA estimate", f"{avg / 10:.2f} / 10")
            b.bar_chart(df_subjects.set_index("Subject"))
            st.dataframe(df_subjects, use_container_width=True, hide_index=True)
    else:
        st.info("Add a student first.")

elif page == "Report Cards":
    st.subheader("🪪 Student report card")
    st.caption("Create a printable-style summary and download an individual report as a text file.")
    if students:
        sid = st.selectbox("Choose student", list(students.keys()), format_func=lambda x: f"{x} — {students[x]['name']}")
        record = students[sid]
        subjects = st.session_state.get("subject_marks", {}).get(sid, {})
        report_average = sum(subjects.values()) / len(subjects) if subjects else float(record.get("marks", 0))
        report_skills = ", ".join(record.get("skills", [])) or "Not provided"
        st.markdown(f"""
        <div class="hero">
          <div class="hero-kicker">Official student summary</div>
          <div class="hero-title">🎓 {record.get('name', 'Student')}</div>
          <div class="hero-sub">Student ID: {sid} &nbsp; • &nbsp; Age: {record.get('age', '—')}</div>
          <hr>
          <h3>Academic performance</h3>
          <p>Overall marks: <b>{record.get('marks', 0)} / 100</b></p>
          <p>Estimated CGPA: <b>{cgpa(record.get('marks', 0))} / 10</b></p>
          <p>Subject average: <b>{report_average:.1f}%</b></p>
          <p>Skills: <b>{report_skills}</b></p>
        </div>
        """, unsafe_allow_html=True)
        report_text = (
            f"STUDENT NEXUS - STUDENT REPORT CARD\n"
            f"Student ID: {sid}\nName: {record.get('name', '')}\nAge: {record.get('age', '')}\n"
            f"Overall marks: {record.get('marks', 0)}/100\nEstimated CGPA: {cgpa(record.get('marks', 0))}/10\n"
            f"Subject average: {report_average:.1f}%\nSkills: {report_skills}\n\n"
            + ("Subject marks:\n" + "\n".join(f"- {k}: {v}/100" for k, v in subjects.items()) if subjects else "No subject-wise marks recorded.")
        )
        st.download_button("⬇️ Download report card (.txt)", report_text, f"report_card_{sid}.txt", "text/plain")
    else:
        st.info("Add a student to generate a report card.")

elif page == "Class Insights":
    st.subheader("🧠 Class insights")
    rows = student_rows()
    if rows:
        df = pd.DataFrame(rows)
        avg = float(df["Marks"].mean())
        pass_mark = st.number_input("Passing marks threshold", min_value=0, max_value=100, value=40)
        passed = int((df["Marks"] >= pass_mark).sum())
        failed = len(df) - passed
        a, b, c, d = st.columns(4)
        a.metric("Class average", f"{avg:.1f}%")
        b.metric("Pass rate", f"{passed / len(df) * 100:.1f}%")
        c.metric("At/above threshold", passed)
        d.metric("Below threshold", failed)
        st.markdown("### Performance distribution")
        bins = pd.cut(df["Marks"], bins=[-1, 39, 59, 74, 89, 100], labels=["0–39", "40–59", "60–74", "75–89", "90–100"])
        distribution = bins.value_counts(sort=False)
        st.bar_chart(distribution)
        st.markdown("### Students who may need support")
        support = df[df["Marks"] < pass_mark][["Student ID", "Name", "Marks", "CGPA"]]
        if support.empty:
            st.success("Everyone is at or above the selected threshold.")
        else:
            st.dataframe(support, use_container_width=True, hide_index=True)
    else:
        st.info("Add student records to see class insights.")

elif page == "Import / Export":
    st.subheader("📦 Import, export & backup")
    st.caption("Download a backup of all student data or import student records from a CSV file.")
    students_json = json.dumps(students, indent=2).encode("utf-8")
    st.download_button("⬇️ Download full JSON backup", students_json, "students_backup.json", "application/json", use_container_width=True)
    if students:
        all_csv = pd.DataFrame(student_rows()).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export student table as CSV", all_csv, "student_records.csv", "text/csv", use_container_width=True)
    uploaded = st.file_uploader("Import CSV (columns: Student ID, Name, Age, Marks, Skills)", type=["csv"])
    if uploaded is not None:
        try:
            imported_df = pd.read_csv(uploaded)
            st.write("Preview imported records")
            st.dataframe(imported_df.head(10), use_container_width=True, hide_index=True)
            if st.button("Import / merge these records"):
                required = {"Student ID", "Name", "Age", "Marks"}
                if not required.issubset(set(imported_df.columns)):
                    st.error("CSV must contain Student ID, Name, Age and Marks columns.")
                else:
                    added, skipped = 0, 0
                    for _, row in imported_df.iterrows():
                        sid = str(row["Student ID"]).strip()
                        try:
                            age_value, marks_value = int(row["Age"]), float(row["Marks"])
                            name_value = str(row["Name"]).strip()
                            if not sid or not sid.isdigit() or not name_value or not (1 <= age_value <= 100) or not (0 <= marks_value <= 100):
                                skipped += 1
                                continue
                            raw_skills = str(row.get("Skills", ""))
                            skills_value = [s.strip() for s in raw_skills.split(",") if s.strip() and s.strip().lower() != "nan"]
                            students[sid] = {"name": name_value, "age": age_value, "marks": marks_value, "skills": skills_value}
                            added += 1
                        except (ValueError, TypeError):
                            skipped += 1
                    save_students()
                    st.success(f"Imported/updated {added} record(s). Skipped {skipped} invalid record(s).")
                    st.rerun()
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")

st.markdown("---")
st.markdown('<div class="small-muted">STUDENT NEXUS • Built with Python + Streamlit • Demo data is stored locally in students.json</div>', unsafe_allow_html=True)
