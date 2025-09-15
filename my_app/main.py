import streamlit as st
import time
from .config.load_env_variable import init_env_variables

init_env_variables()

# Page configuration
st.set_page_config(
    page_title="Africai - Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Hide Streamlit menu, footer, and sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Font stack */
    body, .main-title, .subtitle, .feature-title, .feature-description, .stat-label {
        font-family: 'Inter', 'Roboto', sans-serif;
    }
    
    /* Main container */
    .main-container {
        background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Main title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out 0.3s both;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 1s ease-out 0.6s both;
        width: 100%; /* Make card take full column width */
        height: 100%; /* Make card of equal height */
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-top: 1rem; /* Add space between button and card */
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        opacity: 0.8;
        line-height: 1.6;
        flex-grow: 1; /* Allows description to take available space */
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    
    /* Stats container */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 4rem 0 2rem 0; /* Adjusted margin */
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        animation: fadeInUp 1s ease-out 1.2s both;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
        color: #ffd700;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Main container
st.markdown("""
<div class="main-container">
    <div class="main-title">⚖️ Africai Legal Assistant</div>
    <div class="subtitle">
        Your intelligent legal AI companion powered by RAG and agentic systems
        <br>Get precise legal insights and contextual answers to your legal questions
    </div>
</div>
""", unsafe_allow_html=True)

# Columns for centering content
col1, col2, col3 = st.columns([1, 6, 1]) # Adjusted column ratio for wider central content

with col2:
    # Features section with buttons above each card
    feat_col1, feat_col2, feat_col3 = st.columns(3, gap="large")

    with feat_col1:
        if st.button("🚀 Start Legal Chat", use_container_width=True):
            st.switch_page("pages/rag_app.py")
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Legal RAG System</div>
            <div class="feature-description">
                Advanced Retrieval-Augmented Generation for precise document analysis and intelligent question answering.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feat_col2:
        if st.button("🤖 Start Agentic Chat", use_container_width=True):
            st.info("Dashboard under development...")
            # st.switch_page("pages/agent_app.py")
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">Agentic RAG System</div>
            <div class="feature-description">
                Leverages autonomous AI agents to perform complex legal research, analysis, and multi-step task execution.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feat_col3:
        if st.button("📊 Dashboard", use_container_width=True):
            st.info("Dashboard under development...")
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Dashboard</div>
            <div class="feature-description">
                Visualize key metrics, track query history, and manage your legal cases in an intuitive, unified interface.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics/information section
    st.markdown("""
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-number">24/7</span>
            <div class="stat-label">Availability</div>
        </div>
        <div class="stat-item">
            <span class="stat-number">∞</span>
            <div class="stat-label">Legal Queries</div>
        </div>
        <div class="stat-item">
            <span class="stat-number">⚡</span>
            <div class="stat-label">AI Speed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer with supplementary information
st.markdown("---")

# Help section
with st.expander("💡 How to use Africai Legal Assistant?"):
    st.write("""
    **Simple steps to get started:**
    
    1. **Click "Start Legal Chat"** to access the standard RAG conversational interface.
    2. **Click "Start Agentic Chat"** to use the advanced, multi-step AI agent.
    3. **Ask your legal question** in natural language.
    4. **Get AI-powered answers** based on legal knowledge and document analysis.
    
    **Tips for better legal assistance:**
    - Be specific about your legal jurisdiction when relevant.
    - Provide context for your legal questions.
    - Remember this is for informational purposes - consult a qualified attorney for legal advice.
    """)

# Custom welcome message
if "first_visit" not in st.session_state:
    st.session_state.first_visit = True
    with st.container():
        st.success("👋 Welcome to Africai! Your legal AI assistant is ready to help with your legal questions.")
        time.sleep(3) 
        st.rerun()
