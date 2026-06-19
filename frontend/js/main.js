const BACKEND_URL = "http://127.0.0.1:5000/api";

function startAnalysis() {
    let tag = document.getElementById("playerTagInput").value.trim();
    if (!tag) {
        document.getElementById("errorMsg").innerText = "Lütfen geçerli bir etiket girin!";
        return;
    }
    
    if (tag.startsWith("#")) {
        tag = tag.substring(1);
    }
    
    // Geçici olarak etiketi yerel hafızaya atıp dashboard'a yönlendiriyoruz
    localStorage.setItem("search_player_tag", tag);
    window.location.href = "dashboard.html";
}

function loadDashboardData() {
    const tag = localStorage.getItem("search_player_tag");
    if (!tag) {
        window.location.href = "index.html";
        return;
    }

    fetch(`${BACKEND_URL}/analyze/${tag}`)
        .then(response => {
            if (!response.ok) throw new Error("Oyuncu verisi alınamadı.");
            return response.json();
        })
        .then(data => {
            // Arayüzü Besle
            document.getElementById("playerName").innerText = data.player_info.name;
            document.getElementById("currentTrophies").innerText = data.player_info.trophies;
            document.getElementById("bestTrophies").innerText = data.player_info.best_trophies;
            
            document.getElementById("winRate").innerText = `%${data.analysis_results.calculated_win_rate}`;
            document.getElementById("counterCard").innerText = data.analysis_results.counter_card_threat;

            // Sandıkları Ekrana Bas
            const chestsDiv = document.getElementById("chestsList");
            chestsDiv.innerHTML = "";
            data.upcoming_chests.forEach(chest => {
                chestsDiv.innerHTML += `<div class="chest-item"><h4>+${chest.index + 1}</h4><p>${chest.name}</p></div>`;
            });

            // Desteyi Ekrana Bas
            const deckDiv = document.getElementById("currentDeck");
            deckDiv.innerHTML = "";
            data.player_info.current_deck.forEach(card => {
                deckDiv.innerHTML += `<div class="card-item"><p>${card.name}</p><span>Seviye ${card.level + (14 - card.maxLevel)}</span></div>`;
            });

            // Grafik dosyasını tetikle
            if(window.renderWinLossChart) {
                window.renderWinLossChart(data.analysis_results.calculated_win_rate);
            }
        })
        .catch(err => {
            alert("Veriler yüklenirken hata oluştu! Backend sunucusunun çalıştığından emin olun.");
            window.location.href = "index.html";
        });
}
