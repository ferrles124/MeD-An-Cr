function startAnalysis() {
    let tag = document.getElementById("playerTagInput").value.trim().toUpperCase();
    if (!tag) {
        document.getElementById("errorMsg").innerText = "Lütfen geçerli bir etiket girin!";
        return;
    }
    if (tag.startsWith("#")) tag = tag.substring(1);
    
    localStorage.setItem("search_player_tag", tag);
    window.location.href = "dashboard.html";
}

function loadDashboardData() {
    const tag = localStorage.getItem("search_player_tag");
    if (!tag) {
        window.location.href = "index.html";
        return;
    }

    // Doğrudan GitHub üzerindeki hazır JSON dosyasına yönlendiriyoruz
    fetch(`data/${tag}.json`)
        .then(response => {
            if (!response.ok) throw new Error("Bu oyuncu için henüz analiz verisi üretilmemiş.");
            return response.json();
        })
        .then(data => {
            document.getElementById("playerName").innerText = data.name;
            document.getElementById("currentTrophies").innerText = data.trophies;
            document.getElementById("bestTrophies").innerText = data.best_trophies;
            document.getElementById("winRate").innerText = `%${data.win_rate}`;
            document.getElementById("counterCard").innerText = data.win_rate > 50 ? "Düşük Risk" : "Yüksek Risk";

            const chestsDiv = document.getElementById("chestsList");
            chestsDiv.innerHTML = "";
            data.upcoming_chests.forEach(chest => {
                chestsDiv.innerHTML += `<div class="chest-item"><h4>+${chest.index + 1}</h4><p>${chest.name}</p></div>`;
            });

            const deckDiv = document.getElementById("currentDeck");
            deckDiv.innerHTML = "";
            data.current_deck.forEach(card => {
                deckDiv.innerHTML += `<div class="card-item"><p>${card.name}</p><span>Seviye ${card.level + (14 - card.maxLevel)}</span></div>`;
            });

            if(window.renderWinLossChart) {
                window.renderWinLossChart(data.win_rate);
            }
        })
        .catch(err => {
            alert(err.message + " (Not: Profilinizin listeye eklenip Actions çalıştırıldığından emin olun.)");
            window.location.href = "index.html";
        });
}
