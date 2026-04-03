document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById("formCadastro");
    const mensagem = document.getElementById("mensagem");

    const modal = document.getElementById("modalTermos");
    const abrir = document.getElementById("abrirTermos");
    const fechar = document.getElementById("fecharTermos");
    const termos = document.getElementById("termos");

    // ABRIR MODAL
    abrir.addEventListener("click", function(e){
        e.preventDefault();
        modal.classList.add("active");
    });

    // FECHAR MODAL
    fechar.addEventListener("click", function(){
        modal.classList.remove("active");
    });

    function getCSRFToken(){
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // CADASTRO
    form.addEventListener("submit", function(e){

        e.preventDefault();

        if(!termos.checked){
            mensagem.innerHTML = `<div class="alert alert-danger">Aceite os termos</div>`;
            return;
        }
        
        const formData = new FormData(form);

        formData.append("aceitou", "true");

        fetch("/api/cadastro/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {

            if(data.success){
                window.location.href = "/dashboard/";
            } else {
                mensagem.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            }

        });

    });

});

// CEP
const cepInput = document.getElementById("cep");

if(cepInput){
    cepInput.addEventListener("blur", function(){

        const cep = this.value;

        fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('endereco').value = data.logradouro || "";
            document.getElementById('cidade').value = data.localidade || "";
            document.getElementById('estado').value = data.uf || "";
        });

    });
}

// VALIDAÇÃO
document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById("formCadastro");
    const mensagem = document.getElementById("mensagem");

    function getCSRFToken(){
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    form.addEventListener("submit", function(e){

        e.preventDefault();

        const formData = new FormData(form);

        fetch("/api/cadastro/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {

            if(data.success){
                window.location.href = "/dashboard/";
            } else {
                mensagem.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            }

        });

    });

});