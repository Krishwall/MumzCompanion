import streamlit as st
from agent.agent import run_agent

st.set_page_config(page_title="MumzCompanion 🤰", page_icon="🤰", layout="centered")

st.title("MumzCompanion 🤰")
st.markdown("Your week-by-week pregnancy and pediatric timeline guide.")

date_col, input_col = st.columns([1, 2])
with date_col:
    due_date = st.text_input("Due Date / Birth Date (YYYY-MM-DD)", "2026-06-01")
with input_col:
    query = st.text_input("How can I help you?", "I need a maternity pillow")

if st.button("Run"):
    with st.spinner("Thinking..."):
        result = run_agent(query, due_date)

    if result.input_language == "ar":
        st.markdown('<style>body { direction: rtl; text-align: right; }</style>', unsafe_allow_html=True)
        st.markdown(f"**المرحلة:** {result.stage_bucket} | **الأسبوع/الشهر:** {result.timeline_insight.exact_week_or_month}")
    else:
        st.markdown(f"**Stage:** {result.stage_bucket.replace('_', ' ').title()} | **Week/Month:** {result.timeline_insight.exact_week_or_month}")

    if result.refused:
        st.error(result.refusal_reason)
        if result.disclaimer:
            st.warning(result.disclaimer)
    else:
        st.info(f"### {result.timeline_insight.headline}\n{result.timeline_insight.body}")
        if result.timeline_insight.heads_up:
            st.warning(f"**Heads Up:** {result.timeline_insight.heads_up}")

        st.subheader("Recommended for You")
        if not result.products:
            st.write("No specific products found for this query/stage.")
        
        for p in result.products:
            with st.container():
                st.markdown(f"**{p.name}**")
                st.markdown(f"Price: AED {p.price_aed} | Confidence: {p.confidence}")
                st.markdown(f"*{p.relevance_reason}*")
                st.divider()
        
        if result.follow_up_prompt:
            st.caption(result.follow_up_prompt)