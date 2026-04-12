//  TOGGLE FORM 
function toggleFormDespesa(){
    const form = document.getElementById("formDespesaContainer");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

//  CSRF 
function getCSRFToken(){
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

//  CRIAR 
document.getElementById("formDespesa").addEventListener("submit", function(e){
    e.preventDefault();

    const formData = new FormData(this);
    const tabela = document.getElementById("tabelaDespesas");

    fetch("/despesas/criar/", {
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
                        ? '<span class="badge bg-danger">Sim</span>' 
                        : '<span class="badge bg-secondary">Não</span>'}
                </td>
                <td>
                    <button onclick="editarDespesa(${data.id})" class="btn btn-warning btn-sm">Editar</button>
                    <button onclick="excluirDespesa(${data.id})" class="btn btn-danger btn-sm">Excluir</button>
                </td>
            `;

            tabela.appendChild(novaLinha);

            document.getElementById("formDespesa").reset();
            toggleFormDespesa();

        } else {
            alert(data.error);
        }

    })
    .catch(() => {
        alert("Erro ao salvar despesa");
    });
});


//  EDITAR 
function editarDespesa(id){

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
        <button onclick="salvarDespesa(${id})" class="btn btn-success btn-sm">Salvar</button>
        <button onclick="cancelarEdicaoDespesa(${id}, '${descOriginal}', '${valorOriginal}')" class="btn btn-secondary btn-sm">
            Cancelar
        </button>
    `;
}


//  CANCELAR 
function cancelarEdicaoDespesa(id, descOriginal, valorOriginal){

    document.getElementById(`desc-${id}`).innerText = descOriginal;
    document.getElementById(`valor-${id}`).innerText = valorOriginal;

    const tdAcoes = document.getElementById(`linha-${id}`).querySelector("td:last-child");

    tdAcoes.innerHTML = `
        <button onclick="editarDespesa(${id})" class="btn btn-warning btn-sm">Editar</button>
        <button onclick="excluirDespesa(${id})" class="btn btn-danger btn-sm">Excluir</button>
    `;
}


//  SALVAR 
function salvarDespesa(id){

    const descricao = document.getElementById(`input-desc-${id}`).value;
    let valor = document.getElementById(`input-valor-${id}`).value;

    valor = valor.replace(',', '.');

    fetch(`/despesas/editar/${id}/`, {
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

            cancelarEdicaoDespesa(id, data.descricao, valorFormatado);

        } else {
            alert(data.error);
        }

    });
}


//  EXCLUIR 
function excluirDespesa(id){

    if(!confirm("Deseja excluir esta despesa?")) return;

    fetch(`/despesas/excluir/${id}/`, {
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