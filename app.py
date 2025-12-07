import streamlit as st
import os
from rag_chatbot import ask   # Import your ask() function from existing RAG code

st.set_page_config(page_title="RAG Chatbot", page_icon="📚")

st.title(" Multi-Query RAG Chatbot")
st.write("Ask questions based on the knowledge.")

# Input box
user_input = st.text_input("Ask a question:", "")

# When user clicks button
if st.button("Submit"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        answer, citations = ask(user_input, return_data=True)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Citations")
        if len(citations) == 0:
            st.write("No relevant sources found.")
        else:
            for src, pg in citations:
                st.write(f"- **{src}**, page {pg}")
