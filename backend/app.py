from flask import Flask, jsonify, request
from flask_cors import CORS
from api_client import ClashRoyaleAPI
from analyzer import MeDAnalyzer

app = Flask(__name__)
CORS(app)  # Tarayıcı engellerini aşmak için CORS aktif

api_client = ClashRoyaleAPI()

@app.route('/api/analyze/<string:player_tag>', methods=['GET'])
def analyze_player(player_tag):
    profile = api_client.get_player_profile(player_tag)
    if not profile:
        return jsonify({"error": "Oyuncu bulunamadı veya API hatası"}), 404

    chests = api_client.get_upcoming_chests(player_tag)
    battle_log = api_client.get_battle_log(player_tag)
    
    # Analiz motorunu çalıştır
    analysis = MeDAnalyzer.analyze_deck_performance(battle_log)

    # UI için birleştirilmiş paket veri döndür
    return jsonify({
        "player_info": {
            "name": profile.get("name"),
            "trophies": profile.get("trophies"),
            "best_trophies": profile.get("bestTrophies"),
            "current_deck": profile.get("currentDeck", [])
        },
        "upcoming_chests": chests.get("items", [])[:5],  # İlk 5 sandığı gönder
        "analysis_results": analysis
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
  
