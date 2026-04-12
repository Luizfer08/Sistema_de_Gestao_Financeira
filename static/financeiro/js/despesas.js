function toggleFormDespesa(){
    const form = document.getElementById("formDespesaContainer");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

function getCSRFToken(){
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// CRIAR
document.getElementById("formDespesa").addEventListener("submit", function(e){
    e.preventDefault();

    const formData = new FormData(this);

    fetch("{% url 'financeiro:criar_despesa' %}", {
        method: "POST",
        headers: {"X-CSRFToken": getCSRFToken()},
        body: formData
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){
            location.reload();
        } else {
            alert(data.error);
        }

    });
});

// EDITAR
function editarDespesa(id){

    const desc = document.getElementById(`desc-${id}`);
    const valor = document.getElementById(`valor-${id}`);

    const descOriginal = desc.innerText;
    const valorOriginal = valor.innerText;

    desc.innerHTML = `<input id="input-desc-${id}" value="${descOriginal}" class="form-control">`;
    const valorLimpo = valorOriginal
    .replace('R$', '')
    .replace(/\./g, '')
    .replace(',', '.')      // troca vírgula por ponto
    .trim();

valor.innerHTML = `<input id="input-valor-${id}" value="${valorLimpo}" class="form-control">`;

    const tdAcoes = desc.parentElement.querySelector("td:last-child");

    tdAcoes.innerHTML = `
        <button onclick="salvarDespesa(${id})" class="btn btn-success btn-sm">Salvar</button>
        <button onclick="cancelarEdicaoDespesa(${id}, '${descOriginal}', '${valorOriginal}')" class="btn btn-secondary btn-sm">
            Cancelar
        </button>
    `;
}

// CANCELAR 
function cancelarEdicaoDespesa(id, descOriginal, valorOriginal){

    document.getElementById(`desc-${id}`).innerText = descOriginal;
    document.getElementById(`valor-${id}`).innerText = valorOriginal;

    const tdAcoes = document.getElementById(`linha-${id}`).querySelector("td:last-child");

    tdAcoes.innerHTML = `
        <button onclick="editarDespesa(${id})" class="btn btn-warning btn-sm">Editar</button>
        <button onclick="excluirDespesa(${id})" class="btn btn-danger btn-sm">Excluir</button>
    `;
}

// SALVAR
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
            location.reload();
        } else {
            alert(data.error);
        }

    });
}

// EXCLUIR
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
