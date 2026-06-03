import streamlit as st
import re
import os

# ─────────────────────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LinkedIn Post Generator · AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS — Dark Glassmorphism Theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

/* ── Global Reset ─────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0a0e1a !important;
    color: #e2e8f0 !important;
}

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1526 50%, #0a0e1a 100%) !important;
    min-height: 100vh;
}

/* ── Streamlit chrome cleanup ────── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Hero Section ────────────────── */
.hero-wrapper {
    background: linear-gradient(135deg, #0a66c2 0%, #004182 40%, #1a237e 100%);
    padding: 3.5rem 2rem 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.hero-wrapper::before {
    content: "";
    position: absolute;
    top: -60%;
    left: 50%;
    transform: translateX(-50%);
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.18);
    color: rgba(255,255,255,0.9);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 0.3rem;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}
.hero-title span {
    background: linear-gradient(90deg, #7dd3fc, #a5f3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.75);
    max-width: 520px;
    width: 100%;
    margin: 0.3rem auto 0;
    line-height: 1.6;
    text-align: center;
    display: block;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin-top: 2rem;
}
.stat-item {
    text-align: center;
}
.stat-num {
    font-family: 'Sora', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #7dd3fc;
}
.stat-label {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.15rem;
}

/* ── Main Content ────────────────── */
.main-content {
    max-width: 1320px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem 4rem;
}

/* ── Glass Card ──────────────────── */
.glass-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(10,102,194,0.35);
}
.section-label {
    font-family: 'Sora', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #7dd3fc;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(125,211,252,0.15);
}

/* ── Streamlit widget overrides ───── */
.stTextInput > label,
.stTextArea > label,
.stSelectbox > label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 0.4rem !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #0a66c2 !important;
    box-shadow: 0 0 0 3px rgba(10,102,194,0.2) !important;
    background: rgba(10,102,194,0.06) !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}
.stSelectbox > div > div:hover {
    border-color: #0a66c2 !important;
}

/* ── Generate Button ─────────────── */
div[data-testid="stButton"]:has(button[key="gen_btn"]) > button,
.stButton > button[data-baseweb="button"] {
    display: none;
}
.gen-btn-wrapper {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0 0;
}

/* Override Streamlit button for the main one */
.stButton > button {
    background: linear-gradient(135deg, #0a66c2 0%, #0052a3 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2.5rem !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(10,102,194,0.35) !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1a76d2 0%, #0a66c2 100%) !important;
    box-shadow: 0 6px 28px rgba(10,102,194,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Tone Pill Selector (CSS only) ─ */
.tone-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.tone-pill {
    padding: 0.4rem 1rem;
    border-radius: 100px;
    border: 1.5px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.04);
    color: #94a3b8;
    font-size: 0.82rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
}
.tone-pill.active {
    border-color: #0a66c2;
    background: rgba(10,102,194,0.2);
    color: #7dd3fc;
    font-weight: 600;
}

/* ── LinkedIn Preview Card ─────────── */
.li-card {
    background: #1b2030;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    overflow: hidden;
    margin-top: 0.5rem;
}
.li-card-header {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 1.1rem 1.4rem 0.9rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.li-avatar {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0a66c2, #004182);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.li-name {
    font-weight: 700;
    font-size: 0.92rem;
    color: #e2e8f0;
}
.li-meta {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.1rem;
}
.li-logo {
    margin-left: auto;
    width: 28px;
    height: 28px;
}
.li-body {
    padding: 1.2rem 1.4rem;
    font-size: 0.93rem;
    line-height: 1.7;
    color: #cbd5e1;
    white-space: pre-wrap;
    max-height: 520px;
    overflow-y: auto;
}
.li-body::-webkit-scrollbar { width: 4px; }
.li-body::-webkit-scrollbar-track { background: transparent; }
.li-body::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }
.li-actions {
    padding: 0.8rem 1.4rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex;
    gap: 1.4rem;
}
.li-action {
    font-size: 0.78rem;
    color: #64748b;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

/* ── Character Counter ────────────── */
.char-bar-wrap {
    margin-top: 1rem;
    padding: 0.9rem 1.1rem;
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.06);
}
.char-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #64748b;
    margin-bottom: 0.45rem;
}
.char-bar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
}
.char-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.4s ease;
}

/* ── Success / Error boxes ───────── */
.success-box {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    color: #6ee7b7;
    font-size: 0.88rem;
    margin-top: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

/* ── Spinner override ─────────────── */
.stSpinner > div { border-top-color: #0a66c2 !important; }

/* ── Copy snippet ─────────────────── */
.stCodeBlock { 
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}

/* ── Tip box ─────────────────────── */
.tip-box {
    display: flex;
    gap: 0.7rem;
    background: rgba(10,102,194,0.08);
    border: 1px solid rgba(10,102,194,0.2);
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    font-size: 0.82rem;
    color: #7dd3fc;
    margin-top: 1.2rem;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline helpers
# ─────────────────────────────────────────────────────────────────────────────
def save_post(post: str, topic: str) -> str:
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', topic.strip())
    filename = f"LINKDIN_POST_{safe_name}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post)
    return filename


def run_pipeline(inputs: dict) -> str:
    from config import get_model
    from prompt_builder import generate_post
    model = get_model()
    post = generate_post(model, inputs)
    return post


# ─────────────────────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <h1 class="hero-title">LinkedIn Post <span>Generator</span></h1>
    <p class="hero-sub">Craft compelling, viral-ready LinkedIn posts in seconds — tailored to your voice, audience, and goals.</p>
    <div class="hero-stats">
        <div class="stat-item">
            <div class="stat-num">6</div>
            <div class="stat-label">Tone Styles</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">6</div>
            <div class="stat-label">Frameworks</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">3</div>
            <div class="stat-label">Post Lengths</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Layout — 2 columns
# ─────────────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

# ════════════════════════════════════════════════════════════════
# LEFT — Input Form
# ════════════════════════════════════════════════════════════════
with left_col:

    # ── Topic ────────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📝 Post Details</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "Topic *",
        placeholder="e.g. Why every developer should learn system design",
        key="topic_input",
    )

    audience = st.text_input(
        "Target Audience *",
        placeholder="e.g. Software engineers, startup founders, HR managers",
        key="audience_input",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Tone & Length ─────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🎨 Style & Format</div>', unsafe_allow_html=True)

    TONES = ["Professional", "Inspirational", "Humorous", "Funny", "Angry", "Sad"]
    tone = st.selectbox("Tone", TONES, key="tone_sel")

    LENGTHS = [
        "Short (100–150 words)",
        "Medium (200–300 words)",
        "Long (400–500 words)",
    ]
    length = st.selectbox("Post Length", LENGTHS, key="len_sel")

    FRAMEWORKS = [
        "AIDA (Attention, Interest, Desire, Action)",
        "PAS (Problem, Agitate, Solution)",
        "Storytelling",
        "Listicle",
        "How-to / Tips",
        "None",
    ]
    framework = st.selectbox("Copywriting Framework", FRAMEWORKS, key="fw_sel")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Extra context ──────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💡 Extra Context (Optional)</div>', unsafe_allow_html=True)

    extra = st.text_area(
        "Additional Notes",
        placeholder="Specific data points, personal story, CTA to include…",
        height=100,
        key="extra_input",
    )

    st.markdown("""
    <div class="tip-box">
        💡 <span>The more context you give, the more personalised your post will be. Try adding a personal story or a surprising stat!</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Generate Button ────────────────────────────────────
    generate_clicked = st.button("✨ Generate LinkedIn Post", key="gen_btn", use_container_width=True)


# ════════════════════════════════════════════════════════════════
# Generate Logic
# ════════════════════════════════════════════════════════════════
if generate_clicked:
    if not topic.strip():
        st.warning("⚠️  Please enter a **topic** before generating.")
    elif not audience.strip():
        st.warning("⚠️  Please enter a **target audience** before generating.")
    else:
        inputs = {
            "topic":     topic.strip(),
            "tone":      tone,
            "audience":  audience.strip(),
            "length":    length,
            "framework": framework,
            "extra":     extra.strip(),
        }
        with st.spinner("🤖 Gemini is crafting your post…"):
            try:
                post = run_pipeline(inputs)
                st.session_state["post"]   = post
                st.session_state["topic"]  = topic.strip()
                st.session_state["inputs"] = inputs
            except Exception as e:
                st.error(f"❌ Generation failed: {e}")


# ════════════════════════════════════════════════════════════════
# RIGHT — Live Preview + Output
# ════════════════════════════════════════════════════════════════
with right_col:

    # ── LinkedIn Preview ───────────────────────────────────
    st.markdown('<div class="glass-card" style="padding:1.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">👁️ LinkedIn Preview</div>', unsafe_allow_html=True)

    if "post" in st.session_state:
        post_text = st.session_state["post"]
        char_count = len(post_text)
        li_optimal = 3000
        fill_pct = min(100, int((char_count / li_optimal) * 100))

        # Colour the bar
        if fill_pct < 60:
            bar_color = "#0a66c2"
        elif fill_pct < 90:
            bar_color = "#10b981"
        else:
            bar_color = "#f59e0b"

        st.markdown(f"""
        <div class="li-card">
            <div class="li-card-header">
                <div class="li-avatar">👤</div>
                <div>
                    <div class="li-name">Your Name · <span style="color:#64748b;font-weight:400">You</span></div>
                    <div class="li-meta">Just now · 🌐</div>
                </div>
                <svg class="li-logo" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="34" height="34" rx="6" fill="#0a66c2"/>
                    <path d="M8 13h4v13H8zM10 11.5a2 2 0 1 1 0-4 2 2 0 0 1 0 4zM15 13h4v2s1-2 4-2c3.5 0 5 2.2 5 6v7h-4v-6.5c0-1.5-.5-2.5-2-2.5s-3 1-3 3V26h-4V13z" fill="white"/>
                </svg>
            </div>
            <div class="li-body">{post_text}</div>
            <div class="li-actions">
                <span class="li-action">👍 Like</span>
                <span class="li-action">💬 Comment</span>
                <span class="li-action">🔁 Repost</span>
                <span class="li-action">📤 Send</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Character bar
        st.markdown(f"""
        <div class="char-bar-wrap">
            <div class="char-bar-label">
                <span>Character count</span>
                <span style="color:#e2e8f0;font-weight:600">{char_count:,} / {li_optimal:,}</span>
            </div>
            <div class="char-bar-bg">
                <div class="char-bar-fill" style="width:{fill_pct}%;background:{bar_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Placeholder state
        st.markdown("""
        <div class="li-card">
            <div class="li-card-header">
                <div class="li-avatar">👤</div>
                <div>
                    <div class="li-name">Your Name</div>
                    <div class="li-meta">Your Post will appear here</div>
                </div>
                <svg class="li-logo" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="34" height="34" rx="6" fill="#0a66c2"/>
                    <path d="M8 13h4v13H8zM10 11.5a2 2 0 1 1 0-4 2 2 0 0 1 0 4zM15 13h4v2s1-2 4-2c3.5 0 5 2.2 5 6v7h-4v-6.5c0-1.5-.5-2.5-2-2.5s-3 1-3 3V26h-4V13z" fill="white"/>
                </svg>
            </div>
            <div class="li-body" style="color:#475569;font-style:italic;text-align:center;padding:3rem 1.4rem;">
                ✨ Fill in the form on the left and click<br>
                <strong style="color:#0a66c2;">Generate LinkedIn Post</strong><br>
                to see your post previewed here.
            </div>
            <div class="li-actions">
                <span class="li-action">👍 Like</span>
                <span class="li-action">💬 Comment</span>
                <span class="li-action">🔁 Repost</span>
                <span class="li-action">📤 Send</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Actions ────────────────────────────────────────────
    if "post" in st.session_state:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">⚡ Actions</div>', unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            # Copy via code block
            st.code(st.session_state["post"], language=None)

        with col_b:
            if st.button("💾 Save to File", key="save_btn", use_container_width=True):
                try:
                    fname = save_post(st.session_state["post"], st.session_state["topic"])
                    st.markdown(
                        f'<div class="success-box">✅ Saved as <strong>{fname}</strong></div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"Could not save: {e}")

        with col_c:
            safe_topic = re.sub(r'[^a-zA-Z0-9_]', '_', st.session_state.get("topic", "post"))
            st.download_button(
                label="⬇️ Download .txt",
                data=st.session_state["post"],
                file_name=f"LINKDIN_POST_{safe_topic}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_btn",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Regenerate Post", key="regen_btn", use_container_width=True):
            with st.spinner("Regenerating…"):
                try:
                    new_post = run_pipeline(st.session_state["inputs"])
                    st.session_state["post"] = new_post
                    st.rerun()
                except Exception as e:
                    st.error(f"Regeneration failed: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-content
