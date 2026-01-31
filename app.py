import streamlit as st
import time
from engine import generer_itineraire

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Horizon IA Voyage", page_icon="✈️", layout="wide")

# --- INJECTION CSS (Gardé tel quel car il est top !) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 14px;
        transition: all 0.3s ease;
    }
    .main-title {
        background: linear-gradient(90deg, #60a5fa, #3b82f6, #93c5fd);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-weight: 800;
        text-align: center;
        font-size: 3.5rem;
    }
    @keyframes shine { to { background-position: 200% center; } }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title">✈️ Horizon IA Voyage</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #94a3b8; margin-bottom: 40px;">L\'intelligence artificielle au service de votre prochaine aventure.</p>', unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL ---
col_param, col_res = st.columns([1, 2], gap="large")

with col_param:
    with st.container():
        dest = st.text_input("📍 Où souhaitez-vous aller ?", placeholder="ex: Japon, Canada, Grèce...")
        jours = st.select_slider("📅 Durée du séjour (jours)", options=list(range(1, 15)), value=3)
        style = st.selectbox("🎭 Style de voyage", ["Aventure & Nature", "Culture & Histoire", "Détente & Luxe", "Budget Éco"])
        btn_generer = st.button("Lancer la planification ✨")

with col_res:
    if btn_generer:
        if not dest:
            st.warning("⚠️ Veuillez indiquer une destination.")
        else:
            st.markdown(f"### 🗺️ Votre itinéraire à {dest}")
            with st.chat_message("assistant", avatar="✨"):
                try:
                    barre = st.progress(0, text="Connexion au Cloud IA...")
                    flux = generer_itineraire(dest, jours, style)
                    
                    chunks = []
                    # Nouvelle fonction pour lire le flux Groq
                    def generateur():
                        for morceau in flux:
                            # Format spécifique aux clés API Cloud (Groq/OpenAI)
                            c = morceau.choices[0].delta.content
                            if c:
                                chunks.append(c)
                                yield c
                    
                    st.write_stream(generateur)
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
        st.markdown('<div style="border: 2px dashed rgba(255,255,255,0.05); border-radius: 24px; padding: 50px; text-align: center;">🌍<br>Configurez votre voyage à gauche.</div>', unsafe_allow_html=True)