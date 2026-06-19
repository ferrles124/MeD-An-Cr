import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ClashRoyaleAPI:
    def __init__(self):
        # GitHub Secrets veya .env dosyasından tokenı alır
        self.api_key = os.getenv("CR_API_KEY")
        self.base_url = "https://api.clashroyale.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }

    def _format_tag(self, tag):
        # Etiketin başındaki # işaretini URL uyumlu hale getirir
        tag = tag.strip().upper()
        if tag.startswith("#"):
            tag = tag[1:]
        return f"%23{tag}"

    def get_player_profile(self, player_tag):
        formatted_tag = self._format_tag(player_tag)
        url = f"{self.base_url}/players/{formatted_tag}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def get_upcoming_chests(self, player_tag):
        formatted_tag = self._format_tag(player_tag)
        url = f"{self.base_url}/players/{formatted_tag}/upcomingchests"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def get_battle_log(self, player_tag):
        formatted_tag = self._format_tag(player_tag)
        url = f"{self.base_url}/players/{formatted_tag}/battlelog"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
      
