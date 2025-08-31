import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from components.sidebar import sidebar_config
from components.display import render_chat_history, append_message
from services.query_processor import process_query

# Page configuration
st.set_page_config(
    page_title="AfricAI Legal IA",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    /* Style pour le bouton de navigation */
    .nav-button {
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 999;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Header avec navigation */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .nav-buttons {
        display: flex;
        gap: 0.5rem;
    }
    
    .breadcrumb {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .breadcrumb a {
        color: #1f4e79;
        text-decoration: none;
    }
    
    .breadcrumb a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Breadcrumb navigation
    st.markdown("""
    <div class="breadcrumb">
        🏠 <a href="#" onclick="window.location.reload()">Accueil</a> > 💬 Chat Legal
    </div>
    """, unsafe_allow_html=True)
    
    # Header avec boutons de navigation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h1 class='main-header'>⚖️ AfricAI the Legal IA</h1>", unsafe_allow_html=True)
    
    with col2:
        # Bouton de retour vers la page principale
        if st.button("🏠 Accueil", type="secondary", help="Retour à la page principale"):
            st.switch_page("main.py")
        
        # Bouton pour réinitialiser la conversation
        if st.button("🔄 Nouveau Chat", type="secondary", help="Commencer une nouvelle conversation"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialisation des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Configuration sidebar
    with st.sidebar:
        config = sidebar_config()
        
        # Ajout d'une section navigation dans la sidebar
        st.markdown("---")
        st.subheader("📍 Navigation")
        if st.button("🏠 Retour à l'accueil", use_container_width=True):
            st.switch_page("main.py")
        
        if st.button("🗑️ Vider l'historique", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Informations sur la session
        st.markdown("---")
        st.subheader("📊 Session Info")
        st.info(f"💬 Messages: {len(st.session_state.messages)}")
        if st.session_state.messages:
            st.success("✅ Chat actif")
        else:
            st.warning("🆕 Nouveau chat")

    # Interface de chat
    st.subheader("💬 Posez votre Question Juridique")
    
    # Afficher un message de bienvenue si c'est le premier message
    if not st.session_state.messages:
        st.info("👋 Bienvenue ! Je suis votre assistant juridique IA. Posez-moi vos questions sur le droit africain.")
    
    # Afficher l'historique des messages
    render_chat_history()
    
    # Zone de saisie
    if prompt := st.chat_input("Entrez votre question juridique..."):
        append_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Recherche dans les documents juridiques..."):
                try:
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
                except Exception as e:
                    error_msg = f"❌ Désolé, une erreur s'est produite : {str(e)}"
                    st.error(error_msg)
                    append_message("assistant", error_msg)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["TOGETHER_AI_API_KEY", "GOOGLE_API_KEY"] 
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        st.error(f"⚠️ Variables d'environnement manquantes: {', '.join(missing_vars)}")
        st.info("Veuillez créer un fichier `.env` avec les variables requises. Voir `.env.example` pour référence.")
        
        # Bouton pour retourner à l'accueil même en cas d'erreur
        if st.button("🏠 Retour à l'accueil"):
            st.switch_page("main.py")
        
        return False
    return True

if __name__ == "__main__":
    if check_environment():
        main()
    else:
        st.stop()