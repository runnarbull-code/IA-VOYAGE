import ollama

def generer_itineraire(destination, jours, style):
    # Préparation des instructions pour l'IA
    prompt = f"Expert voyage. Crée un itinéraire pour {destination}, {jours} jours, style {style}. Réponds en français."
    
    try:
        # On active le streaming pour un affichage fluide
        response = ollama.chat(
            model='mistral-nemo',
            messages=[
                {'role': 'system', 'content': 'Tu es une IA spécialisée dans le voyage.'},
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': 0.7},
            stream=True  # Envoie les mots un par un
        )
        return response 
    except Exception as e:
        # En cas de problème avec Ollama
        raise Exception(f"Erreur moteur : {e}")
