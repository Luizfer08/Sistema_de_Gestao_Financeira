const ctx = document.getElementById('grafico');

if (ctx) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Receitas', 'Despesas'],
            datasets: [{
                data: dadosGrafico,
                backgroundColor: ['#396afc', '#ff4b2b']
            }]
        }
    });
}