// Controla a receita que esta em edicao
let receitaEmEdicao = null;

// Este arquivo controla o popup, a tabela e as requisicoes AJAX de receitas.


// OBTEM TOKEN CSRF DO DJANGO
function getCSRFToken() {

    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    )?.value || "";
}


// EXECUTA APOS CARREGAR A PAGINA
document.addEventListener("DOMContentLoaded", function () {

    // FORMULARIO DE RECEITA
    const formReceita = document.getElementById(
        "formReceita"
    );

    // CAMPOS DE PARCELAMENTO
    const parcelada = document.getElementById(
        "receitaParcelada"
    );

    const recorrente = formReceita?.elements.recorrente;

    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelasReceita"
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

            atualizarTravamentoReceita();
        });
    }

    if (recorrente) {

        recorrente.addEventListener("change", atualizarTravamentoReceita);
    }


    // Verifica existencia do formulario
    if (!formReceita) return;


    // ENVIO DO FORMULARIO
    formReceita.addEventListener("submit", function (e) {

        e.preventDefault();

        // Dados do formulario
        const formData = new FormData(this);

        const editando = Boolean(receitaEmEdicao);

        // Botao de envio
        const btn = formReceita.querySelector(
            'button[type="submit"]'
        );

        // Icones configuraveis
        const icons = typeof RECEITA_ICONS !== "undefined"

            ? RECEITA_ICONS

            : {};

        // URL DE CRIACAO
        const urlCriar = typeof URL_CRIAR_RECEITA !== "undefined"

            ? URL_CRIAR_RECEITA

            : "/receitas/criar/";

        // URL DE EDICAO
        const urlEditar = `${
            typeof RECEITA_URL_EDITAR_BASE !== "undefined"

                ? RECEITA_URL_EDITAR_BASE

                : "/receitas/editar/"
        }${receitaEmEdicao}/`;

        // Desabilita botao durante envio
        btn.disabled = true;

        btn.innerText = "Salvando...";


        // REQUISICAO PARA API
        fetch(receitaEmEdicao ? urlEditar : urlCriar, {

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
                    data.error || "Erro ao salvar receita"
                );

                return;
            }

            // Mes atual exibido na tela
            const mesAtual = typeof RECEITA_MES_ATUAL !== "undefined"

                ? RECEITA_MES_ATUAL

                : "";

            // Busca linha existente
            const linhaExistente = document.getElementById(
                `linha-${data.id}`
            );

            // Valor anterior da receita
            const valorAnterior = linhaExistente

                ? parseNumero(
                    linhaExistente.dataset.valor || 0
                )

                : 0;


            // Atualiza tabela caso receita pertenca ao mes atual
            if (data.data_iso.startsWith(mesAtual)) {

                // Atualiza linha existente
                if (linhaExistente) {

                    atualizarLinhaReceita(data);

                    atualizarTotalReceita(
                        parseNumero(data.valor)
                        - valorAnterior
                    );

                } else {

                    // Cria nova linha
                    adicionarLinhaReceita(data);

                    atualizarTotalReceita(
                        parseNumero(data.valor)
                    );
                }

            // Remove linha caso receita tenha mudado de mes
            } else if (linhaExistente) {

                linhaExistente.remove();

                atualizarTotalReceita(-valorAnterior);

                verificarTabelaVazia();
            }

            // Fecha modal
            fecharModalReceita();

            if (!editando) {

                mostrarMensagemSucesso(
                    "Receita adicionada com sucesso!"
                );
            }
        })

        // Captura erros
        .catch(() => alert("Erro ao salvar receita"))

        // Reativa botao
        .finally(() => {

            btn.disabled = false;

            btn.innerHTML = `
                <img src="${
                    icons.check
                    || "/static/financeiro/img/check.png"
                }" alt="">

                Salvar
            `;
        });
    });
});


function atualizarTravamentoReceita() {

    const form = document.getElementById("formReceita");
    const parcelada = document.getElementById("receitaParcelada");
    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelasReceita"
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


// ABRE MODAL DE RECEITA
function abrirModalReceita(dados = null) {

    // ELEMENTOS DO MODAL
    const modal = document.getElementById(
        "modalReceita"
    );

    const form = document.getElementById(
        "formReceita"
    );

    const titulo = document.getElementById(
        "modalReceitaTitulo"
    );

    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelasReceita"
    );

    // Define receita em edicao
    receitaEmEdicao = dados?.id || null;

    // Reseta formulario
    form.reset();

    // Define titulo do modal
    titulo.innerText = receitaEmEdicao

        ? "Editar Receita"

        : "Adicionar Receita";


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

        // Desabilita campo de parcelas
        quantidadeParcelas.disabled = true;

        quantidadeParcelas.required = false;
    }

    atualizarTravamentoReceita();

    // Abre modal
    modal.classList.remove("is-closing");

    modal.classList.add("is-open");

    modal.setAttribute("aria-hidden", "false");

    // Foca no campo valor
    setTimeout(() => {

        document.getElementById(
            "valorReceita"
        )?.focus();

    }, 80);
}


// FECHA MODAL
function fecharModalReceita() {

    const modal = document.getElementById(
        "modalReceita"
    );

    const form = document.getElementById(
        "formReceita"
    );

    const quantidadeParcelas = document.getElementById(
        "quantidadeParcelasReceita"
    );

    // Limpa edicao atual
    receitaEmEdicao = null;

    // Reseta formulario
    form.reset();

    // Define titulo padrao
    document.getElementById(
        "modalReceitaTitulo"
    ).innerText = "Adicionar Receita";

    // Desabilita campo de parcelas
    if (quantidadeParcelas) {

        quantidadeParcelas.disabled = true;

        quantidadeParcelas.required = false;
    }

    atualizarTravamentoReceita();

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


// GERA HTML DA LINHA DE RECEITA
function linhaReceitaHtml(data) {

    // ICONES PADRAO
    const icons = typeof RECEITA_ICONS !== "undefined"

        ? RECEITA_ICONS

        : {};

    const editarIcon =
        icons.editar
        || "/static/financeiro/img/editar.png";

    const lixeiraIcon =
        icons.lixeira
        || "/static/financeiro/img/lixeira.png";

    return `
        <span class="receita-dot"
            style="background-color:
            ${data.categoria_cor || "#8FEBDD"};">
        </span>

        <span class="receita-data">
            ${escapeHtml(data.data.slice(0, 5))}
        </span>

        <span id="desc-${data.id}">
            ${escapeHtml(data.descricao)}
        </span>

        <span class="receita-categoria">
            ${escapeHtml(data.categoria)}
        </span>

        <span class="receita-recorrente">
            ${badgeStatus(data.recorrente)}
        </span>

        <span class="receita-parcelada">
            ${badgeStatus(data.parcelada)}
        </span>

        <span class="receita-parcelas">
            ${data.quantidade_parcelas || "-"}
        </span>

        <span id="valor-${data.id}">
            ${formatarMoeda(data.valor)}
        </span>

        <span class="receita-actions">

            <button type="button"
                onclick="editarReceita(${data.id})"
                aria-label="Editar ${escapeHtml(data.descricao)}">

                <img src="${editarIcon}" alt="">
            </button>

            <button type="button"
                onclick="excluirReceita(${data.id})"
                aria-label="Excluir ${escapeHtml(data.descricao)}">

                <img src="${lixeiraIcon}" alt="">
            </button>

        </span>
    `;
}


// APLICA DADOS NO DATASET DA LINHA
function aplicarDatasetReceita(row, data) {

    row.dataset.id = data.id;

    row.dataset.descricao = data.descricao;

    row.dataset.valor = data.valor;

    row.dataset.data = data.data_iso;

    row.dataset.categoriaId =
        data.categoria_id || "";

    row.dataset.categoria = data.categoria;

    row.dataset.categoriaCor =
        data.categoria_cor || "#8FEBDD";

    row.dataset.recorrente =
        data.recorrente ? "true" : "false";

    row.dataset.parcelada =
        data.parcelada ? "true" : "false";

    row.dataset.quantidadeParcelas =
        data.quantidade_parcelas || "";
}


// ADICIONA NOVA LINHA DE RECEITA
function adicionarLinhaReceita(data) {

    const tabela = document.getElementById(
        "tabelaReceitas"
    );

    const vazio = document.getElementById(
        "semReceitas"
    );

    // Remove mensagem vazia
    if (vazio) vazio.remove();

    // Cria linha
    const row = document.createElement("div");

    row.className = "receita-row fade-in";

    row.id = `linha-${data.id}`;

    aplicarDatasetReceita(row, data);

    row.innerHTML = linhaReceitaHtml(data);

    tabela.appendChild(row);
}


// ATUALIZA LINHA EXISTENTE
function atualizarLinhaReceita(data) {

    const row = document.getElementById(
        `linha-${data.id}`
    );

    if (!row) return;

    aplicarDatasetReceita(row, data);

    row.innerHTML = linhaReceitaHtml(data);
}


// ABRE MODAL PARA EDICAO
function editarReceita(id) {

    const row = document.getElementById(
        `linha-${id}`
    );

    if (!row) return;

    abrirModalReceita({

        id,

        descricao: row.dataset.descricao,

        valor: row.dataset.valor,

        data: row.dataset.data,

        categoriaId: row.dataset.categoriaId,

        recorrente: row.dataset.recorrente,

        parcelada: row.dataset.parcelada,

        quantidadeParcelas:
            row.dataset.quantidadeParcelas,
    });
}


// EXCLUI RECEITA
function excluirReceita(id) {

    // Confirma exclusao
    if (!confirm(
        "Deseja excluir esta receita?"
    )) return;

    const row = document.getElementById(
        `linha-${id}`
    );

    // Valor atual da receita
    const valorAtual = parseNumero(
        row?.dataset.valor || 0
    );

    // REQUISICAO DE EXCLUSAO
    fetch(`/receitas/excluir/${id}/`, {

        method: "POST",

        headers: {
            "X-CSRFToken": getCSRFToken()
        },
    })

    .then((res) => res.json())

    .then((data) => {

        // Erro retornado pela API
        if (!data.success) {

            alert(
                data.error || "Erro ao excluir receita"
            );

            return;
        }

        // Remove linha
        row?.remove();

        atualizarTotalReceita(-valorAtual);

        verificarTabelaVazia();
    })

    .catch(() => alert("Erro ao excluir receita"));
}


// VERIFICA TABELA VAZIA
function verificarTabelaVazia() {

    const tabela = document.getElementById(
        "tabelaReceitas"
    );

    // Se ainda existem itens nao faz nada
    if (!tabela || tabela.children.length > 0)
        return;

    // Cria mensagem vazia
    const empty = document.createElement("p");

    empty.className = "receitas-empty";

    empty.id = "semReceitas";

    empty.innerText =
        "Nenhuma receita cadastrada neste mes";

    tabela.appendChild(empty);
}


// ATUALIZA TOTAL DAS RECEITAS
function atualizarTotalReceita(delta) {

    const total = document.getElementById(
        "totalReceitasMes"
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

