// TOGGLE
function toggleFormReceita(){
    const form = document.getElementById("formReceitaContainer");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

// CSRF
function getCSRFToken(){
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

//  CRIA
document.getElementById("formReceita").addEventListener("submit", function(e){
    e.preventDefault();

    const formData = new FormData(this);

    fetch("{% url 'financeiro:criar_receita' %}", {
        method: "POST",
        headers: {"X-CSRFToken": getCSRFToken()},
        body: formData
    })
    .then(res => res.json())
    .then(data => {

        if(data.success){

            location.reload(); // simples e seguro (evita inconsistência)

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
    .replace(',', '.')      // troca vírgula por ponto
    .trim();

valor.innerHTML = `<input id="input-valor-${id}" value="${valorLimpo}" class="form-control">`;

    const tdAcoes = desc.parentElement.querySelector("td:last-child");

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

    const tdAcoes = document.getElementById(`linha-${id}`).querySelector("td:last-child");

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
            location.reload();
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
