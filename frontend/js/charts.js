window.renderWinLossChart = function(winRate) {
    const ctx = document.getElementById('winLossChart').getContext('2d');
    
    const lossRate = 100 - winRate;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Kazanma Oranı', 'Kaybetme Oranı'],
            datasets: [{
                data: [winRate, lossRate],
                backgroundColor: ['#10b981', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#f8fafc' }
                }
            }
        }
    });
}
