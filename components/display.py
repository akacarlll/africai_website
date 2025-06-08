import streamlit as st

def render_chat_history():
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def append_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})
