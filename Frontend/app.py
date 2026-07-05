import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(
    page_title="Verba AI · AI Language Translator",
    page_icon="🌍",
    layout="wide"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

/* Reset and Global Rules */
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #04040a !important;
    color: #f8fafc !important;
}

/* Glassmorphic Background Blur Orbs */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(99, 102, 241, 0) 70%);
    top: -100px;
    left: -100px;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, rgba(168, 85, 247, 0) 70%);
    bottom: -150px;
    right: -150px;
    pointer-events: none;
    z-index: 0;
}

/* Hide Default Streamlit Elements */
[data-testid="stHeader"] {
    display: none !important;
    height: 0px !important;
}
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer { display: none !important; visibility: hidden !important; }

/* Remove default Streamlit top section padding */
[data-testid="stAppViewContainer"] > section {
    padding-top: 0rem !important;
}

/* Main Container spacing */
.main .block-container {
    max-width: 1200px !important;
    padding-top: 0.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-bottom: 5rem !important;
    position: relative;
    z-index: 1;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.4); border-radius: 10px; }

/* Header Styling */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 3.5rem;
}
.header-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}
.logo-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    border-radius: 12px;
    display: grid; place-items: center;
    font-size: 1.3rem;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35);
}
.logo-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #fff;
}
.logo-name span {
    background: linear-gradient(135deg, #a855f7, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header-tag {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #cbd5e1;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 6px 14px;
    border-radius: 100px;
    backdrop-filter: blur(10px);
}
.dot {
    width: 6px; height: 6px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 1.8s infinite;
}
@keyframes pulse { 0%,100%{opacity:1; transform: scale(1);} 50%{opacity:.3; transform: scale(0.85);} }

/* Cards (Glass Panels) */
.glass-panel {
    background: rgba(13, 13, 27, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 28px;
    padding: 2.25rem;
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.06);
    height: 100%;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.glass-panel:hover {
    border-color: rgba(99, 102, 241, 0.2);
}

.panel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.panel-title-left {
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Detected Badge */
.detected-badge {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: #34d399;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 8px;
    letter-spacing: 0.02em;
}

/* Counters Row */
.stats-badge-row {
    display: flex;
    gap: 10px;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}
.stats-badge {
    font-size: 0.72rem;
    font-weight: 600;
    color: #94a3b8;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 4px 10px;
    border-radius: 8px;
}

/* Textarea Custom Styling */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    color: #f8fafc !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1.05rem !important;
    line-height: 1.75 !important;
    padding: 1.25rem !important;
    resize: none !important;
    transition: all 0.25s ease !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99, 102, 241, 0.5) !important;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.15) !important;
}
.stTextArea textarea::placeholder { color: #475569 !important; font-style: italic; }

/* Custom Output Box Display */
.output-box {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.25rem;
    min-height: 280px;
    max-height: 280px;
    overflow-y: auto;
    color: #f8fafc;
    font-size: 1.05rem;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.output-placeholder {
    color: #475569;
    font-style: italic;
}

/* Custom Selectbox styling */
[data-testid="stSelectbox"] label {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #94a3b8 !important;
    margin-bottom: 6px !important;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    height: 42px !important;
    font-weight: 500 !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(99, 102, 241, 0.5) !important;
}
[data-testid="stSelectbox"] > div > div > div { color: #f1f5f9 !important; }

/* Primary Action Button */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 12px !important;
    border-radius: 12px !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35) !important;
    margin-top: 1rem !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.45) !important;
}
.stButton>button:active {
    transform: translateY(0) !important;
}

/* History Box Styling */
.history-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #fff;
    margin-top: 4rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 0.75rem;
}
[data-testid="stExpander"] {
    background: rgba(13, 13, 27, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 14px !important;
    margin-bottom: 12px !important;
    backdrop-filter: blur(10px);
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #cbd5e1 !important;
    font-size: 0.9rem !important;
}

/* Custom styled alerts */
[data-testid="stAlert"] {
    background: rgba(239, 68, 68, 0.08) !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-radius: 12px !important;
}
[data-testid="stAlertContainer"] p { color: #fca5a5 !important; }
[data-testid="stSpinner"] > div { border-top-color: #6366f1 !important; }

/* Responsive adjustments */
@media (max-width: 768px) {
    .main .block-container { padding: 1.5rem 1rem 3rem !important; }
    .glass-panel { padding: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Session State Initialisation ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "translated_output" not in st.session_state:
    st.session_state.translated_output = ""
if "detected_language" not in st.session_state:
    st.session_state.detected_language = ""

# ════════════ LOGO HEADER ═════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
  <div class="header-logo">
    <div class="logo-icon">🌐</div>
    <span class="logo-name">Verba <span>AI</span></span>
  </div>
  <div class="header-tag">
    <span class="dot"></span>
    <span>AI Live · Groq · Llama 3.3</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Language Options
languages = [
    "English", "Hindi", "Bengali", "Spanish", "French", "German",
    "Italian", "Japanese", "Chinese", "Korean", "Arabic",
    "Russian", "Tamil", "Telugu", "Malayalam", "Urdu"
]

# Columns for side-by-side workspace
col1, col2 = st.columns([1, 1])

# ════════════ INPUT COLUMN ════════════════════════════════════════════════════
with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    # Title showing detected language dynamically
    detected_indicator = ""
    if st.session_state.detected_language:
         detected_indicator = f'<span class="detected-badge">Detected: {st.session_state.detected_language}</span>'
    
    st.markdown(f"""
    <div class="panel-title">
        <div class="panel-title-left">📝 Source Input</div>
        {detected_indicator}
    </div>
    """, unsafe_allow_html=True)
    
    text = st.text_area(
        "Source Text",
        height=280,
        placeholder="Type or paste text to translate...",
        key="input_text_area",
        label_visibility="collapsed"
    )
    
    # Inline Stats
    char_len = len(text) if text else 0
    word_len = len(text.split()) if text else 0
    
    st.markdown(f"""
    <div class="stats-badge-row">
        <span class="stats-badge">Characters: {char_len}</span>
        <span class="stats-badge">Words: {word_len}</span>
    </div>
    """, unsafe_allow_html=True)

    language = st.selectbox(
        "Target Language",
        languages,
        key="target_language_select"
    )

    translate_clicked = st.button("🚀 Translate Now")
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════ OUTPUT COLUMN ═══════════════════════════════════════════════════
with col2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title"><div class="panel-title-left">✨ Translation Output</div></div>', unsafe_allow_html=True)
    
    if translate_clicked:
        if not text.strip():
            st.warning("⚠️ Please enter some text to translate.")
            st.session_state.translated_output = ""
            st.session_state.detected_language = ""
        else:
            with st.spinner("Translating..."):
                try:
                    # Make post request safely
                    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
                    response = requests.post(
                        f"{backend_url}/translate",
                        json={
                            "text": text,
                            "target_language": language
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        translated_text = res_data.get("translated_text", "")
                        detected_lang = res_data.get("detected_language", "")
                        
                        st.session_state.translated_output = translated_text
                        st.session_state.detected_language = detected_lang
                    else:
                        st.error(f"❌ Error from translator service (Status code: {response.status_code})")
                except Exception as e:
                    st.error(f"❌ Could not reach the translation service. Make sure the backend is running.\n\n`{e}`")

    # Display output as a beautifully styled read-only box
    if st.session_state.translated_output:
        st.markdown(f'<div class="output-box">{st.session_state.translated_output}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="output-box output-placeholder">Translation will appear here...</div>', unsafe_allow_html=True)

    # Show raw code preview copybox if output is active
    if st.session_state.translated_output:
        st.write("") # spacing
        st.info("💡 Tip: Copy the translated text below")
        st.code(st.session_state.translated_output, language="")

    st.markdown("</div>", unsafe_allow_html=True)