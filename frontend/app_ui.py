import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib
import io

st.set_page_config(page_title="CSV Analyst AI", page_icon="📊", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 760px; }

[data-testid="stFileUploader"] {
    border: 1.5px dashed #d1d5db;
    border-radius: 10px;
    padding: 0.25rem;
}

.stButton > button {
    background: #111827 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.45rem 1.4rem !important;
    font-size: 0.88rem !important;
}
.stButton > button:hover { background: #374151 !important; }

.user-bubble {
    background: #f3f4f6;
    border-radius: 12px 12px 4px 12px;
    padding: 0.65rem 0.9rem;
    margin: 0.3rem 0 0.3rem 3rem;
    font-size: 0.88rem;
    color: #111827;
}
.ai-bubble {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px 12px 12px 4px;
    padding: 0.65rem 0.9rem;
    margin: 0.3rem 3rem 0.3rem 0;
    font-size: 0.88rem;
    color: #111827;
    white-space: pre-wrap;
}
.msg-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.1rem;
}
.section-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin: 1.4rem 0 0.5rem;
}
hr { border-color: #f3f4f6 !important; margin: 1.2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

matplotlib.rcParams.update({
    "figure.facecolor": "#ffffff",
    "axes.facecolor":   "#ffffff",
    "text.color":       "#111827",
    "font.family":      "sans-serif",
})
COLORS = ["#6366f1", "#f59e0b", "#10b981", "#ef4444", "#3b82f6", "#ec4899", "#14b8a6", "#f97316"]

for k, v in {"session_id": None, "df": None, "chat_history": [], "api_base": "http://localhost:8000"}.items():
    if k not in st.session_state:
        st.session_state[k] = v


def upload_csv(file_bytes, filename):
    r = requests.post(f"{st.session_state.api_base}/Upload",
                      files={"file": (filename, file_bytes, "text/csv")}, timeout=30)
    r.raise_for_status()
    return r.json()


def stream_chat(session_id, message):
    with requests.post(f"{st.session_state.api_base}/chat",
                       json={"session_id": session_id, "message": message},
                       stream=True, timeout=60) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode("utf-8", errors="ignore")


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("### 📊 CSV Analyst AI")
st.caption("Upload a CSV, explore a pie chart, then chat with your data.")
st.markdown("---")

# ── Upload ────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

if uploaded:
    c1, c2 = st.columns([3, 1])
    with c1:
        st.caption(f"📄 **{uploaded.name}**")
    with c2:
        if st.button("Analyse →"):
            with st.spinner("Processing…"):
                try:
                    data = uploaded.read()
                    result = upload_csv(data, uploaded.name)
                    st.session_state.session_id = result["session_id"]
                    st.session_state.df = pd.read_csv(io.BytesIO(data))
                    st.session_state.chat_history = []
                    st.success("Ready!")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── Pie chart ─────────────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    all_cols = df.columns.tolist()
    col_options = cat_cols if cat_cols else all_cols

    st.markdown('<div class="section-title">Pie Chart</div>', unsafe_allow_html=True)

    ca, cb = st.columns([2, 1])
    with ca:
        col = st.selectbox("Column", col_options, label_visibility="collapsed")
    with cb:
        top_n = st.selectbox("Top slices", [5, 7, 10], label_visibility="collapsed")

    counts = df[col].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(5, 4.2))
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index.astype(str),
        autopct="%1.1f%%",
        colors=COLORS[:len(counts)],
        startangle=90,
        wedgeprops=dict(edgecolor="#fff", linewidth=1.5),
        pctdistance=0.82,
    )
    for t in texts:
        t.set_fontsize(9)
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("#fff")
        at.set_fontweight("600")
    ax.set_title(col, fontsize=11, fontweight="600", pad=12)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("---")

    # ── Chat ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Chat with your data</div>', unsafe_allow_html=True)

    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="msg-label">You</div>'
                    f'<div class="user-bubble">{msg["content"]}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="msg-label">AI</div>'
                    f'<div class="ai-bubble">{msg["content"]}</div>',
                    unsafe_allow_html=True)
    else:
        st.caption("e.g. *What are the top categories?* · *Summarise this data.*")

    prompt = st.chat_input("Ask about your data…")
    if prompt:
        if not st.session_state.session_id:
            st.warning("Upload a CSV first.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.spinner(""):
                full = ""
                try:
                    for chunk in stream_chat(st.session_state.session_id, prompt):
                        full += chunk
                except Exception as e:
                    full = f"Error: {e}"
            st.session_state.chat_history.append({"role": "assistant", "content": full})
            st.rerun()