// Controla a despesa que esta em edicao
let despesaEmEdicao = null;

// Este arquivo controla o popup, a tabela e as requisicoes AJAX de despesas.


// OBTEM TOKEN CSRF DO DJANGO
function getCSRFToken() {

    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    )?.value || "";
}


// EXECUTA APOS CARREGAR A PAGINA
document.addEventListener("DOMContentLoaded", function () {

    // FORMULARIO DE DESPESA
    const formDespesa = document.getElementById(
        "formDespesa"
    );

    // CAMPOS DE PARCELAMENTO
    const parcelada = document.getElementById(
        "despesaParcelada"
    );

    const recorrente = formDespesa?.elements.recorrente;

    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelas"
    );


    // CONTROLA CAMPO DE PARCELAS
    if (parcelada && quantidadeParcelas) {

        parcelada.addEventListener("change", function () {

            // Habilita ou desabilita input
            quantidadeParcelas.disabled = !this.checked;

            quantidadeParcelas.required = this.checked;

            // Limpa valor caso desmarcado
            if (!this.checked)
                quantidadeParcelas.value = "";

            atualizarTravamentoDespesa();
        });
    }

    if (recorrente) {

        recorrente.addEventListener("change", atualizarTravamentoDespesa);
    }


    // Verifica existencia do formulario
    if (!formDespesa) return;


    // ENVIO DO FORMULARIO
    formDespesa.addEventListener("submit", function (e) {

        e.preventDefault();

        // Dados do formulario
        const formData = new FormData(this);

        const editando = Boolean(despesaEmEdicao);

        // Botao de envio
        const btn = formDespesa.querySelector(
            'button[type="submit"]'
        );

        // URL DE CRIACAO
        const urlCriar = typeof URL_CRIAR_DESPESA !== "undefined"

            ? URL_CRIAR_DESPESA

            : "/despesas/criar/";

        // URL DE EDICAO
        const urlEditar = `${
            typeof DESPESA_URL_EDITAR_BASE !== "undefined"

                ? DESPESA_URL_EDITAR_BASE

                : "/despesas/editar/"
        }${despesaEmEdicao}/`;

        // Desabilita botao
        btn.disabled = true;

        btn.innerText = "Salvando...";


        // REQUISICAO PARA API
        fetch(despesaEmEdicao ? urlEditar : urlCriar, {

            method: "POST",

            headers: {
                "X-CSRFToken": getCSRFToken()
            },

            body: formData,
        })

        .then((res) => res.json())

        .then((data) => {

            // Erro retornado pela API
            if (!data.success) {

                alert(
                    data.error || "Erro ao salvar despesa"
                );

                return;
            }

            // Mes atual da tela
            const mesAtual = typeof DESPESA_MES_ATUAL !== "undefined"

                ? DESPESA_MES_ATUAL

                : "";

            // Linha existente
            const linhaExistente = document.getElementById(
                `linha-${data.id}`
            );

            // Valor anterior
            const valorAnterior = linhaExistente

                ? parseNumero(
                    linhaExistente.dataset.valor || 0
                )

                : 0;


            // Atualiza tabela caso despesa pertenca ao mes atual
            if (data.data_iso.startsWith(mesAtual)) {

                // Atualiza linha existente
                if (linhaExistente) {

                    atualizarLinhaDespesa(data);

                    atualizarTotalDespesa(
                        parseNumero(data.valor) - valorAnterior
                    );

                } else {

                    // Cria nova linha
                    adicionarLinhaDespesa(data);

                    atualizarTotalDespesa(
                        parseNumero(data.valor)
                    );
                }

            // Remove linha caso tenha mudado de mes
            } else if (linhaExistente) {

                linhaExistente.remove();

                atualizarTotalDespesa(-valorAnterior);

                verificarTabelaVazia();
            }

            // Fecha modal
            fecharModalDespesa();

            if (!editando) {

                mostrarMensagemSucesso(
                    "Despesa adicionada com sucesso!"
                );
            }
        })

        // Captura erros
        .catch(() => alert("Erro ao salvar despesa"))

        // Reativa botao
        .finally(() => {

            btn.disabled = false;

            btn.innerHTML = `
                <img src="/static/financeiro/img/check.png" alt="">
                Salvar
            `;
        });
    });
});


function atualizarTravamentoDespesa() {

    const form = document.getElementById("formDespesa");
    const parcelada = document.getElementById("despesaParcelada");
    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelas"
    );

    if (!form || !parcelada || !quantidadeParcelas)
        return;

    const recorrente = form.elements.recorrente;

    if (!recorrente)
        return;

    if (recorrente.checked) {

        parcelada.checked = false;
        parcelada.disabled = true;
        quantidadeParcelas.value = "";
        quantidadeParcelas.disabled = true;
        quantidadeParcelas.required = false;

        return;
    }

    parcelada.disabled = false;

    if (parcelada.checked) {

        recorrente.checked = false;
        recorrente.disabled = true;
        quantidadeParcelas.disabled = false;
        quantidadeParcelas.required = true;

        return;
    }

    recorrente.disabled = false;
    quantidadeParcelas.disabled = true;
    quantidadeParcelas.required = false;
}


// ABRE MODAL DE DESPESA
function abrirModalDespesa(dados = null) {

    // ELEMENTOS DO MODAL
    const modal = document.getElementById(
        "modalDespesa"
    );

    const form = document.getElementById(
        "formDespesa"
    );

    const titulo = document.getElementById(
        "modalDespesaTitulo"
    );

    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelas"
    );

    // Define despesa em edicao
    despesaEmEdicao = dados?.id || null;

    // Reseta formulario
    form.reset();

    // Define titulo do modal
    titulo.innerText = despesaEmEdicao

        ? "Editar Despesa"

        : "Adicionar Despesa";


    // PREENCHE DADOS NO MODO EDICAO
    if (dados) {

        form.elements.descricao.value =
            dados.descricao || "";

        form.elements.valor.value =
            normalizarNumero(dados.valor);

        form.elements.data.value =
            dados.data || "";

        form.elements.categoria.value =
            dados.categoriaId || "";

        form.elements.conta.value =
            dados.conta || "";

        form.elements.recorrente.checked =
            dados.recorrente === "true"
            || dados.recorrente === true;

        form.elements.parcelada.checked =
            dados.parcelada === "true"
            || dados.parcelada === true;

        quantidadeParcelas.disabled =
            !form.elements.parcelada.checked;

        quantidadeParcelas.required =
            form.elements.parcelada.checked;

        form.elements.quantidade_parcelas.value =
            dados.quantidadeParcelas || "";

    } else if (quantidadeParcelas) {

        // Desabilita parcelas no modo criacao
        quantidadeParcelas.disabled = true;

        quantidadeParcelas.required = false;
    }

    atualizarTravamentoDespesa();

    // Abre modal
    modal.classList.remove("is-closing");

    modal.classList.add("is-open");

    modal.setAttribute("aria-hidden", "false");

    // Foca no input valor
    setTimeout(() => {

        document.getElementById(
            "valorDespesa"
        )?.focus();

    }, 80);
}


// FECHA MODAL
function fecharModalDespesa() {

    const modal = document.getElementById(
        "modalDespesa"
    );

    const form = document.getElementById(
        "formDespesa"
    );

    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelas"
    );

    // Limpa edicao atual
    despesaEmEdicao = null;

    // Reseta formulario
    form.reset();

    // Define titulo padrao
    document.getElementById(
        "modalDespesaTitulo"
    ).innerText = "Adicionar Despesa";

    // Desabilita campo de parcelas
    if (quantidadeParcelas) {

        quantidadeParcelas.disabled = true;

        quantidadeParcelas.required = false;
    }

    atualizarTravamentoDespesa();

    modal.setAttribute("aria-hidden", "true");

    fecharModalComAnimacao(modal);
}


// FECHA MODAL COM ANIMACAO
function fecharModalComAnimacao(modal) {

    modal.classList.remove("is-open");

    modal.classList.add("is-closing");

    setTimeout(() => {

        modal.classList.remove("is-closing");

    }, 280);
}


// GERA HTML DA LINHA DE DESPESA
function linhaDespesaHtml(data) {

    // ICONES PADRAO
    const icons = typeof DESPESA_ICONS !== "undefined"

        ? DESPESA_ICONS

        : {};

    const editarIcon =
        icons.editar
        || "/static/financeiro/img/editar.png";

    const lixeiraIcon =
        icons.lixeira
        || "/static/financeiro/img/lixeira.png";

    return `
        <span class="despesa-dot"
            style="background-color:
            ${data.categoria_cor || "#8FEBDD"};">
        </span>

        <span class="despesa-data">
            ${escapeHtml(data.data.slice(0, 5))}
        </span>

        <span id="desc-${data.id}">
            ${escapeHtml(data.descricao)}
        </span>

        <span class="despesa-categoria">
            ${escapeHtml(data.categoria)}
        </span>

        <span class="despesa-conta">
            ${escapeHtml(data.conta || "-")}
        </span>

        <span class="despesa-parcelada">
            ${badgeStatus(data.parcelada)}
        </span>

        <span class="despesa-parcelas">
            ${data.quantidade_parcelas || "-"}
        </span>

        <span class="despesa-recorrente">
            ${badgeStatus(data.recorrente)}
        </span>

        <span id="valor-${data.id}">
            ${formatarMoeda(data.valor)}
        </span>

        <span class="despesa-actions">

            <button type="button"
                onclick="editarDespesa(${data.id})"
                aria-label="Editar ${escapeHtml(data.descricao)}">

                <img src="${editarIcon}" alt="">
            </button>

            <button type="button"
                onclick="excluirDespesa(${data.id})"
                aria-label="Excluir ${escapeHtml(data.descricao)}">

                <img src="${lixeiraIcon}" alt="">
            </button>

        </span>
    `;
}


// APLICA DADOS NO DATASET DA LINHA
function aplicarDatasetDespesa(row, data) {

    row.dataset.id = data.id;

    row.dataset.descricao = data.descricao;

    row.dataset.valor = data.valor;

    row.dataset.data = data.data_iso;

    row.dataset.categoriaId =
        data.categoria_id || "";

    row.dataset.categoria = data.categoria;

    row.dataset.categoriaCor =
        data.categoria_cor || "#8FEBDD";

    row.dataset.conta =
        data.conta || "";

    row.dataset.recorrente =
        data.recorrente ? "true" : "false";

    row.dataset.parcelada =
        data.parcelada ? "true" : "false";

    row.dataset.quantidadeParcelas =
        data.quantidade_parcelas || "";
}


// ADICIONA NOVA LINHA DE DESPESA
function adicionarLinhaDespesa(data) {

    const tabela = document.getElementById(
        "tabelaDespesas"
    );

    const vazio = document.getElementById(
        "semDespesas"
    );

    // Remove mensagem vazia
    if (vazio) vazio.remove();

    // Cria linha
    const row = document.createElement("div");

    row.className = "despesa-row fade-in";

    row.id = `linha-${data.id}`;

    aplicarDatasetDespesa(row, data);

    row.innerHTML = linhaDespesaHtml(data);

    tabela.appendChild(row);
}


// ATUALIZA LINHA EXISTENTE
function atualizarLinhaDespesa(data) {

    const row = document.getElementById(
        `linha-${data.id}`
    );

    if (!row) return;

    aplicarDatasetDespesa(row, data);

    row.innerHTML = linhaDespesaHtml(data);
}


// ABRE MODAL PARA EDICAO
function editarDespesa(id) {

    const row = document.getElementById(
        `linha-${id}`
    );

    if (!row) return;

    abrirModalDespesa({

        id,

        descricao: row.dataset.descricao,

        valor: row.dataset.valor,

        data: row.dataset.data,

        categoriaId: row.dataset.categoriaId,

        conta: row.dataset.conta,

        recorrente: row.dataset.recorrente,

        parcelada: row.dataset.parcelada,

        quantidadeParcelas:
            row.dataset.quantidadeParcelas,
    });
}


// EXCLUI DESPESA
function excluirDespesa(id) {

    // Confirma exclusao
    if (!confirm(
        "Deseja excluir esta despesa?"
    )) return;

    const row = document.getElementById(
        `linha-${id}`
    );

    // Valor atual da despesa
    const valorAtual = parseNumero(
        row?.dataset.valor || 0
    );

    // REQUISICAO DE EXCLUSAO
    fetch(`/despesas/excluir/${id}/`, {

        method: "POST",

        headers: {
            "X-CSRFToken": getCSRFToken()
        },
    })

    .then((res) => res.json())

    .then((data) => {

        // Erro da API
        if (!data.success) {

            alert(
                data.error || "Erro ao excluir despesa"
            );

            return;
        }

        // Remove linha
        row?.remove();

        atualizarTotalDespesa(-valorAtual);

        verificarTabelaVazia();
    })

    .catch(() => alert("Erro ao excluir despesa"));
}


// VERIFICA TABELA VAZIA
function verificarTabelaVazia() {

    const tabela = document.getElementById(
        "tabelaDespesas"
    );

    // Se ainda existem itens nao faz nada
    if (!tabela || tabela.children.length > 0)
        return;

    // Cria mensagem vazia
    const empty = document.createElement("p");

    empty.className = "despesas-empty";

    empty.id = "semDespesas";

    empty.innerText =
        "Nenhuma despesa cadastrada neste mes";

    tabela.appendChild(empty);
}


// ATUALIZA TOTAL DAS DESPESAS
function atualizarTotalDespesa(delta) {

    const total = document.getElementById(
        "totalDespesasMes"
    );

    // Valor atual exibido
    const valorAtual = extrairValor(
        total.innerText
    );

    // Atualiza valor total
    total.innerText = formatarMoeda(
        Math.max(0, valorAtual + delta)
    );
}


// EXTRAI VALOR MONETARIO
function extrairValor(valor) {

    return Number(

        String(valor)

            .replace("R$", "")

            .replace(/\./g, "")

            .replace(",", ".")

            .trim()

    ) || 0;
}


// NORMALIZA VALOR NUMERICO
function normalizarNumero(valor) {

    return String(valor || "")
        .replace(",", ".");
}


// CONVERTE PARA NUMERO
function parseNumero(valor) {

    return Number(
        normalizarNumero(valor)
    ) || 0;
}


// FORMATA VALOR MONETARIO
function formatarMoeda(valor) {

    return Number(valor || 0).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL",
        }
    );
}


// GERA BADGE DE STATUS
function badgeStatus(ativo) {

    return `
        <span class="status-badge
            ${ativo ? "is-on" : "is-off"}">

            ${ativo ? "Sim" : "Nao"}

        </span>
    `;
}


// PROTEGE HTML CONTRA CARACTERES ESPECIAIS
function escapeHtml(valor) {

    return String(valor ?? "")

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");
}


function mostrarMensagemSucesso(texto) {

    const anterior = document.querySelector(".app-toast");

    if (anterior)
        anterior.remove();

    const toast = document.createElement("div");

    toast.className = "app-toast";
    toast.innerText = texto;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("is-visible");
    }, 20);

    setTimeout(() => {
        toast.classList.remove("is-visible");
        setTimeout(() => toast.remove(), 250);
    }, 2600);
}

