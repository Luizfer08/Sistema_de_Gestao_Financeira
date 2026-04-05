document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById("formCadastro");
    const mensagem = document.getElementById("mensagem");

    const modal = document.getElementById("modalTermos");
    const abrir = document.getElementById("abrirTermos");
    const fechar = document.getElementById("fecharTermos");
    const termos = document.getElementById("termos");

    // ===== CSRF TOKEN =====
    function getCSRFToken() {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        return input ? input.value : "";
    }

    // ===== MODAL =====
    if(abrir){
        abrir.addEventListener("click", function(e){
            e.preventDefault();
            modal.classList.add("active");
        });
    }

    if(fechar){
        fechar.addEventListener("click", function(){
            modal.classList.remove("active");
        });
    }

    // ===== CADASTRO =====
    if(form){
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
                body: formData,
                credentials: "same-origin"
            })
            .then(res => res.json())
            .then(data => {

                if(data.success){
                    window.location.href = "/dashboard/";
                } else {
                    mensagem.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                }

            })
            .catch(() => {
                mensagem.innerHTML = `<div class="alert alert-danger">Erro na requisição</div>`;
            });

        });
    }

    // ===== CEP =====
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
            })
            .catch(() => {
                mensagem.innerHTML = `<div class="alert alert-danger">CEP não encontrado</div>`;
            });

        });
    }

});