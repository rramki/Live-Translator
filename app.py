"""
Live Audio Translation App - Streamlit
Captures microphone audio in the browser, transcribes via Web Speech API,
and translates using Claude AI with scrolling display.
"""

import streamlit as st
import streamlit.components.v1 as components

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎙️ Live Translator",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Sidebar: Settings ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    target_language = st.selectbox(
        "Translate to",
        [
            "Spanish", "French", "German", "Japanese", "Korean",
            "Chinese (Simplified)", "Arabic", "Portuguese", "Italian",
            "Russian", "Hindi", "Turkish", "Dutch", "Polish",
            "Vietnamese", "Thai", "Swedish", "Norwegian"
        ],
        index=0
    )

    source_language = st.selectbox(
        "Speak in (source)",
        ["English", "Spanish", "French", "German", "Japanese",
         "Korean", "Chinese", "Arabic", "Portuguese", "Italian",
         "Russian", "Hindi", "Auto-detect"],
        index=0
    )

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Required for AI translation. Get yours at console.anthropic.com"
    )

    st.markdown("---")
    st.markdown("""
**How it works:**
1. Click **Start Listening**
2. Speak into your microphone
3. Watch real-time transcription + translation scroll below

*Uses browser's Web Speech API for transcription and Claude AI for translation.*
    """)

# ─── Main UI ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    letter-spacing: -2px;
    font-size: 2.8rem !important;
    background: linear-gradient(135deg, #00f5a0, #00d9f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0 !important;
}

.subtitle {
    color: #6b6b8a;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0;
    margin-bottom: 2rem;
}

.stButton button {
    background: linear-gradient(135deg, #00f5a0, #00d9f5) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 1px;
}

.info-bar {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #6b6b8a;
    margin-bottom: 1rem;
    display: flex;
    gap: 1.5rem;
}

.badge {
    color: #00f5a0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🌐 Live Translator")
st.markdown('<p class="subtitle">Real-time speech · instant translation</p>', unsafe_allow_html=True)

st.markdown(f"""
<div class="info-bar">
  <span>🎤 Source: <span class="badge">{source_language}</span></span>
  <span>→</span>
  <span>💬 Target: <span class="badge">{target_language}</span></span>
</div>
""", unsafe_allow_html=True)

# ─── Core Component (HTML + JS) ───────────────────────────────────────────────
lang_code_map = {
    "English": "en-US", "Spanish": "es-ES", "French": "fr-FR",
    "German": "de-DE", "Japanese": "ja-JP", "Korean": "ko-KR",
    "Chinese": "zh-CN", "Arabic": "ar-SA", "Portuguese": "pt-BR",
    "Italian": "it-IT", "Russian": "ru-RU", "Hindi": "hi-IN",
    "Auto-detect": ""
}

src_code = lang_code_map.get(source_language, "en-US")

html_component = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital@0;1&family=Syne:wght@700;800&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #0a0a0f;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
    padding: 0;
    min-height: 100vh;
  }}

  .controls {{
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }}

  button {{
    padding: 10px 22px;
    border: none;
    border-radius: 50px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.5px;
  }}

  #startBtn {{
    background: linear-gradient(135deg, #00f5a0, #00d9f5);
    color: #0a0a0f;
  }}
  #startBtn:hover {{ opacity: 0.85; transform: scale(1.02); }}
  #startBtn:disabled {{ opacity: 0.4; cursor: not-allowed; transform: none; }}

  #stopBtn {{
    background: #1e1e30;
    color: #ff6b6b;
    border: 1px solid #ff6b6b44;
  }}
  #stopBtn:hover {{ background: #ff6b6b22; }}
  #stopBtn:disabled {{ opacity: 0.4; cursor: not-allowed; }}

  #clearBtn {{
    background: #1e1e30;
    color: #6b6b8a;
    border: 1px solid #2a2a40;
  }}
  #clearBtn:hover {{ background: #2a2a40; }}

  .status-bar {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #6b6b8a;
  }}

  .dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #2a2a40;
    transition: background 0.3s;
  }}
  .dot.active {{
    background: #00f5a0;
    box-shadow: 0 0 8px #00f5a0;
    animation: pulse 1.2s infinite;
  }}

  @keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.4; }}
  }}

  .panels {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
  }}

  @media (max-width: 600px) {{
    .panels {{ grid-template-columns: 1fr; }}
  }}

  .panel {{
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    overflow: hidden;
  }}

  .panel-header {{
    padding: 10px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 1px solid #1e1e30;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  #transcriptPanel .panel-header {{ color: #00d9f5; }}
  #translationPanel .panel-header {{ color: #00f5a0; }}

  .scroll-box {{
    height: 220px;
    overflow-y: auto;
    padding: 14px;
    scroll-behavior: smooth;
  }}

  .scroll-box::-webkit-scrollbar {{ width: 4px; }}
  .scroll-box::-webkit-scrollbar-track {{ background: transparent; }}
  .scroll-box::-webkit-scrollbar-thumb {{ background: #2a2a40; border-radius: 4px; }}

  .entry {{
    margin-bottom: 12px;
    opacity: 0;
    transform: translateY(8px);
    animation: fadeSlide 0.4s ease forwards;
  }}

  @keyframes fadeSlide {{
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  .entry-time {{
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #3a3a5a;
    margin-bottom: 3px;
  }}

  .entry-text {{
    font-size: 0.9rem;
    line-height: 1.5;
    color: #c8c8e0;
  }}

  .entry-text.transcript {{ color: #c8e8f8; }}
  .entry-text.translation {{
    color: #b8f8d8;
    font-weight: 700;
    font-size: 1rem;
  }}

  .interim {{
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #3a3a5a;
    font-style: italic;
    padding: 8px 14px;
    min-height: 32px;
    border-top: 1px solid #1a1a28;
  }}

  .loading-dot {{
    display: inline-block;
    animation: blink 1s infinite;
    color: #00f5a0;
  }}
  @keyframes blink {{ 0%,100%{{opacity:0}} 50%{{opacity:1}} }}

  .no-support {{
    background: #2a1a1a;
    border: 1px solid #ff6b6b44;
    color: #ff8888;
    padding: 12px 16px;
    border-radius: 10px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.6;
  }}

  #apiWarning {{
    background: #1a1a2a;
    border: 1px solid #f5a00044;
    color: #f5c842;
    padding: 10px 14px;
    border-radius: 10px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    margin-bottom: 12px;
    display: none;
  }}
</style>
</head>
<body>

<div id="apiWarning">⚠ No API key provided — showing transcript only (no translation)</div>

<div class="controls">
  <button id="startBtn" onclick="startListening()">▶ Start Listening</button>
  <button id="stopBtn" onclick="stopListening()" disabled>■ Stop</button>
  <button id="clearBtn" onclick="clearAll()">✕ Clear</button>
</div>

<div class="status-bar">
  <div class="dot" id="statusDot"></div>
  <span id="statusText">Ready to listen</span>
</div>

<div id="noSupport" style="display:none">
  <div class="no-support">
    ❌ <strong>Web Speech API not supported</strong><br/>
    Please use Chrome or Edge on desktop/mobile for live speech recognition.
  </div>
</div>

<div class="panels" id="mainPanels">
  <div class="panel" id="transcriptPanel">
    <div class="panel-header">🎤 Transcript ({source_language})</div>
    <div class="scroll-box" id="transcriptBox"></div>
    <div class="interim" id="interimBox">Waiting for speech...</div>
  </div>
  <div class="panel" id="translationPanel">
    <div class="panel-header">💬 Translation ({target_language})</div>
    <div class="scroll-box" id="translationBox"></div>
    <div class="interim" id="translationStatus">—</div>
  </div>
</div>

<script>
const API_KEY = `{api_key}`;
const TARGET_LANG = `{target_language}`;
const SRC_CODE = `{src_code}`;

let recognition = null;
let isListening = false;
let translationQueue = [];
let isTranslating = false;

if (!API_KEY || API_KEY.trim() === '') {{
  document.getElementById('apiWarning').style.display = 'block';
}}

if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
  document.getElementById('noSupport').style.display = 'block';
  document.getElementById('mainPanels').style.display = 'none';
  document.getElementById('startBtn').disabled = true;
}}

function getTime() {{
  return new Date().toLocaleTimeString([], {{hour:'2-digit', minute:'2-digit', second:'2-digit'}});
}}

function addEntry(boxId, text, cls) {{
  const box = document.getElementById(boxId);
  const entry = document.createElement('div');
  entry.className = 'entry';
  entry.innerHTML = `
    <div class="entry-time">${{getTime()}}</div>
    <div class="entry-text ${{cls}}">${{escHtml(text)}}</div>
  `;
  box.appendChild(entry);
  box.scrollTop = box.scrollHeight;
}}

function escHtml(t) {{
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

function startListening() {{
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = SRC_CODE || 'en-US';
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {{
    isListening = true;
    document.getElementById('statusDot').classList.add('active');
    document.getElementById('statusText').textContent = 'Listening...';
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
    document.getElementById('interimBox').textContent = 'Listening...';
  }};

  recognition.onresult = (event) => {{
    let interim = '';
    let final = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {{
      const t = event.results[i][0].transcript;
      if (event.results[i].isFinal) {{ final += t; }}
      else {{ interim += t; }}
    }}
    if (interim) document.getElementById('interimBox').textContent = '⟩ ' + interim;
    if (final) {{
      document.getElementById('interimBox').textContent = '';
      addEntry('transcriptBox', final.trim(), 'transcript');
      enqueueTranslation(final.trim());
    }}
  }};

  recognition.onerror = (e) => {{
    if (e.error === 'not-allowed') {{
      document.getElementById('statusText').textContent = '❌ Mic access denied';
    }} else if (e.error !== 'no-speech') {{
      document.getElementById('statusText').textContent = 'Error: ' + e.error;
    }}
  }};

  recognition.onend = () => {{
    if (isListening) recognition.start();
  }};

  recognition.start();
}}

function stopListening() {{
  isListening = false;
  if (recognition) recognition.stop();
  document.getElementById('statusDot').classList.remove('active');
  document.getElementById('statusText').textContent = 'Stopped';
  document.getElementById('startBtn').disabled = false;
  document.getElementById('stopBtn').disabled = true;
  document.getElementById('interimBox').textContent = '—';
}}

function clearAll() {{
  document.getElementById('transcriptBox').innerHTML = '';
  document.getElementById('translationBox').innerHTML = '';
  document.getElementById('interimBox').textContent = isListening ? 'Listening...' : 'Waiting for speech...';
  document.getElementById('translationStatus').textContent = '—';
  translationQueue = [];
}}

function enqueueTranslation(text) {{
  if (!API_KEY || API_KEY.trim() === '') {{
    document.getElementById('translationStatus').textContent = '⚠ No API key';
    return;
  }}
  translationQueue.push(text);
  if (!isTranslating) processQueue();
}}

async function processQueue() {{
  if (translationQueue.length === 0) {{ isTranslating = false; return; }}
  isTranslating = true;
  const text = translationQueue.shift();

  document.getElementById('translationStatus').innerHTML =
    'Translating<span class="loading-dot">...</span>';

  try {{
    const resp = await fetch('https://api.anthropic.com/v1/messages', {{
      method: 'POST',
      headers: {{
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true'
      }},
      body: JSON.stringify({{
        model: 'claude-sonnet-4-20250514',
        max_tokens: 300,
        system: `You are a real-time translator. Translate the given text to ${{TARGET_LANG}}.
Return ONLY the translated text — no explanations, no punctuation changes beyond what is natural, no extra commentary.`,
        messages: [{{ role: 'user', content: text }}]
      }})
    }});

    const data = await resp.json();
    if (data.content && data.content[0]) {{
      const translated = data.content[0].text.trim();
      addEntry('translationBox', translated, 'translation');
      document.getElementById('translationStatus').textContent = '✓ Translated';
    }} else {{
      document.getElementById('translationStatus').textContent = '⚠ Translation failed';
    }}
  }} catch(err) {{
    document.getElementById('translationStatus').textContent = '⚠ ' + err.message;
  }}

  processQueue();
}}
</script>
</body>
</html>
"""

components.html(html_component, height=560, scrolling=False)

# ─── Footer Tips ─────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📖 Usage Tips"):
    st.markdown("""
**Getting Started**
1. Enter your **Anthropic API Key** in the sidebar
2. Select your **source language** (what you'll speak in)
3. Select your **target language** (what to translate to)
4. Click **▶ Start Listening** and allow microphone access
5. Speak clearly — translations appear automatically!

**Browser Compatibility**
- ✅ **Chrome** (Desktop & Android) — Best support
- ✅ **Edge** (Desktop) — Good support
- ⚠️ **Safari** (iOS) — Limited support
- ❌ **Firefox** — Not supported (no Web Speech API)

**Tips for Best Results**
- Speak in clear, complete sentences
- Minimize background noise
- Pause briefly between sentences
- Use a headset/earphones for better accuracy

**No API Key?**
You can still use the app for **live transcription only** — translation will be skipped.
    """)

st.markdown("""
<div style="text-align:center; font-family:'Space Mono',monospace; font-size:0.65rem; color:#2a2a40; margin-top:1rem;">
  LIVE AUDIO TRANSLATOR · POWERED BY CLAUDE AI + WEB SPEECH API
</div>
""", unsafe_allow_html=True)
