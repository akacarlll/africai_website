import streamlit as st
import os
# from dotenv import load_dotenv
from typing import Dict, Any
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from components.sidebar import sidebar_config
from components.sidebar import sidebar_config
from components.display import render_chat_history, append_message
from services.query_processor import process_query
# load_dotenv()
# Page configuration
st.set_page_config(
    page_title="AfricAI Legal IA",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .search-box {
        margin: 2rem 0;
    }
    .result-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)
def main():
    st.markdown("<h1 class='main-header'>⚖️ AfricAI the Legal IA</h1>", unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        config = sidebar_config()

    st.subheader("💬 Ask a Legal Question")
    render_chat_history()

    if prompt := st.chat_input("Enter your legal question..."):
        append_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching legal documents..."):
                response = process_query(
                    prompt,
                    config["doc_types"],
                    config["retriever_type"],
                    config["retriever_params"],
                    config["start_year"],
                    config["end_year"],
                    config["max_results"]
                )
                st.markdown(response)
                append_message("assistant", response)

def check_environment():
    """Check if required environment variables are set"""
    # required_vars = ["OPENAI_API_KEY"]  # Add your vector DB vars here
    # missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    # if missing_vars:
    #     st.error(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
    #     st.info("Please create a `.env` file with the required variables. See `.env.example` for reference.")
    #     return False
    return True

if __name__ == "__main__":
    if check_environment():
        main()
    else:
        st.stop()