// CSRF
function getCSRFToken(){
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// ELEMENTOS
const loginForm = document.getElementById("formLogin");
const cadastroForm = document.getElementById("formCadastro");
const mensagem = document.getElementById("mensagem");
const toggleText = document.getElementById("toggleText");

// TOGGLE
function toggleForm(){
    loginForm.classList.toggle("hidden");
    cadastroForm.classList.toggle("hidden");

    toggleText.innerText = loginForm.classList.contains("hidden") 
        ? "Já tenho conta" 
        : "Criar conta";
}

// LOGIN
if(loginForm){
    loginForm.addEventListener("submit", function(e){

        e.preventDefault();

        const formData = new FormData(loginForm);

        fetch("/api/login/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            credentials: "same-origin",
            body: formData
        })
        .then(res => res.json())
        .then(data => {

            if(data.success){
                window.location.href = "/dashboard/";
            } else {
                mensagem.innerHTML = `<div class="alert alert-danger">Login inválido</div>`;
            }

        });

    });
}

// CADASTRO
if(cadastroForm){
    cadastroForm.addEventListener("submit", function(e){

        e.preventDefault();

        const termos = document.getElementById("termos");

        if(!termos.checked){
            mensagem.innerHTML = `<div class="alert alert-danger">Aceite os termos</div>`;
            return;
        }

        const formData = new FormData(cadastroForm);
        formData.append("aceitou", true);

        fetch("/api/cadastro/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            credentials: "same-origin",
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
}

// VIA CEP
const cepInput = document.getElementById('cep');

if(cepInput){
    cepInput.addEventListener('blur', function(){

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