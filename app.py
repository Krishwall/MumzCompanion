import streamlit as st
import uuid
from agent.agent import run_agent

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MumzCompanion",
    page_icon="🤱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "chat" not in st.session_state:
    st.session_state.chat = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding-top: 1rem !important;
    max-width: 800px;
}
/* hide default streamlit header/footer */
#MainMenu, footer, header {visibility: hidden;}

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, #F9A8D4 0%, #F472B6 40%, #EC4899 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; right: -30%;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 0.95rem;
    opacity: 0.9;
    margin: 0;
    font-weight: 300;
}

/* ── Stage Badge ── */
.stage-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
    border: 1px solid #F9A8D4;
    border-radius: 50px;
    padding: 8px 18px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #BE185D;
    margin-bottom: 1rem;
}

/* ── Stage Progress ── */
.progress-container {
    background: #FDF2F8;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #FCE7F3;
}
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #9CA3AF;
    margin-bottom: 6px;
    font-weight: 500;
}
.progress-bar-bg {
    background: #F3E8FF;
    border-radius: 100px;
    height: 10px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #F9A8D4, #EC4899, #DB2777);
    transition: width 0.5s ease;
}
.progress-stage-name {
    text-align: center;
    font-size: 0.9rem;
    font-weight: 600;
    color: #BE185D;
    margin-top: 8px;
}

/* ── Insight Card ── */
.insight-card {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-left: 4px solid #F59E0B;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
}
.insight-card h3 {
    margin: 0 0 0.4rem 0;
    font-size: 1rem;
    font-weight: 600;
    color: #92400E;
}
.insight-card p {
    margin: 0;
    font-size: 0.9rem;
    color: #78350F;
    line-height: 1.5;
}
.heads-up {
    background: #FFF7ED;
    border: 1px solid #FDBA74;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.82rem;
    color: #C2410C;
}

/* ── Product Cards ── */
.product-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
}
.product-card {
    background: #FFFFFF;
    border: 1px solid #F3F4F6;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.product-card:hover {
    border-color: #F9A8D4;
    box-shadow: 0 4px 12px rgba(236, 72, 153, 0.1);
    transform: translateY(-1px);
}
.product-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
}
.product-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #1F2937;
    margin: 0;
}
.product-price {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    color: #065F46;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 4px 12px;
    border-radius: 50px;
    white-space: nowrap;
}
.product-reason {
    font-size: 0.82rem;
    color: #6B7280;
    margin: 0 0 0.6rem 0;
    font-style: italic;
}
.confidence-row {
    display: flex;
    align-items: center;
    gap: 8px;
}
.confidence-label {
    font-size: 0.72rem;
    color: #9CA3AF;
    font-weight: 500;
    min-width: 50px;
}
.confidence-bar-bg {
    flex: 1;
    background: #F3F4F6;
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
}
.confidence-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #34D399, #10B981);
}
.confidence-value {
    font-size: 0.72rem;
    color: #6B7280;
    font-weight: 600;
    min-width: 32px;
    text-align: right;
}

/* ── Chat Bubbles ── */
.chat-container {
    margin-bottom: 1rem;
}
.chat-bubble {
    padding: 0.7rem 1rem;
    border-radius: 14px;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    line-height: 1.5;
    max-width: 85%;
}
.chat-user {
    background: linear-gradient(135deg, #EDE9FE, #DDD6FE);
    color: #5B21B6;
    margin-left: auto;
    border-bottom-right-radius: 4px;
    text-align: right;
}
.chat-assistant {
    background: #F3F4F6;
    color: #374151;
    margin-right: auto;
    border-bottom-left-radius: 4px;
}

/* ── Refusal Card ── */
.refusal-card {
    background: linear-gradient(135deg, #FEF2F2, #FEE2E2);
    border-left: 4px solid #EF4444;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.refusal-card h3 {
    margin: 0 0 0.3rem 0;
    color: #991B1B;
    font-size: 1rem;
}
.refusal-card p {
    margin: 0;
    color: #7F1D1D;
    font-size: 0.9rem;
}

/* ── Disclaimer ── */
.disclaimer-bar {
    background: #F0F9FF;
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-size: 0.8rem;
    color: #0369A1;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Follow-up ── */
.followup {
    background: #F9FAFB;
    border: 1px dashed #D1D5DB;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #6B7280;
    text-align: center;
    margin-top: 0.5rem;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 1.5px solid #E5E7EB !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #F472B6 !important;
    box-shadow: 0 0 0 2px rgba(244,114,182,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #EC4899, #DB2777) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #DB2777, #BE185D) !important;
    box-shadow: 0 4px 12px rgba(219, 39, 119, 0.3) !important;
    transform: translateY(-1px) !important;
}
.stDateInput > div > div > input {
    border-radius: 12px !important;
}

/* ── No products ── */
.no-products {
    text-align: center;
    padding: 2rem;
    color: #9CA3AF;
    font-size: 0.9rem;
}
.no-products .emoji {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STAGE DISPLAY HELPERS
# ─────────────────────────────────────────────
STAGE_META = {
    "early_pregnancy": {"label": "Early Pregnancy", "emoji": "🌱", "order": 1, "max_unit": 13},
    "mid_pregnancy":   {"label": "Mid Pregnancy",   "emoji": "🌸", "order": 2, "max_unit": 27},
    "late_pregnancy":  {"label": "Late Pregnancy",  "emoji": "🤰", "order": 3, "max_unit": 40},
    "newborn":         {"label": "Newborn",          "emoji": "👶", "order": 4, "max_unit": 2},
    "infant":          {"label": "Infant",           "emoji": "🍼", "order": 5, "max_unit": 6},
    "older_infant":    {"label": "Older Infant",     "emoji": "🧒", "order": 6, "max_unit": 12},
    "unknown":         {"label": "Unknown",          "emoji": "❓", "order": 0, "max_unit": 1},
}

def get_progress_pct(stage, exact_time):
    """Return 0-100 for the overall journey progress."""
    meta = STAGE_META.get(stage, STAGE_META["unknown"])
    # Each stage is ~16.6% of the journey (6 stages)
    base = (meta["order"] - 1) * 16.67
    within = min(exact_time / meta["max_unit"], 1.0) * 16.67 if meta["max_unit"] else 0
    return min(round(base + within, 1), 100)

def render_confidence_color(conf):
    if conf >= 0.8:
        return "#10B981"
    elif conf >= 0.6:
        return "#F59E0B"
    return "#EF4444"

# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🤱 MumzCompanion</h1>
    <p>Your week-by-week pregnancy &amp; pediatric product guide — personalized to your stage.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
if st.session_state.chat:
    chat_html = '<div class="chat-container">'
    for role, msg in st.session_state.chat[-6:]:  # show last 6 messages
        cls = "chat-user" if role == "user" else "chat-assistant"
        icon = "👤" if role == "user" else "🤱"
        chat_html += f'<div class="chat-bubble {cls}">{icon} {msg}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT AREA
# ─────────────────────────────────────────────
col_date, col_query = st.columns([1, 2])
with col_date:
    due_date = st.text_input(
        "📅 Due / Birth Date",
        value="2026-06-01",
        placeholder="YYYY-MM-DD"
    )
with col_query:
    query = st.text_input(
        "💬 What do you need?",
        value="",
        placeholder="e.g. I need a maternity pillow, stroller under 200 AED..."
    )

run_btn = st.button("✨ Get Recommendations")

# ─────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────
if run_btn and query.strip():
    with st.spinner("🤱 Finding the best for you..."):
        result = run_agent(query, due_date, user_id=st.session_state.user_id)

    # Save to chat history
    st.session_state.chat.append(("user", query))
    st.session_state.chat.append((
        "assistant",
        result.follow_up_prompt or result.timeline_insight.headline
    ))
    st.session_state.last_result = result

result = st.session_state.last_result

if result:
    # ── RTL support for Arabic ──
    if result.input_language == "ar":
        st.markdown('<style>body{direction:rtl;text-align:right;}</style>', unsafe_allow_html=True)

    # ── Stage Progress Bar ──
    meta = STAGE_META.get(result.stage_bucket, STAGE_META["unknown"])
    pct = get_progress_pct(result.stage_bucket, result.timeline_insight.exact_week_or_month)
    unit_label = "Week" if "pregnancy" in result.stage_bucket else "Month"
    unit_val = result.timeline_insight.exact_week_or_month

    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-label">
            <span>🌱 Early Pregnancy</span>
            <span>🧒 12 Months</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {pct}%;"></div>
        </div>
        <div class="progress-stage-name">{meta['emoji']} {meta['label']} — {unit_label} {unit_val}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Refused ──
    if result.refused:
        st.markdown(f"""
        <div class="refusal-card">
            <h3>⚠️ Safety First</h3>
            <p>{result.refusal_reason}</p>
        </div>
        """, unsafe_allow_html=True)
        if result.disclaimer:
            st.markdown(f"""
            <div class="disclaimer-bar">🩺 {result.disclaimer}</div>
            """, unsafe_allow_html=True)
    else:
        # ── Disclaimer (mild medical) ──
        if result.disclaimer:
            st.markdown(f"""
            <div class="disclaimer-bar">💡 {result.disclaimer}</div>
            """, unsafe_allow_html=True)

        # ── Timeline Insight ──
        heads_up_html = ""
        if result.timeline_insight.heads_up:
            heads_up_html = f'<div class="heads-up">🔔 {result.timeline_insight.heads_up}</div>'

        st.markdown(f"""
        <div class="insight-card">
            <h3>📖 {result.timeline_insight.headline}</h3>
            <p>{result.timeline_insight.body}</p>
            {heads_up_html}
        </div>
        """, unsafe_allow_html=True)

        # ── Product Cards ──
        st.markdown("#### 🛍️ Recommended for You")

        if not result.products:
            st.markdown("""
            <div class="no-products">
                <div class="emoji">🔍</div>
                No specific products found for this query. Try a different search!
            </div>
            """, unsafe_allow_html=True)
        else:
            for p in result.products:
                conf_pct = int(p.confidence * 100)
                conf_color = render_confidence_color(p.confidence)
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-header">
                        <p class="product-name">{p.name}</p>
                        <span class="product-price">AED {p.price_aed:.0f}</span>
                    </div>
                    <p class="product-reason">✦ {p.relevance_reason}</p>
                    <div class="confidence-row">
                        <span class="confidence-label">Match</span>
                        <div class="confidence-bar-bg">
                            <div class="confidence-bar-fill" style="width:{conf_pct}%; background: linear-gradient(90deg, {conf_color}88, {conf_color});"></div>
                        </div>
                        <span class="confidence-value">{conf_pct}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ── Follow-up ──
        if result.follow_up_prompt:
            st.markdown(f"""
            <div class="followup">💬 {result.follow_up_prompt}</div>
            """, unsafe_allow_html=True)

elif run_btn and not query.strip():
    st.warning("Please type a question first!")