let grafico;
let tipoAtual = "bar";

// ===== CRIAR GRÁFICO =====
function criarGrafico(receitas, despesas){

    if (grafico) grafico.destroy();

    grafico = new Chart(document.getElementById('grafico'), {
        type: tipoAtual,
        data: {
            labels: ['Receitas', 'Despesas'],
            datasets: [{
                data: [receitas, despesas],
                backgroundColor: ['#00c853', '#ff5252']
            }]
        },
        options: {
            responsive: true
        }
    });
}

// ===== ATUALIZA DASHBOARD =====
function atualizarDashboard(){

    const mes = document.getElementById("mes").value;
    const ano = document.getElementById("ano").value;

    document.getElementById('loading').style.display = "block";

    fetch(`/dashboard/dados/?mes=${mes}&ano=${ano}`)
    .then(res => res.json())
    .then(resp => {

        const receitas = Number(resp.receitas || 0);
        const despesas = Number(resp.despesas || 0);
        const saldo = Number(resp.saldo || 0);
        const saldoPrevisto = Number(resp.saldo_previsto || 0);

        document.getElementById('receitas').innerText = `R$ ${receitas.toFixed(2)}`;
        document.getElementById('despesas').innerText = `R$ ${despesas.toFixed(2)}`;
        document.getElementById('saldoAtual').innerText = `R$ ${saldo.toFixed(2)}`;
        document.getElementById('saldoPrevisto').innerText = `R$ ${saldoPrevisto.toFixed(2)}`;

        // ===== ALERTA PREVISTO =====
        const alertaPrevisto = document.getElementById('alertaPrevisto');

        alertaPrevisto.innerText = resp.alerta_previsto || "";

        if (saldoPrevisto < 0){
            alertaPrevisto.className = "fw-bold text-white d-block mt-1";
        } else {
            alertaPrevisto.className = "fw-bold text-dark d-block mt-1";
        }

        // ===== ALERTAS GERAIS =====
        const alertasGeraisDiv = document.getElementById('alertasGerais');

        if (resp.alertas_gerais && resp.alertas_gerais.length > 0){

            let html = '<div class="alert alert-warning mb-1"><ul class="mb-0">';

            resp.alertas_gerais.forEach(alerta => {
                html += `<li>${alerta}</li>`;
            });

            html += '</ul></div>';

            alertasGeraisDiv.innerHTML = html;

        } else {
            alertasGeraisDiv.innerHTML = "";
        }

        // ===== COR DO CARD =====
        const card = document.getElementById('cardPrevisto');

        card.className = "card card-premium mt-3 p-3 " +
            (saldoPrevisto < 0 ? "bg-despesa" :
             saldoPrevisto < 100 ? "bg-warning text-dark" :
             "bg-saldo");

        criarGrafico(receitas, despesas);
    })
    .finally(() => {
        document.getElementById('loading').style.display = "none";
    });
}

// ===== EVENTOS =====
document.getElementById('mes').addEventListener('change', atualizarDashboard);
document.getElementById('ano').addEventListener('input', atualizarDashboard);

document.getElementById('tipoGrafico').addEventListener('change', function(){
    tipoAtual = this.value;
    atualizarDashboard();
});

// ===== INIT =====
atualizarDashboard();