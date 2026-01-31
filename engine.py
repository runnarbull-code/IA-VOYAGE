from groq import Groq
import streamlit as st

def generer_itineraire(destination, jours, style):
    # Récupère la clé API cachée dans les paramètres de Streamlit
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error("⚠️ La clé GROQ_API_KEY est manquante dans les Secrets.")
        return

    client = Groq(api_key=api_key)
    
    prompt = f"Expert voyage. Crée un itinéraire pour {destination}, {jours} jours, style {style}. Réponds en français."
    
    try:
        # On utilise un modèle puissant disponible sur le Cloud
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {'role': 'system', 'content': 'Tu es une IA spécialisée dans le voyage.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.7,
            stream=True  # Permet l'affichage progressif du texte
        )
        return response 
    except Exception as e:
        raise Exception(f"Erreur moteur Cloud : {e}")