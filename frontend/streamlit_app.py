import streamlit as st
from backend import query

st.set_page_config(page_title="Recruiter Assistant", page_icon="🧠")

st.title("🤖 Ask About the Candidate")

st.markdown(
    """
    This assistant helps recruiters find relevant information about the candidate using natural language.
    """
)

# Input
user_question = st.text_input("Ask a question (e.g. 'What are your main skills?')")

if user_question:
    with st.spinner("Searching..."):
        docs = query.query_cortex(user_question)
        answer = query.generate_answer(user_question, docs)

    st.subheader("📌 Answer")
    st.success(answer)

    with st.expander("📄 Retrieved context"):
        for i, doc in enumerate(docs, 1):
            st.markdown(f"**Document {i}:**\n{doc}\n---")
