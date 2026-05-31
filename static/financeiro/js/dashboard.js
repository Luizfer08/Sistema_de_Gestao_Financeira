// OBTÉM JSON SALVO NO HTML
function obterJsonScript(id) {

    // Busca elemento pelo ID
    const el = document.getElementById(id);

    // Retorna null caso não exista
    if (!el) return null;

    // Converte conteúdo para objeto JSON
    return JSON.parse(el.textContent);
}


// CRIA GRÁFICO FINANCEIRO
function criarGraficoFinanceiro() {

    // Dados vindos do backend
    const dados = obterJsonScript(
        "graficoFinanceiroData"
    );

    // Canvas do gráfico
    const canvas = document.getElementById(
        "graficoFinanceiro"
    );

    // Valida dados e biblioteca Chart.js
    if (!dados || !canvas || typeof Chart === "undefined")
        return;


    // CRIA GRÁFICO
    new Chart(canvas, {

        data: {

            // Labels do eixo X
            labels: dados.labels,

            // CONJUNTO DE DADOS
            datasets: [

                // RECEITAS
                {
                    type: "bar",

                    label: "Receitas",

                    data: dados.receitas,

                    backgroundColor: "#62bf93",

                    borderRadius: 2,
                },

                // DESPESAS
                {
                    type: "bar",

                    label: "Despesas",

                    // Valores negativos para gráfico
                    data: dados.despesas.map(
                        (valor) => -Math.abs(valor)
                    ),

                    backgroundColor: "#f17878",

                    borderRadius: 2,
                },

                // SALDO FUTURO
                {
                    type: "line",

                    label: "Saldo futuro",

                    data: dados.saldo_futuro,

                    borderColor: "#4a7df0",

                    backgroundColor: "#ffffff",

                    // Linha tracejada
                    borderDash: [4, 4],

                    borderWidth: 2,

                    pointRadius: 3,

                    // Suaviza linha
                    tension: 0.35,
                },
            ],
        },


        // CONFIGURAÇÕES DO GRÁFICO
        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                // LEGENDA
                legend: {

                    position: "bottom",

                    labels: {

                        boxWidth: 8,

                        font: {
                            size: 10
                        },
                    },
                },
            },

            // EIXOS
            scales: {

                // EIXO X
                x: {

                    grid: {
                        display: false
                    },

                    ticks: {

                        font: {
                            size: 10
                        },
                    },
                },

                // EIXO Y
                y: {

                    grid: {
                        color: "#eef1f5"
                    },

                    ticks: {

                        font: {
                            size: 10
                        },

                        // Formata valores monetários
                        callback: (value) =>
                            `R$ ${Math.abs(value)}`,
                    },
                },
            },
        },
    });
}


// CRIA GRÁFICO DE CATEGORIAS
function criarGraficoCategorias() {

    // Dados das categorias
    const categorias = obterJsonScript(
        "categoriasData"
    ) || [];

    // Canvas do gráfico
    const canvas = document.getElementById(
        "graficoCategorias"
    );

    // Valida canvas e biblioteca
    if (!canvas || typeof Chart === "undefined")
        return;

    // Verifica se existem valores maiores que zero
    const temValores = categorias.some(
        (item) => Number(item.total) > 0
    );

    const dados = categorias;


    // CRIA GRÁFICO
    new Chart(canvas, {

        type: "doughnut",

        data: {

            // Nome das categorias
            labels: dados.map(
                (item) => item.nome
            ),

            datasets: [{

                // Valores das categorias
                data: dados.map((item) =>

                    temValores
                        ? Number(item.total)
                        : 1
                ),

                // Cores das categorias
                backgroundColor: dados.map(
                    (item) => item.cor
                ),

                borderWidth: 0,
            }],
        },


        // CONFIGURAÇÕES
        options: {

            responsive: true,

            maintainAspectRatio: false,

            // Espaço interno do gráfico
            cutout: "58%",

            plugins: {

                // Remove legenda padrão
                legend: {
                    display: false
                },

                // TOOLTIP
                tooltip: {

                    callbacks: {

                        // Texto exibido ao passar mouse
                        label: (context) => {

                            const categoria =
                                dados[context.dataIndex];

                            return `
                                ${categoria.nome}:
                                ${formatarMoeda(categoria.total)}
                            `;
                        },
                    },
                },
            },
        },
    });
}

// MARCAR NOTIFICAÇÃO COMO LIDA
document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".notification-read")
    .forEach(botao => {

        botao.addEventListener("click", function() {

            const notificacao =
                this.closest(".dashboard-notification");

            notificacao.style.opacity = "0";
            notificacao.style.transform = "translateX(20px)";

            setTimeout(() => {
                notificacao.remove();
            }, 250);

        });

    });

});


// FORMATA VALOR MONETÁRIO
function formatarMoeda(valor) {

    return Number(valor || 0).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL",
        }
    );
}


// EXECUTA APÓS CARREGAR PÁGINA
document.addEventListener("DOMContentLoaded", function () {

    // Cria gráfico financeiro
    criarGraficoFinanceiro();

    // Cria gráfico de categorias
    criarGraficoCategorias();
});