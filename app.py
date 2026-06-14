import streamlit as st
import time
import re
from datetime import datetime
from agents import writer_chain, critic_chain
from tools import web_search, scrape_url
from report_exporter import export_pdf, export_docx

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


for key, default in [
    ("results",      {}),
    ("running",      False),
    ("done",         False),
    ("history",      []),
    ("loaded_report",None),
    ("max_sources",  3),
]:
    if key not in st.session_state:
        st.session_state[key] = default


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}
.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.07) 0%, transparent 55%);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 100%; }


[data-testid="stSidebar"] {
    background: #0d0d16 !important;
    border-right: 1px solid rgba(255,140,50,0.2) !important;
    min-width: 270px !important;
    max-width: 270px !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
[data-testid="stSidebarContent"] {
    display: flex !important;
    flex-direction: column !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Re-open tab — the orange pill on left edge when sidebar is collapsed */
[data-testid="stSidebarCollapsedControl"] {
    background: rgba(255,140,50,0.2) !important;
    border: 1px solid rgba(255,140,50,0.5) !important;
    border-left: none !important;
    border-radius: 0 12px 12px 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    height: 60px !important;
    width: 24px !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999 !important;
}
[data-testid="stSidebarCollapsedControl"]:hover {
    background: rgba(255,140,50,0.35) !important;
    width: 32px !important;
}
[data-testid="stSidebarCollapsedControl"] svg {
    color: #ff8c32 !important;
    fill: #ff8c32 !important;
}


[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #706860 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #c8c3b8 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    color: #706860 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.66rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.06em !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 7px !important;
    padding: 0.28rem 0.7rem !important;
    box-shadow: none !important;
    transform: none !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,140,50,0.1) !important;
    color: #ff8c32 !important;
    border-color: rgba(255,140,50,0.3) !important;
    transform: none !important;
    box-shadow: none !important;
}


[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: #f0ebe0 !important;
}


.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #706860 !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    border: none !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,140,50,0.15) !important;
    color: #ff8c32 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }


.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
    color: #f0ebe0 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

            
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.8rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
}
.stDownloadButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: #a09890 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    border-color: rgba(255,140,50,0.3) !important;
    color: #ff8c32 !important;
    transform: none !important;
}


.source-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s, transform 0.2s;
}
.source-card:hover { border-color: rgba(255,140,50,0.3); transform: translateY(-2px); }
.source-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700; color:#f0ebe0; margin-bottom:0.3rem; }
.source-url   { font-family:'DM Mono',monospace; font-size:0.66rem; color:#ff8c32; opacity:0.65;
                white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:0.45rem; }
.source-badge { display:inline-block; font-family:'DM Mono',monospace; font-size:0.6rem;
                letter-spacing:0.08em; text-transform:uppercase; padding:0.18rem 0.55rem;
                border-radius:4px; margin-right:0.35rem; }
.badge-high     { background:rgba(80,200,120,0.12);  color:#50c878; border:1px solid rgba(80,200,120,0.25); }
.badge-medium   { background:rgba(255,200,50,0.1);   color:#ffc832; border:1px solid rgba(255,200,50,0.2); }
.badge-news     { background:rgba(100,150,255,0.1);  color:#6496ff; border:1px solid rgba(100,150,255,0.2); }
.badge-blog     { background:rgba(200,100,255,0.1);  color:#c864ff; border:1px solid rgba(200,100,255,0.2); }
.badge-research { background:rgba(255,140,50,0.1);   color:#ff8c32; border:1px solid rgba(255,140,50,0.2); }


.timeline-item { display:flex; align-items:flex-start; gap:1rem; margin-bottom:1.2rem; }
.timeline-dot  { width:32px; height:32px; border-radius:50%; display:flex; align-items:center;
                 justify-content:center; font-size:0.85rem; flex-shrink:0; margin-top:2px; }
.dot-done    { background:rgba(80,200,120,0.2);   border:1px solid rgba(80,200,120,0.5);  color:#50c878; }
.dot-running { background:rgba(255,140,50,0.2);   border:1px solid rgba(255,140,50,0.5);  color:#ff8c32; }
.dot-waiting { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); color:#2a2420; }
.timeline-content { flex:1; }
.timeline-title { font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#f0ebe0; margin-bottom:0.12rem; }
.timeline-meta  { font-family:'DM Mono',monospace; font-size:0.65rem; color:#555048; letter-spacing:0.08em; }


.hero { padding:1.5rem 0 1rem; }
.hero-eyebrow { font-family:'DM Mono',monospace; font-size:0.68rem; letter-spacing:0.25em;
                text-transform:uppercase; color:#ff8c32; margin-bottom:0.6rem; opacity:0.9; }
.hero h1 { font-family:'Syne',sans-serif; font-size:clamp(2rem,4vw,3.2rem); font-weight:800;
           letter-spacing:-0.03em; color:#f0ebe0; margin:0 0 0.5rem; line-height:1.05; }
.hero h1 span { color:#ff8c32; }
.hero-sub { font-size:0.9rem; font-weight:300; color:#706860; line-height:1.6; }


.glass-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.8rem 2rem; margin-bottom: 1.2rem;
    backdrop-filter: blur(12px); box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.panel-label { font-family:'DM Mono',monospace; font-size:0.68rem; letter-spacing:0.2em;
               text-transform:uppercase; padding-bottom:0.8rem; margin-bottom:1rem;
               border-bottom:1px solid rgba(255,255,255,0.06); }
.label-orange { color:#ff8c32; }
.label-green  { color:#50c878; }
.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(255,140,50,0.25),transparent); margin:1.5rem 0; }


.hist-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 0.65rem 0.8rem; margin-bottom: 0.35rem;
    transition: border-color 0.18s, background 0.18s;
}
.hist-card:hover { border-color: rgba(255,140,50,0.25); background: rgba(255,140,50,0.04); }
.hist-topic { font-family:'Syne',sans-serif; font-size:0.8rem; font-weight:600; color:#c0bab0;
              white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:0.1rem; }
.hist-time  { font-family:'DM Mono',monospace; font-size:0.58rem; color:#3a3028; letter-spacing:0.07em; }

.sb-divider { height:1px; background:rgba(255,140,50,0.1); margin:0.9rem 0; }
.sb-label   { font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.22em;
              text-transform:uppercase; color:#ff8c32; opacity:0.8; margin-bottom:0.65rem;
              display:block; }
.stSpinner > div { color:#ff8c32 !important; }
details summary { font-family:'DM Mono',monospace !important; font-size:0.7rem !important;
                  color:#706860 !important; letter-spacing:0.1em !important; }
</style>
""", unsafe_allow_html=True)



def extract_urls(text):
    urls = re.findall(r"https?://[^\s]+", text)
    return [u.rstrip(".,);]") for u in urls]

def count_words(text):
    return len(text.split())

def parse_quality_score(critic_text):
    m = re.search(r"Score:\s*([\d.]+)/10", critic_text or "")
    return m.group(1) if m else "N/A"

def classify_source(url):
    u = url.lower()
    if any(x in u for x in ["arxiv","nature","pubmed","ieee","scholar","research","journal","science"]):
        return ("Research","badge-research"), "🔬"
    if any(x in u for x in ["news","reuters","bbc","cnn","nytimes","guardian","techcrunch","wired"]):
        return ("News","badge-news"), "📰"
    if any(x in u for x in [".gov",".edu"]):
        return ("Official","badge-high"), "🏛️"
    if any(x in u for x in ["medium","blog","substack","dev.to","hashnode"]):
        return ("Blog","badge-blog"), "✍️"
    return ("Web","badge-medium"), "🌐"

def credibility_label(url):
    u = url.lower()
    if any(x in u for x in [".gov",".edu","arxiv","nature","pubmed","ieee","reuters","bbc","nytimes","guardian"]):
        return "High","badge-high"
    return "Medium","badge-medium"

def domain_name(url):
    m = re.search(r"https?://(?:www\.)?([^/]+)", url)
    return m.group(1) if m else url

def render_timeline(steps_status):
    icons = {"done":"✓","running":"●","waiting":"○"}
    for step in steps_status:
        meta = step.get("meta","")
        st.markdown(
            f'<div class="timeline-item">'
            f'<div class="timeline-dot dot-{step["state"]}">{icons[step["state"]]}</div>'
            f'<div class="timeline-content">'
            f'<div class="timeline-title">{step["title"]}</div>'
            + (f'<div class="timeline-meta">{meta}</div>' if meta else "")
            + '</div></div>',
            unsafe_allow_html=True,
        )

def render_source_card(url, idx):
    (type_label, type_badge), icon = classify_source(url)
    cred_label, cred_badge = credibility_label(url)
    domain = domain_name(url)
    st.markdown(
        f'<div class="source-card">'
        f'<div class="source-title">{icon} {domain}</div>'
        f'<div class="source-url">{url}</div>'
        f'<span class="source-badge {type_badge}">{type_label}</span>'
        f'<span class="source-badge {cred_badge}">Credibility: {cred_label}</span>'
        f'<a href="{url}" target="_blank" style="font-family:\'DM Mono\',monospace;font-size:0.63rem;'
        f'color:#4a4035;text-decoration:none;margin-left:0.4rem;">&#8599; Open</a>'
        f'</div>',
        unsafe_allow_html=True,
    )





with st.sidebar:

    
    st.markdown(
        '<div style="padding:1.2rem 0.2rem 0.8rem;">'
        '<div style="font-family:\'DM Mono\',monospace;font-size:0.58rem;letter-spacing:0.28em;'
        'text-transform:uppercase;color:#ff8c32;margin-bottom:0.3rem;">ResearchMind</div>'
        '<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:800;'
        'color:#f0ebe0;line-height:1.15;margin-bottom:0.22rem;">AI Research<br>Agent</div>'
        '<div style="font-family:\'DM Mono\',monospace;font-size:0.6rem;'
        'color:#3e3428;letter-spacing:0.1em;">by Rohit Patel</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    
    st.markdown('<span class="sb-label">⚙ Settings</span>', unsafe_allow_html=True)

    max_sources = st.slider(
        "Max Sources to Scrape", 1, 5,
        st.session_state.max_sources,
        key="max_src_sl",
    )
    st.session_state.max_sources = max_sources

    st.selectbox(
        "Report Depth",
        ["Standard", "Deep", "Quick Summary"],
        key="depth_sel",
    )

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    
    st.markdown('<span class="sb-label">📋 Recent Reports</span>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            '<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;'
            'color:#2a2018;text-align:center;padding:1rem 0.4rem;'
            'border:1px dashed rgba(255,255,255,0.05);border-radius:8px;">'
            'No reports yet</div>',
            unsafe_allow_html=True,
        )
    else:
        for i, item in enumerate(reversed(st.session_state.history[-12:])):
            t = item["topic"].replace("<","&lt;").replace(">","&gt;")
            st.markdown(
                f'<div class="hist-card">'
                f'<div class="hist-topic">{t}</div>'
                f'<div class="hist-time">{item["time"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button("↩ Load", key=f"ld_{i}", use_container_width=True):
                st.session_state.results       = item["results"]
                st.session_state.done          = True
                st.session_state.loaded_report = item["topic"]
                st.rerun()

    # spacer at bottom
    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)




col_main, col_pipe = st.columns([6, 3])

with col_main:
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Multi-Agent AI System</div>
        <h1>Research<span>Mind</span></h1>
        <p class="hero-sub">
            Specialized AI agents collaborate — searching, scraping, writing,
            and critiquing — to deliver a polished research report on any topic.
        </p>
    </div>""", unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
    )

    cb1, cb2 = st.columns([3, 1])
    with cb1:
        run_btn   = st.button("⚡  Run Research Pipeline", use_container_width=True)
    with cb2:
        clear_btn = st.button("✕ Clear", use_container_width=True)

    if clear_btn:
        st.session_state.results       = {}
        st.session_state.done          = False
        st.session_state.loaded_report = None
        st.rerun()

with col_pipe:
    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;'
        'color:#f0ebe0;margin:1.5rem 0 1rem;">Pipeline Status</div>',
        unsafe_allow_html=True,
    )
    r = st.session_state.results

    def step_state(key):
        if key in r: return "done"
        if st.session_state.running:
            for k in ["search","reader","writer","critic"]:
                if k not in r: return "running" if k == key else "waiting"
        return "waiting"

    meta_map = {
        "search": f"{len(extract_urls(r.get('search','')))} URLs found"   if r.get("search") else "",
        "reader": f"{len(r.get('reader','').split())//200} pages scraped" if r.get("reader") else "",
        "writer": f"{count_words(r.get('writer',''))} words"              if r.get("writer") else "",
        "critic": f"Score: {parse_quality_score(r.get('critic',''))}/10"  if r.get("critic") else "",
    }
    render_timeline([
        {"title":"Search Agent","state":step_state("search"),"meta":meta_map["search"]},
        {"title":"Reader Agent","state":step_state("reader"),"meta":meta_map["reader"]},
        {"title":"Writer Chain","state":step_state("writer"),"meta":meta_map["writer"]},
        {"title":"Critic Chain","state":step_state("critic"),"meta":meta_map["critic"]},
    ])



if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results       = {}
        st.session_state.running       = True
        st.session_state.done          = False
        st.session_state.loaded_report = None
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results   = {}
    topic_val = st.session_state.topic_input
    max_src   = st.session_state.max_sources

    with st.status("🔍 Running Research Pipeline...", expanded=True) as status:

        st.write("**Step 1** — Searching the web...")
        results["search"] = web_search.invoke({"query": topic_val})
        st.session_state.results = dict(results)
        st.write(f"✓ Found {len(extract_urls(results['search']))} sources")

        st.write("**Step 2** — Scraping top sources...")
        urls_list = extract_urls(results["search"])
        scraped_text = []
        for url in urls_list[:max_src]:
            content = scrape_url.invoke({"url": url})
            scraped_text.append(f"\nSOURCE: {url}\n\n{content}")
        results["reader"] = "\n\n".join(scraped_text) if scraped_text else "No content scraped."
        st.session_state.results = dict(results)
        st.write(f"✓ Scraped {len(scraped_text)} pages")

        st.write("**Step 3** — Writing research report...")
        results["writer"] = writer_chain.invoke({
            "topic":    topic_val,
            "research": f"SEARCH RESULTS:\n{results['search']}\n\nSCRAPED CONTENT:\n{results['reader']}",
        })
        st.session_state.results = dict(results)
        st.write(f"✓ Report drafted ({count_words(results['writer'])} words)")

        st.write("**Step 4** — Critic reviewing report...")
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)
        st.write(f"✓ Score: {parse_quality_score(results['critic'])}/10")

        status.update(label="✅ Research Pipeline Complete!", state="complete", expanded=False)

    st.session_state.history.append({
        "topic":   topic_val,
        "time":    datetime.now().strftime("%b %d, %H:%M"),
        "results": dict(results),
    })
    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()



r = st.session_state.results

if r and st.session_state.done:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    url_list      = extract_urls(r.get("search",""))
    scraped_count = len([s for s in r.get("reader","").split("SOURCE:") if s.strip()])
    word_count    = count_words(r.get("writer",""))
    quality       = parse_quality_score(r.get("critic",""))

    st.markdown(
        '<div style="font-family:\'Syne\',sans-serif;font-size:1rem;font-weight:700;'
        'color:#f0ebe0;margin-bottom:1rem;">Research Dashboard</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sources Found",   len(url_list))
    c2.metric("Sources Scraped", scraped_count)
    c3.metric("Report Words",    f"{word_count:,}")
    c4.metric("Quality Score",   f"{quality}/10" if quality != "N/A" else "—")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    tab_report, tab_sources, tab_analysis, tab_critic, tab_raw = st.tabs([
        "📝 Report", "🔗 Sources", "📊 Analysis", "🧐 Critic", "🗂 Raw Data"
    ])

    with tab_report:
        st.markdown(
            '<div class="glass-panel">'
            '<div class="panel-label label-orange">Final Research Report</div>',
            unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("**Export Report**")
        d1, d2, d3 = st.columns(3)
        with d1:
            st.download_button("⬇ Markdown", data=r["writer"],
                file_name=f"report_{int(time.time())}.md",
                mime="text/markdown", use_container_width=True)
        with d2:
            try:
                st.download_button("⬇ PDF", data=export_pdf(r["writer"]),
                    file_name=f"report_{int(time.time())}.pdf",
                    mime="application/pdf", use_container_width=True)
            except Exception:
                st.button("⬇ PDF (unavail.)", disabled=True, use_container_width=True)
        with d3:
            try:
                st.download_button("⬇ DOCX", data=export_docx(r["writer"]),
                    file_name=f"report_{int(time.time())}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True)
            except Exception:
                st.button("⬇ DOCX (unavail.)", disabled=True, use_container_width=True)

    with tab_sources:
        if url_list:
            st.markdown(
                f'<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;'
                f'color:#605850;letter-spacing:0.1em;margin-bottom:1.2rem;">'
                f'{len(url_list)} SOURCES DISCOVERED</div>',
                unsafe_allow_html=True)
            for idx, url in enumerate(url_list):
                render_source_card(url, idx)
        else:
            st.info("No URLs found in search results.")

    with tab_analysis:
        try:
            import plotly.graph_objects as go
            from collections import Counter

            type_counts = Counter()
            for url in url_list:
                (label, _), _ = classify_source(url)
                type_counts[label] += 1

            if type_counts:
                st.markdown("#### Source Distribution")
                fig_pie = go.Figure(go.Pie(
                    values=list(type_counts.values()),
                    labels=list(type_counts.keys()),
                    hole=0.45,
                    marker=dict(
                        colors=["#ff8c32","#50c878","#6496ff","#c864ff","#ffc832"],
                        line=dict(color="rgba(0,0,0,0.3)", width=2)),
                    textfont=dict(color="#f0ebe0", size=12)))
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#a09890", font_family="DM Sans",
                    margin=dict(t=20,b=20,l=20,r=20),
                    legend=dict(font=dict(color="#a09890",size=11), bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("#### Keyword Frequency")
            report_text = (r.get("writer","") + " " + r.get("search","")).lower()
            topic_words = [w for w in st.session_state.topic_input.lower().split() if len(w) > 3]
            terms = ["research","study","data","model","system","technology",
                     "analysis","results","findings","approach","method"] + topic_words
            wc = {w: report_text.count(w) for w in dict.fromkeys(terms) if report_text.count(w) > 0}
            if wc:
                swc = dict(sorted(wc.items(), key=lambda x: x[1], reverse=True)[:12])
                fig_bar = go.Figure(go.Bar(
                    x=list(swc.values()), y=list(swc.keys()), orientation="h",
                    marker_color="#ff8c32",
                    marker_line_color="rgba(255,140,50,0.3)", marker_line_width=1))
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#a09890", font_family="DM Sans", height=340,
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#555"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#a09890"),
                    margin=dict(t=10,b=10,l=10,r=10))
                st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("#### Sentiment Overview")
            pos_w = ["breakthrough","success","innovative","promising","effective",
                     "significant","improve","advance","achieve","positive","growth"]
            neg_w = ["challenge","problem","risk","issue","concern","fail",
                     "difficult","limit","barrier","negative","decline"]
            pos = sum(report_text.count(w) for w in pos_w)
            neg = sum(report_text.count(w) for w in neg_w)
            neu = max(0, word_count // 50 - pos - neg)
            fig_s = go.Figure(go.Bar(
                x=["Positive","Neutral","Negative"], y=[pos, neu, neg],
                marker_color=["#50c878","#6496ff","#ff5a1a"],
                marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1))
            fig_s.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#a09890", font_family="DM Sans", height=260,
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_s, use_container_width=True)

        except ImportError:
            st.info("pip install plotly to enable visualizations")

    with tab_critic:
        if r.get("critic"):
            st.markdown(
                '<div class="glass-panel">'
                '<div class="panel-label label-green">Critic Feedback</div>',
                unsafe_allow_html=True)
            st.markdown(r["critic"])
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No critic feedback available.")

    with tab_raw:
        with st.expander("🔍 Raw Search Results", expanded=False):
            st.text(r.get("search",""))
        with st.expander("📄 Raw Scraped Content", expanded=False):
            st.text(r.get("reader",""))



st.markdown(
    '<div style="font-family:\'DM Mono\',monospace;font-size:0.62rem;color:#252018;'
    'text-align:center;margin-top:3rem;letter-spacing:0.1em;">'
    'ResearchMind &middot; LangChain + Groq + Tavily &middot; Streamlit'
    '</div>',
    unsafe_allow_html=True,
)