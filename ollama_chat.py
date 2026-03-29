import streamlit as st
import requests
import json

# ── Page config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="LLaMA Chat",
    page_icon="🦙",
    layout="centered",
)

# ── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

/* ── Root theme ── */
:root {
    --bg:        #0d0f12;
    --surface:   #161a20;
    --border:    #2a2f3a;
    --accent:    #e87c3e;
    --accent2:   #f5a461;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --user-bg:   #1e2330;
    --bot-bg:    #13171e;
    --radius:    12px;
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--text);
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* ── Main container ── */
[data-testid="stMainBlockContainer"] {
    max-width: 780px;
    padding: 0 1.5rem 6rem;
}

/* ── Title bar ── */
.title-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1.6rem 0 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.6rem;
}
.title-bar .icon {
    font-size: 2rem;
    line-height: 1;
}
.title-bar h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text);
    margin: 0;
    letter-spacing: -0.5px;
}
.title-bar .badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: var(--accent);
    background: rgba(232,124,62,0.12);
    border: 1px solid rgba(232,124,62,0.3);
    border-radius: 4px;
    padding: 2px 7px;
    margin-left: auto;
}

/* ── Chat messages ── */
.msg-wrap {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 1.2rem;
}
.msg-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    padding: 0 4px;
}
.msg-label.user { color: var(--accent2); }
.msg-bubble {
    padding: 0.85rem 1.1rem;
    border-radius: var(--radius);
    font-size: 0.93rem;
    line-height: 1.65;
    border: 1px solid var(--border);
    white-space: pre-wrap;
    word-break: break-word;
}
.msg-bubble.user {
    background: var(--user-bg);
    border-color: rgba(232,124,62,0.2);
}
.msg-bubble.assistant {
    background: var(--bot-bg);
}

/* ── Typing indicator ── */
.typing {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 0.7rem 1.1rem;
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    width: fit-content;
}
.typing span {
    width: 7px; height: 7px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
    animation: bounce 1.2s infinite ease-in-out;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40%            { transform: translateY(-6px); opacity: 1; }
}

/* ── Input area ── */
[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.93rem !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

.stSlider > div > div > div { background: var(--accent) !important; }

/* ── Buttons ── */
.stButton button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    border-radius: 6px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Metrics ── */
.stat-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1.4rem;
    flex-wrap: wrap;
}
.stat-box {
    flex: 1;
    min-width: 100px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
}
.stat-box .s-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--muted);
}
.stat-box .s-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent2);
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ─────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434"

def check_ollama() -> bool:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def list_models() -> list[str]:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return ["llama3.2:1b"]

def stream_response(messages: list, model: str, temperature: float, max_tokens: int):
    """Yield text chunks from Ollama streaming API."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    with requests.post(f"{OLLAMA_URL}/api/chat", json=payload, stream=True, timeout=120) as resp:
        for line in resp.iter_lines():
            if line:
                chunk = json.loads(line)
                delta = chunk.get("message", {}).get("content", "")
                if delta:
                    yield delta
                if chunk.get("done"):
                    break

# ── Session state ────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    online = check_ollama()
    status_color = "#4ade80" if online else "#f87171"
    status_text  = "Connected" if online else "Offline"
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:1rem">'
        f'<div style="width:8px;height:8px;border-radius:50%;background:{status_color}"></div>'
        f'<span style="font-size:0.8rem;color:{status_color}">{status_text}</span></div>',
        unsafe_allow_html=True,
    )

    models = list_models() if online else ["llama3.2:1b"]
    model = st.selectbox("Model", models, index=0)

    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05,
                            help="Higher = more creative, lower = more precise")
    max_tokens  = st.slider("Max tokens", 64, 2048, 512, 64)

    st.markdown("---")
    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful, concise, and friendly AI assistant.",
        height=100,
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑 Clear chat"):
            st.session_state.messages = []
            st.session_state.total_tokens = 0
            st.rerun()
    with col2:
        msg_count = len(st.session_state.messages)
        st.markdown(
            f'<div style="font-size:0.75rem;color:#6b7280;padding-top:6px">'
            f'{msg_count} message{"s" if msg_count != 1 else ""}</div>',
            unsafe_allow_html=True,
        )

# ── Title ────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="title-bar">
        <div class="icon">🦙</div>
        <h1>LLaMA Chat</h1>
        <div class="badge">{model}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Offline warning ──────────────────────────────────────────────
if not online:
    st.error("⚠️ Ollama is not running. Start it with `ollama serve` in your terminal.")

# ── Render history ───────────────────────────────────────────────
for msg in st.session_state.messages:
    role   = msg["role"]
    label  = "YOU" if role == "user" else "LLAMA"
    cls    = "user" if role == "user" else "assistant"
    st.markdown(
        f"""
        <div class="msg-wrap">
            <div class="msg-label {cls}">{label}</div>
            <div class="msg-bubble {cls}">{msg["content"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Chat input ───────────────────────────────────────────────────
if prompt := st.chat_input("Message LLaMA…", disabled=not online):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f"""
        <div class="msg-wrap">
            <div class="msg-label user">YOU</div>
            <div class="msg-bubble user">{prompt}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Build API messages (include system prompt)
    api_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Stream response
    st.markdown('<div class="msg-wrap"><div class="msg-label">LLAMA</div>', unsafe_allow_html=True)
    response_placeholder = st.empty()
    full_response = ""

    try:
        for chunk in stream_response(api_messages, model, temperature, max_tokens):
            full_response += chunk
            response_placeholder.markdown(
                f'<div class="msg-bubble assistant">{full_response}▌</div>',
                unsafe_allow_html=True,
            )

        # Final render without cursor
        response_placeholder.markdown(
            f'<div class="msg-bubble assistant">{full_response}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Rough token estimate (~4 chars per token)
        st.session_state.total_tokens += len(full_response) // 4
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        response_placeholder.error(f"Error: {e}")
