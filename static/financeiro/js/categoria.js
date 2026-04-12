// TOGGLE 
function toggleForm() {
    const form = document.getElementById('containerFormCategoria');

    if (form.style.display === 'none') {
        form.style.display = 'block';
        form.classList.add('fade-in');
    } else {
        form.classList.add('fade-out');

        setTimeout(() => {
            form.style.display = 'none';
            form.classList.remove('fade-out');
        }, 200);
    }
}

// CSRF
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// CRIAR (AJAX)
document.getElementById('formCategoria').addEventListener('submit', function(e) {
    e.preventDefault();

    const nome = document.getElementById('nomeCategoria').value;
    const tabela = document.getElementById('tabelaCategorias');

    fetch("{% url 'financeiro:criar_categoria' %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `nome=${nome}`
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

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

            document.getElementById('nomeCategoria').value = "";
            toggleForm();

        } else {
            alert(data.error);
        }

    });
});


// EDITAR INLINE
function editarInline(id){

    const td = document.getElementById(`nome-${id}`);
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


// SALVAR EDIÇÃO
function salvarEdicao(id){

    const novoNome = document.getElementById(`input-${id}`).value;

    fetch(`/categorias/editar/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `nome=${novoNome}`
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            const td = document.getElementById(`nome-${id}`);
            td.classList.add('fade-in');
            td.innerText = data.nome;

            restaurarBotoes(id);

        } else {
            alert(data.error);
        }

    });
}


// CANCELAR
function cancelarEdicao(id, nomeOriginal){

    document.getElementById(`nome-${id}`).innerText = nomeOriginal;

    restaurarBotoes(id);
}


// RESTAURAR BOTÕES
function restaurarBotoes(id){

    const linha = document.getElementById(`linha-${id}`);
    const botoes = linha.querySelector('td:last-child');

    botoes.innerHTML = `
        <button class="btn btn-warning btn-sm" onclick="editarInline(${id})">
            Editar
        </button>
        <button class="btn btn-danger btn-sm" onclick="excluirCategoria(${id})"">
            Excluir
        </button>
    `;
}

// EXCLUIR 
function excluirCategoria(id){

    if(!confirm("Deseja realmente excluir esta categoria?")){
        return;
    }

    fetch(`/categorias/excluir/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        }
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            const linha = document.getElementById(`linha-${id}`);

            // ANIMAÇÃO DE SAÍDA
            linha.classList.add('fade-out');

            setTimeout(() => {
                linha.remove();
            }, 200);

        } else {
            alert(data.error);
        }

    });
}
