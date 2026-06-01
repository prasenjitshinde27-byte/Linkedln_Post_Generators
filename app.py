import streamlit as st
import re
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Sora', sans-serif;
    }

    /* Header banner */
    .hero {
        background: linear-gradient(135deg, #0a66c2 0%, #004182 100%);
        border-radius: 16px;
        padding: 2.2rem 2rem 1.8rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .hero h1 { font-size: 2rem; margin: 0 0 0.3rem; color: white; }
    .hero p  { opacity: 0.85; margin: 0; font-size: 0.95rem; }

    /* Cards */
    .card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
    }
    .card-title {
        font-family: 'Sora', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #0a66c2;
        margin-bottom: 0.8rem;
    }

    /* Output box */
    .post-output {
        background: #ffffff;
        border: 2px solid #0a66c2;
        border-radius: 12px;
        padding: 1.6rem;
        white-space: pre-wrap;
        font-size: 0.97rem;
        line-height: 1.7;
        color: #1e293b;
    }

    /* Buttons */
    .stButton > button {
        background: #0a66c2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.6rem;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton > button:hover { background: #004182; color: white; }

    /* File saved notice */
    .save-notice {
        background: #ecfdf5;
        border: 1px solid #6ee7b7;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        color: #065f46;
        font-size: 0.9rem;
        margin-top: 0.8rem;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer { visibility: hidden; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def save_post(post: str, topic: str) -> str:
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', topic.strip())
    filename = f"LINKEDIN_POST_{safe_name}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post)
    return filename


def run_pipeline(inputs: dict):
    """Import and run the actual generation pipeline."""
    from config import get_model
    from prompt_builder import generate_post

    model = get_model()
    post = generate_post(model, inputs)
    return post


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>💼 LinkedIn Post Generator</h1>
    <p>Fill in the details below and let AI craft your next viral post.</p>
</div>
""", unsafe_allow_html=True)


# ── Input Form ────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">📝 Post Details</div>', unsafe_allow_html=True)

topic = st.text_input(
    "Topic",
    placeholder="e.g. Why every developer should learn system design",
)

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox(
        "Tone",
        ["Professional", "Conversational", "Inspirational", "Educational", "Storytelling"],
    )
with col2:
    length = st.selectbox(
        "Post Length",
        ["Short (≤150 words)", "Medium (150–300 words)", "Long (300+ words)"],
    )

framework = st.selectbox(
    "Post Framework",
    [
        "Hook → Story → CTA",
        "Problem → Agitate → Solution",
        "Listicle (numbered tips)",
        "Before → After → Bridge",
        "Lessons Learned",
        "Contrarian / Hot Take",
        "Personal Story",
        "No specific framework",
    ],
)

audience = st.text_input(
    "Target Audience",
    placeholder="e.g. Software engineers, startup founders, HR professionals",
)

keywords = st.text_input(
    "Keywords / Hashtags (optional)",
    placeholder="e.g. #AI #Leadership productivity",
)

extra = st.text_area(
    "Additional Context (optional)",
    placeholder="Any specific points, stories, or data you want included…",
    height=100,
)

st.markdown('</div>', unsafe_allow_html=True)


# ── Generate ──────────────────────────────────────────────────────────────────
generate_clicked = st.button("✨ Generate Post")

if generate_clicked:
    if not topic.strip():
        st.warning("Please enter a topic before generating.")
    else:
        inputs = {
            "topic":    topic.strip(),
            "tone":      tone,
            "length":    length,
            "framework": framework,
            "audience":  audience.strip(),
            "keywords": keywords.strip(),
            "extra":    extra.strip(),
        }

        with st.spinner("Crafting your LinkedIn post…"):
            try:
                post = run_pipeline(inputs)
                st.session_state["post"]   = post
                st.session_state["topic"]  = topic.strip()
                st.session_state["inputs"] = inputs
            except Exception as e:
                st.error(f"Generation failed: {e}")


# ── Output ────────────────────────────────────────────────────────────────────
if "post" in st.session_state:
    st.markdown("---")
    st.markdown('<div class="card-title" style="color:#0a66c2;font-family:Sora,sans-serif;font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">📄 Generated Post</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="post-output">{st.session_state["post"]}</div>',
        unsafe_allow_html=True,
    )

    col_copy, col_save, col_dl = st.columns(3)

    with col_copy:
        st.code(st.session_state["post"], language=None)   # lets user copy easily

    with col_save:
        if st.button("💾 Save to File"):
            try:
                fname = save_post(st.session_state["post"], st.session_state["topic"])
                st.markdown(
                    f'<div class="save-notice">✅ Saved as <strong>{fname}</strong></div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Could not save file: {e}")

    with col_dl:
        st.download_button(
            label="⬇️ Download .txt",
            data=st.session_state["post"],
            file_name=f"LINKEDIN_POST_{re.sub(r'[^a-zA-Z0-9_]', '_', st.session_state['topic'])}.txt",
            mime="text/plain",
        )

    # Regenerate
    if st.button("🔄 Regenerate"):
        with st.spinner("Regenerating…"):
            try:
                new_post = run_pipeline(st.session_state["inputs"])
                st.session_state["post"] = new_post
                st.rerun()
            except Exception as e:
                st.error(f"Regeneration failed: {e}")