import streamlit as st
from agent import ask_agent
import re

def clean_markdown(text):
    # Ensure there's a blank line before any line starting with * or -
    text = re.sub(r'(?<!\n\n)(\n)([\*\-] )', r'\n\n\2', text)
    return text

st.set_page_config(page_title="AI Research Agent", page_icon="🔎")
st.markdown("""
    <style>
    [data-testid="stChatInput"] {
        border: 2px solid #2ecc71 !important;
        border-radius: 10px;
    }
    [data-testid="stChatInput"]:focus-within {
        border: 2px solid #27ae60 !important;
        box-shadow: 0 0 0 1px #27ae60 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 AI Research Agent")
st.caption("Ask anything — I'll search the web when I need current information.")

if st.button("🗑️ Clear conversation"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant"):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input and user_input.strip():
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_agent(user_input, st.session_state.messages)
            answer = clean_markdown(answer)
        st.markdown(answer)