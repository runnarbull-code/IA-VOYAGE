"""
API Flask pour le générateur d'itinéraires de voyage.
Ce backend fait le pont entre le frontend et Ollama Cloud API.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le chemin du module pipeline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from itinerary_generator2 import generate_itinerary, DEFAULT_MODEL, FINETUNED_MODEL
except ImportError:
    # Fallback si pipeline.py n'est pas trouvé
    def generate_itinerary(destination, duration, interests, budget=None, model_name=None):
        return "Erreur: Le fichier pipeline.py n'a pas été trouvé. Assurez-vous qu'il est dans le même dossier que app.py"
    DEFAULT_MODEL = "gpt-oss:120b-cloud"
    FINETUNED_MODEL = "gpt-oss:120b-cloud"

app = Flask(__name__, template_folder='.',static_folder='.')

# Configuration CORS pour le déploiement
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # En production, remplacez par votre domaine
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def index():
    """Servir la page d'accueil."""
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Endpoint pour générer un itinéraire.
    
    Expects JSON:
    {
        "destination": "Paris",
        "duration": 5,
        "interests": ["art", "food"],
        "budget": 2000.00,
        "model": "mistral:7b-instruct" (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validation des données
        if not data:
            return jsonify({"error": "Aucune donnée fournie"}), 400
        
        destination = data.get('destination', '').strip()
        duration = data.get('duration')
        interests = data.get('interests', [])
        budget = data.get('budget')
        model_name = data.get('model', DEFAULT_MODEL)
        
        # Validation
        if not destination:
            return jsonify({"error": "La destination est requise"}), 400
        
        if not duration or not isinstance(duration, int) or duration < 1 or duration > 30:
            return jsonify({"error": "La durée doit être entre 1 et 30 jours"}), 400
        
        if not isinstance(interests, list):
            return jsonify({"error": "Les intérêts doivent être une liste"}), 400
        
        # Validation du budget (optionnel)
        if budget is not None:
            try:
                budget = float(budget)
                if budget < 0:
                    return jsonify({"error": "Le budget ne peut pas être négatif"}), 400
            except (TypeError, ValueError):
                return jsonify({"error": "Le budget doit être un nombre valide"}), 400
        
        # Générer l'itinéraire
        print(f"Génération d'itinéraire pour {destination}, {duration} jours, budget: {budget}, intérêts: {interests}")
        itinerary = generate_itinerary(
            destination=destination,
            duration=duration,
            interests=interests,
            budget=budget,
            model_name=model_name
        )
        
        return jsonify({
            "success": True,
            "itinerary": itinerary,
            "destination": destination,
            "duration": duration,
            "interests": interests,
            "budget": budget
        })
        
    except Exception as e:
        print(f"Erreur lors de la génération: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Erreur lors de la génération: {str(e)}"
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Retourner la liste des modèles disponibles."""
    return jsonify({
        "models": [
            DEFAULT_MODEL,
            FINETUNED_MODEL,
            "llama2:7b",
            "gemma:7b"
        ],
        "default": DEFAULT_MODEL
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Vérifier l'état de l'API."""
    return jsonify({
        "status": "ok",
        "message": "API du générateur d'itinéraires opérationnelle"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("🌍 Serveur de génération d'itinéraires démarré")
    print("=" * 60)
    print(f"📍 URL: http://localhost:{port}")
    print(f"📝 API: http://localhost:{port}/api/generate")
    print(f"🔧 Mode: {'Debug' if debug else 'Production'}")
    print("=" * 60)
    
    app.run(debug=debug, host='0.0.0.0', port=port)
