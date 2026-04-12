// CONFIG
const URL_CRIAR = typeof URL_CRIAR_CATEGORIA !== "undefined"
    ? URL_CRIAR_CATEGORIA
    : "/categorias/criar/";


// INIT
document.addEventListener("DOMContentLoaded", function(){

    console.log("Categoria.js carregado");

    // TOGGLE FORM
    window.toggleForm = function () {
        const form = document.getElementById('containerFormCategoria');

        if (!form) return;

        if (form.style.display === 'none' || form.style.display === '') {
            form.style.display = 'block';
            form.classList.add('fade-in');

            setTimeout(() => {
                const input = document.getElementById('nomeCategoria');
                if (input) input.focus();
            }, 100);

        } else {
            form.classList.add('fade-out');

            setTimeout(() => {
                form.style.display = 'none';
                form.classList.remove('fade-out');
            }, 200);
        }
    };


    // CSRF
    function getCSRFToken() {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : '';
    }


    // CRIAR
    const formCategoria = document.getElementById('formCategoria');

    if (!formCategoria) {
        console.warn("FormCategoria não encontrado");
        return;
    }

    formCategoria.addEventListener('submit', function(e){
        e.preventDefault();

        const nomeInput = document.getElementById('nomeCategoria');
        const tabela = document.getElementById('tabelaCategorias');
        const btn = formCategoria.querySelector('button[type="submit"]');

        if (!nomeInput || !tabela) {
            console.warn("Elementos não encontrados");
            return;
        }

        const nome = nomeInput.value.trim();

        if (!nome) {
            alert("Digite o nome da categoria");
            return;
        }

        // 🔥 LOADING BUTTON
        btn.disabled = true;
        btn.innerText = "Salvando...";

        fetch(URL_CRIAR, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `nome=${encodeURIComponent(nome)}`
        })
        .then(res => {
            if (!res.ok) throw new Error("Erro na requisição");
            return res.json();
        })
        .then(data => {

            if (data.success) {

                const vazio = document.getElementById("semCategorias");
                if (vazio) vazio.remove();

                const novaLinha = document.createElement("tr");
                novaLinha.id = `linha-${data.id}`;
                novaLinha.classList.add("fade-in");

                novaLinha.innerHTML = `
                    <td id="nome-${data.id}">${data.nome}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="editarInline(${data.id})">
                            Editar
                        </button>
                        <button class="btn btn-danger btn-sm" onclick="excluirCategoria(${data.id})">
                            Excluir
                        </button>
                    </td>
                `;

                tabela.appendChild(novaLinha);

                nomeInput.value = "";
                window.toggleForm();

            } else {
                alert(data.error || "Erro ao criar categoria");
            }

        })
        .catch((err) => {
            console.error(err);
            alert("Erro ao salvar categoria");
        })
        .finally(() => {
            btn.disabled = false;
            btn.innerText = "Salvar";
        });
    });

});


// EDITAR
function editarInline(id){

    const td = document.getElementById(`nome-${id}`);
    if (!td) return;

    const nomeAtual = td.innerText;

    td.innerHTML = `
        <input type="text" id="input-${id}" value="${nomeAtual}" class="form-control">
    `;

    const linha = document.getElementById(`linha-${id}`);
    const botoes = linha.querySelector('td:last-child');

    botoes.innerHTML = `
        <button class="btn btn-success btn-sm" onclick="salvarEdicao(${id})">
            Salvar
        </button>
        <button class="btn btn-secondary btn-sm" onclick="cancelarEdicao(${id}, '${nomeAtual}')">
            Cancelar
        </button>
    `;
}


// SALVAR
function salvarEdicao(id){

    const input = document.getElementById(`input-${id}`);
    if (!input) return;

    const novoNome = input.value.trim();

    if (!novoNome) {
        alert("Nome não pode ser vazio");
        return;
    }

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    fetch(`/categorias/editar/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `nome=${encodeURIComponent(novoNome)}`
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            const td = document.getElementById(`nome-${id}`);
            td.innerText = data.nome;

            restaurarBotoes(id);

        } else {
            alert(data.error || "Erro ao editar");
        }

    })
    .catch(() => {
        alert("Erro ao editar categoria");
    });
}


// CANCELAR
function cancelarEdicao(id, nomeOriginal){

    const td = document.getElementById(`nome-${id}`);
    if (td) td.innerText = nomeOriginal;

    restaurarBotoes(id);
}


// RESTAURAR BOTÕES
function restaurarBotoes(id){

    const linha = document.getElementById(`linha-${id}`);
    if (!linha) return;

    const botoes = linha.querySelector('td:last-child');

    botoes.innerHTML = `
        <button class="btn btn-warning btn-sm" onclick="editarInline(${id})">
            Editar
        </button>
        <button class="btn btn-danger btn-sm" onclick="excluirCategoria(${id})">
            Excluir
        </button>
    `;
}


// EXCLUIR
function excluirCategoria(id){

    if(!confirm("Deseja realmente excluir esta categoria?")) return;

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    fetch(`/categorias/excluir/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf,
        }
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            const linha = document.getElementById(`linha-${id}`);

            if (linha){
                linha.classList.add('fade-out');

                setTimeout(() => {
                    linha.remove();
                }, 200);
            }

            const tabela = document.getElementById("tabelaCategorias");
            if (tabela.children.length === 0) {

                const tr = document.createElement("tr");
                tr.id = "semCategorias";

                tr.innerHTML = `
                    <td colspan="2" class="text-center text-muted">
                        Nenhuma categoria cadastrada
                    </td>
                `;

                tabela.appendChild(tr);
            }

        } else {
            alert(data.error || "Erro ao excluir");
        }

    })
    .catch(() => {
        alert("Erro ao excluir categoria");
    });
}