class MeDAnalyzer:
    @staticmethod
    def analyze_deck_performance(battle_log):
        if not battle_log:
            return {"error": "Veri bulunamadı"}

        total_battles = 0
        wins = 0
        loss_reasons = {}

        for battle in battle_log:
            # Sadece 1v1 normal maçları analiz edelim
            if battle.get("type") in ["1v1", "pvp"]:
                total_battles += 1
                crowns_earned = battle.get("team", [{}])[0].get("crowns", 0)
                crowns_lost = battle.get("opponent", [{}])[0].get("crowns", 0)

                if crowns_earned > crowns_lost:
                    wins += 1
                else:
                    # Rakipten en çok hangi kart yüzünden yenildiğimizi analiz etmek için
                    opponent_cards = battle.get("opponent", [{}])[0].get("cards", [])
                    for card in opponent_cards:
                        card_name = card.get("name")
                        loss_reasons[card_name] = loss_reasons.get(card_name, 0) + 1

        win_rate = (wins / total_battles) * 100 if total_battles > 0 else 0
        
        # En çok zorlanılan kartı bulma
        hardest_card = max(loss_reasons, key=loss_reasons.get) if loss_reasons else "Bilinmiyor"

        return {
            "total_analyzed_battles": total_battles,
            "calculated_win_rate": round(win_rate, 2),
            "counter_card_threat": hardest_card
        }
      
