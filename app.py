import streamlit as st
import ollama
import time
from engine import generer_itineraire

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Horizon IA Voyage", page_icon="✈️", layout="wide")

# --- INJECTION CSS & JAVASCRIPT AVANCÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }

    /* Panneau de saisie Glassmorphism (sans titre) */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        margin-top: 10px;
    }

    /* Style moderne du bouton */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border: none;
        color: white;
        padding: 12px 0px;
        font-weight: 600;
        border-radius: 14px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.4);
    }

    /* Titre animé */
    .main-title {
        background: linear-gradient(90deg, #60a5fa, #3b82f6, #93c5fd);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-weight: 800;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Inputs personnalisés */
    input {
        background-color: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }

    /* Cacher les labels Streamlit pour un look plus clean si nécessaire */
    .stSelectbox label, .stSlider label, .stTextInput label {
        color: #94a3b8 !important;
        font-weight: 400 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title">✈️ Horizon IA Voyage</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #94a3b8; margin-bottom: 40px;">L\'intelligence artificielle au service de votre prochaine aventure.</p>', unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL ---
col_param, col_res = st.columns([1, 2], gap="large")

with col_param:
    # Le titre "Configuration" a été supprimé pour un look épuré
    with st.container():
        dest = st.text_input("📍 Où souhaitez-vous aller ?", placeholder="ex: Japon, Canada, Grèce...")
        jours = st.select_slider("📅 Durée du séjour (jours)", options=list(range(1, 15)), value=3)
        style = st.selectbox("🎭 Style de voyage", ["Aventure & Nature", "Culture & Histoire", "Détente & Luxe", "Budget Éco"])
        
        st.write("")
        btn_generer = st.button("Lancer la planification ✨")

with col_res:
    if btn_generer:
        if not dest:
            st.warning("⚠️ Veuillez indiquer une destination.")
        else:
            st.markdown(f"### 🗺️ Votre itinéraire à {dest}")
            
            with st.chat_message("assistant", avatar="✨"):
                try:
                    barre = st.progress(0, text="Analyse des destinations...")
                    
                    flux = generer_itineraire(dest, jours, style)
                    
                    for p in range(0, 101, 25):
                        time.sleep(0.1)
                        barre.progress(p)
                    
                    chunks = []
                    
                    def generateur():
                        for morceau in flux:
                            c = morceau['message']['content']
                            chunks.append(c)
                            yield c
                    
                    st.write_stream(generateur)
                    
                    barre.empty()
                    st.success("Planification terminée !")
                    st.balloons()
                    
                    st.download_button(
                        label="💾 Sauvegarder l'itinéraire",
                        data="".join(chunks),
                        file_name=f"horizon_{dest}.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Erreur : {e}")
    else:
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 350px; border: 2px dashed rgba(255,255,255,0.05); border-radius: 24px; background: rgba(255,255,255,0.02);">
                <span style="font-size: 3rem; margin-bottom: 10px;">🌍</span>
                <p style="color: #64748b; font-size: 1.1rem; text-align: center; padding: 0 20px;">
                    Configurez votre voyage à gauche et laissez l'IA créer votre programme sur mesure.
                </p>
            </div>
        """, unsafe_allow_html=True)