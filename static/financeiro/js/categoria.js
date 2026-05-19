// URL PADRÃO PARA CRIAÇÃO DE CATEGORIAS
const URL_CRIAR = typeof URL_CRIAR_CATEGORIA !== "undefined"
    ? URL_CRIAR_CATEGORIA
    : "/categorias/criar/";


// LISTA DE CORES DISPONÍVEIS
const CORES_CATEGORIA = [
    "#8FEBDD", "#62BFF0", "#5A4226", "#FFA0A4", "#399886",
    "#858585", "#C7C7CD", "#08AF4A", "#594CF2", "#A30CE9", "#FEAB1B",
    "#E26CE1", "#99F69D", "#8D8D8D", "#FF073F", "#B775C5",
    "#918F5E", "#FFA5B5", "#FF7B00", "#1E29ED", "#18BEEA", "#F5D7B8",
];


// CONTROLA CATEGORIA EM EDIÇÃO
let categoriaEmEdicao = null;


// EXECUTA APÓS CARREGAR A PÁGINA
document.addEventListener("DOMContentLoaded", function () {

    // Monta paleta de cores
    montarPaleta();

    // FORMULÁRIO DE CATEGORIA
    const formCategoria = document.getElementById("formCategoria");

    if (!formCategoria) return;


    // ENVIO DO FORMULÁRIO
    formCategoria.addEventListener("submit", function (e) {

        e.preventDefault();

        // CAMPOS DO FORMULÁRIO
        const nomeInput = document.getElementById("nomeCategoria");

        const tipoInput = document.getElementById("tipoCategoria");

        const corInput = document.getElementById("corCategoria");

        const btn = formCategoria.querySelector(
            'button[type="submit"]'
        );

        // Nome digitado
        const nome = nomeInput.value.trim();

        // Valida nome obrigatório
        if (!nome) {

            alert("Digite o nome da categoria");

            return;
        }

        // Desabilita botão durante envio
        btn.disabled = true;
        btn.innerText = "Salvando...";

        // URL DE CRIAÇÃO OU EDIÇÃO
        const url = categoriaEmEdicao

            ? `/categorias/editar/${categoriaEmEdicao}/`

            : URL_CRIAR;

        // DADOS ENVIADOS
        const body = categoriaEmEdicao

            ? `nome=${encodeURIComponent(nome)}&cor=${encodeURIComponent(corInput.value)}`

            : `nome=${encodeURIComponent(nome)}&tipo=${encodeURIComponent(tipoInput.value)}&cor=${encodeURIComponent(corInput.value)}`;


        // REQUISIÇÃO PARA API
        fetch(url, {

            method: "POST",

            headers: {

                "X-CSRFToken": getCSRFToken(),

                "Content-Type": "application/x-www-form-urlencoded",
            },

            body,
        })

        // Valida resposta
        .then((res) => {

            if (!res.ok)
                throw new Error("Erro na requisicao");

            return res.json();
        })

        .then((data) => {

            // Erro retornado pela API
            if (!data.success) {

                alert(
                    data.error || "Erro ao salvar categoria"
                );

                return;
            }

            // EDITAR CATEGORIA
            if (categoriaEmEdicao) {

                atualizarLinhaCategoria(
                    categoriaEmEdicao,
                    data.nome,
                    data.cor
                );

            } else {

                // CRIAR NOVA CATEGORIA
                adicionarLinhaCategoria(data);

                atualizarTotal(1);
            }

            // Fecha modal
            fecharModalCategoria();
        })

        // Captura erros
        .catch(() => alert("Erro ao salvar categoria"))

        // Reativa botão
        .finally(() => {

            btn.disabled = false;

            btn.innerText = "Salvar";
        });
    });
});


// OBTÉM TOKEN CSRF DO DJANGO
function getCSRFToken() {

    return document.querySelector(
        "[name=csrfmiddlewaretoken]"
    )?.value || "";
}


// MONTA PALETA DE CORES
function montarPaleta() {

    const container = document.getElementById(
        "coresCategoria"
    );

    if (!container) return;

    // Gera botões de cores
    container.innerHTML = CORES_CATEGORIA.map((cor, index) => `

        <button
            class="categoria-color ${index === 0 ? "is-selected" : ""}"
            type="button"
            style="background-color: ${cor};"
            data-cor="${cor}"
            aria-label="Selecionar cor ${cor}">
        </button>

    `).join("");

    // Evento de seleção das cores
    container.querySelectorAll(".categoria-color").forEach((btn) => {

        btn.addEventListener("click", function () {

            selecionarCor(this.dataset.cor);
        });
    });
}


// DEFINE COR SELECIONADA
function selecionarCor(cor) {

    // Atualiza input oculto
    document.getElementById(
        "corCategoria"
    ).value = cor;

    // Atualiza estado visual
    document.querySelectorAll(".categoria-color").forEach((btn) => {

        btn.classList.toggle(
            "is-selected",
            btn.dataset.cor === cor
        );
    });
}


// ABRE MODAL DE CATEGORIA
function abrirModalCategoria(tipo, categoria = null) {

    // Define categoria em edição
    categoriaEmEdicao = categoria?.id || null;

    // ELEMENTOS DO MODAL
    const modal = document.getElementById("modalCategoria");

    const titulo = document.getElementById(
        "modalCategoriaTitulo"
    );

    const nomeInput = document.getElementById(
        "nomeCategoria"
    );

    const tipoInput = document.getElementById(
        "tipoCategoria"
    );

    // Define título do modal
    titulo.innerText = categoriaEmEdicao

        ? "Editar categoria"

        : "Adicionar categoria";

    // Preenche dados
    nomeInput.value = categoria?.nome || "";

    tipoInput.value = tipo;

    selecionarCor(
        categoria?.cor || "#8FEBDD"
    );

    // Abre modal
    modal.classList.remove("is-closing");

    modal.classList.add("is-open");

    modal.setAttribute("aria-hidden", "false");

    // Foca no input
    setTimeout(() => nomeInput.focus(), 80);
}


// FECHA MODAL
function fecharModalCategoria() {

    const modal = document.getElementById(
        "modalCategoria"
    );

    const form = document.getElementById(
        "formCategoria"
    );

    // Limpa edição atual
    categoriaEmEdicao = null;

    // Reseta formulário
    form.reset();

    selecionarCor("#8FEBDD");

    modal.setAttribute("aria-hidden", "true");

    fecharModalComAnimacao(modal);
}


// FECHA MODAL COM ANIMAÇÃO
function fecharModalComAnimacao(modal) {

    modal.classList.remove("is-open");

    modal.classList.add("is-closing");

    setTimeout(() => {

        modal.classList.remove("is-closing");

    }, 280);
}


// ADICIONA NOVA LINHA DE CATEGORIA
function adicionarLinhaCategoria(data) {

    const lista = document.getElementById(
        `lista-${data.tipo}`
    );

    const vazio = document.getElementById(
        `empty-${data.tipo}`
    );

    // Remove mensagem vazia
    if (vazio) vazio.remove();

    // Cria linha da categoria
    const row = document.createElement("div");

    row.className = "categoria-row fade-in";

    row.id = `categoria-${data.id}`;

    row.dataset.tipo = data.tipo;

    row.innerHTML = linhaCategoriaHtml(
        data.id,
        data.nome,
        data.cor
    );

    lista.appendChild(row);
}


// ATUALIZA LINHA EXISTENTE
function atualizarLinhaCategoria(id, nome, cor) {

    const row = document.getElementById(
        `categoria-${id}`
    );

    if (!row) return;

    // Atualiza cor
    row.querySelector(
        ".categoria-dot"
    ).style.backgroundColor = cor;

    // Atualiza nome
    row.querySelector(
        ".categoria-name"
    ).innerText = nome;
}


// GERA HTML DA LINHA DA CATEGORIA
function linhaCategoriaHtml(id, nome, cor) {

    // Protege HTML contra caracteres especiais
    const nomeSeguro = escapeHtml(nome);

    // Ícones padrão
    const icons = typeof CATEGORIA_ICONS !== "undefined"
        ? CATEGORIA_ICONS
        : {};

    const editarIcon =
        icons.editar || "/static/financeiro/img/editar.png";

    const lixeiraIcon =
        icons.lixeira || "/static/financeiro/img/lixeira.png";

    return `
        <span class="categoria-dot" style="background-color: ${cor};"></span>

        <span class="categoria-name" id="nome-${id}">
            ${nomeSeguro}
        </span>

        <button class="categoria-icon-btn"
            type="button"
            onclick="editarCategoria(${id})"
            aria-label="Editar ${nomeSeguro}">

            <img src="${editarIcon}" alt="">
        </button>

        <button class="categoria-icon-btn"
            type="button"
            onclick="excluirCategoria(${id})"
            aria-label="Excluir ${nomeSeguro}">

            <img src="${lixeiraIcon}" alt="">
        </button>
    `;
}


// ABRE MODAL PARA EDIÇÃO
function editarCategoria(id) {

    const row = document.getElementById(
        `categoria-${id}`
    );

    if (!row) return;

    // Dados atuais
    const nome = row.querySelector(
        ".categoria-name"
    ).innerText;

    const cor = rgbParaHex(
        row.querySelector(
            ".categoria-dot"
        ).style.backgroundColor
    );

    // Abre modal preenchido
    abrirModalCategoria(
        row.dataset.tipo,
        { id, nome, cor }
    );
}


// EXCLUI CATEGORIA
function excluirCategoria(id) {

    // Confirma exclusão
    if (!confirm(
        "Deseja realmente excluir esta categoria?"
    )) return;

    // REQUISIÇÃO DE EXCLUSÃO
    fetch(`/categorias/excluir/${id}/`, {

        method: "POST",

        headers: {
            "X-CSRFToken": getCSRFToken()
        },
    })

    .then((res) => res.json())

    .then((data) => {

        // Erro da API
        if (!data.success) {

            alert(data.error || "Erro ao excluir");

            return;
        }

        // Remove linha da tela
        const row = document.getElementById(
            `categoria-${id}`
        );

        const tipo = row?.dataset.tipo;

        row?.remove();

        atualizarTotal(-1);

        verificarListaVazia(tipo);
    })

    .catch(() => alert("Erro ao excluir categoria"));
}


// VERIFICA LISTA VAZIA
function verificarListaVazia(tipo) {

    if (!tipo) return;

    const lista = document.getElementById(
        `lista-${tipo}`
    );

    // Se ainda existem itens não faz nada
    if (!lista || lista.children.length > 0)
        return;

    // Cria mensagem vazia
    const empty = document.createElement("p");

    empty.className = "categoria-empty";

    empty.id = `empty-${tipo}`;

    empty.innerText = "Nenhuma categoria cadastrada";

    lista.appendChild(empty);
}


// ATUALIZA TOTAL DE CATEGORIAS
function atualizarTotal(delta) {

    const total = document.getElementById(
        "totalCategorias"
    );

    total.innerText = Math.max(
        0,
        Number(total.innerText || 0) + delta
    );
}


// CONVERTE RGB PARA HEXADECIMAL
function rgbParaHex(valor) {

    // Se já estiver em HEX retorna valor
    if (!valor || valor.startsWith("#"))
        return valor || "#8FEBDD";

    const partes = valor.match(/\d+/g);

    if (!partes)
        return "#8FEBDD";

    // Converte RGB para HEX
    return `#${partes.slice(0, 3).map((parte) => {

        const hex = Number(parte)
            .toString(16)
            .toUpperCase();

        return hex.padStart(2, "0");

    }).join("")}`;
}


// PROTEGE HTML CONTRA CARACTERES ESPECIAIS
function escapeHtml(valor) {

    return String(valor)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");
}