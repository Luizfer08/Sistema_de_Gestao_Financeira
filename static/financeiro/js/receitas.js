// TOGGLE
function toggleFormReceita(){
    const form = document.getElementById("formReceitaContainer");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

// CSRF
function getCSRFToken(){
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// CRIAR
document.getElementById("formReceita").addEventListener("submit", function(e){
    e.preventDefault();

    const formData = new FormData(this);
    const tabela = document.getElementById("tabelaReceitas");

    fetch("/receitas/criar/", {
        method: "POST",
        headers: {"X-CSRFToken": getCSRFToken()},
        body: formData
    })
    .then(res => res.json())
    .then(data => {

    if(data.success){

        const novaLinha = document.createElement("tr");
        novaLinha.id = `linha-${data.id}`;
        novaLinha.classList.add("fade-in");

        novaLinha.innerHTML = `
            <td id="desc-${data.id}">${data.descricao}</td>
            <td id="valor-${data.id}">R$ ${parseFloat(data.valor).toFixed(2)}</td>
            <td>${data.categoria}</td>
            <td>${data.data}</td>
            <td>
                ${data.recorrente 
                    ? '<span class="badge bg-success">Sim</span>' 
                    : '<span class="badge bg-secondary">Não</span>'}
            </td>
            <td>
                <button onclick="editarReceita(${data.id})" class="btn btn-warning btn-sm">Editar</button>
                <button onclick="excluirReceita(${data.id})" class="btn btn-danger btn-sm">Excluir</button>
            </td>
        `;

        tabela.appendChild(novaLinha);

        document.getElementById("formReceita").reset();
        toggleFormReceita();

        } else {
            alert(data.error);
        }

    });
});


// EDITAR
function editarReceita(id){

    const desc = document.getElementById(`desc-${id}`);
    const valor = document.getElementById(`valor-${id}`);

    const descOriginal = desc.innerText;
    const valorOriginal = valor.innerText;

    desc.innerHTML = `<input id="input-desc-${id}" value="${descOriginal}" class="form-control">`;

    const valorLimpo = valorOriginal
        .replace('R$', '')
        .replace(/\./g, '')
        .replace(',', '.')
        .trim();

    valor.innerHTML = `<input id="input-valor-${id}" value="${valorLimpo}" class="form-control">`;

    const tdAcoes = document.getElementById(`linha-${id}`).querySelector("td:last-child");

    tdAcoes.innerHTML = `
        <button onclick="salvarReceita(${id})" class="btn btn-success btn-sm">Salvar</button>
        <button onclick="cancelarEdicaoReceita(${id}, '${descOriginal}', '${valorOriginal}')" class="btn btn-secondary btn-sm">
            Cancelar
        </button>
    `;
}


// CANCELAR
function cancelarEdicaoReceita(id, descOriginal, valorOriginal){

    document.getElementById(`desc-${id}`).innerText = descOriginal;
    document.getElementById(`valor-${id}`).innerText = valorOriginal;

    restaurarBotoesReceita(id);
}


// RESTAURAR BOTÕES
function restaurarBotoesReceita(id){

    const linha = document.getElementById(`linha-${id}`);
    const tdAcoes = linha.querySelector("td:last-child");

    tdAcoes.innerHTML = `
        <button onclick="editarReceita(${id})" class="btn btn-warning btn-sm">Editar</button>
        <button onclick="excluirReceita(${id})" class="btn btn-danger btn-sm">Excluir</button>
    `;
}


// SALVAR
function salvarReceita(id){

    const descricao = document.getElementById(`input-desc-${id}`).value;
    let valor = document.getElementById(`input-valor-${id}`).value;
    valor = valor.replace(',', '.');

    fetch(`/receitas/editar/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `descricao=${descricao}&valor=${valor}`
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            const valorFormatado = `R$ ${parseFloat(data.valor).toFixed(2)}`;

            document.getElementById(`desc-${id}`).innerText = data.descricao;
            document.getElementById(`valor-${id}`).innerText = valorFormatado;

            cancelarEdicaoReceita(id, data.descricao, valorFormatado);

        } else {
            alert(data.error);
        }

    });
}


// EXCLUIR
function excluirReceita(id){

    if(!confirm("Deseja excluir esta receita?")) return;

    fetch(`/receitas/excluir/${id}/`, {
        method: "POST",
        headers: {"X-CSRFToken": getCSRFToken()}
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            const linha = document.getElementById(`linha-${id}`);
            linha.classList.add("fade-out");

            setTimeout(() => linha.remove(), 200);

        } else {
            alert(data.error);
        }

    });
}