import os
import json
import requests

class MeDActionAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("CR_API_KEY")
        self.base_url = "https://api.clashroyale.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        # Analiz etmek istediğin oyuncu etiketlerini buraya ekle
        self.target_players = ["9PJ92QQ2"] 

    def _format_tag(self, tag):
        return f"%23{tag.strip().upper().replace('#', '')}"

    def fetch_data(self, endpoint, player_tag):
        url = f"{self.base_url}/players/{self._format_tag(player_tag)}{endpoint}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def analyze(self):
        # Çıktı klasörünü oluştur
        os.makedirs("frontend/data", exist_ok=True)

        for tag in self.target_players:
            profile = self.fetch_data("", tag)
            chests = self.fetch_data("/upcomingchests", tag)
            battle_log = self.fetch_data("/battlelog", tag)

            if not profile:
                continue

            # Temel Deste/Galibiyet Analizi
            total_battles = 0
            wins = 0
            for battle in (battle_log or []):
                if battle.get("type") in ["1v1", "pvp"]:
                    total_battles += 1
                    if battle.get("team", [{}])[0].get("crowns", 0) > battle.get("opponent", [{}])[0].get("crowns", 0):
                        wins += 1
            
            win_rate = round((wins / total_battles) * 100, 2) if total_battles > 0 else 0

            # UI için optimize edilmiş tek bir JSON dosyası hazırla
            output_data = {
                "name": profile.get("name"),
                "trophies": profile.get("trophies"),
                "best_trophies": profile.get("bestTrophies"),
                "win_rate": win_rate,
                "current_deck": profile.get("currentDeck", []),
                "upcoming_chests": (chests or {}).get("items", [])[:5]
            }

            # Her oyuncunun verisini kendi etiketiyle kaydet
            with open(f"frontend/data/{tag}.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    analyzer = MeDActionAnalyzer()
    analyzer.analyze()
    
