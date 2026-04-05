document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById("formCadastro");
    const mensagem = document.getElementById("mensagem");

    const modal = document.getElementById("modalTermos");
    const abrir = document.getElementById("abrirTermos");
    const fechar = document.getElementById("fecharTermos");
    const termos = document.getElementById("termos");


    function getCSRFToken() {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        return input ? input.value : "";
    }

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

    if(form){
        form.addEventListener("submit", function(e){

            e.preventDefault();

            mensagem.innerHTML = "";

            const senhaInput = document.getElementById("senha");
            const confirmarInput = document.getElementById("confirmar_senha");

            if (!senhaInput || !confirmarInput) {
                console.error("Inputs de senha não encontrados");
                mensagem.innerHTML = `<div class="alert alert-danger">Erro interno</div>`;
                return;
            }

            const senha = senhaInput.value;
            const confirmar = confirmarInput.value;

            if (!senha || !confirmar){
                mensagem.innerHTML = `<div class="alert alert-danger">Preencha a senha</div>`;
                return;
            }

            if (senha !== confirmar) {
                mensagem.innerHTML = `<div class="alert alert-danger">As senhas não coincidem</div>`;
                return;
            }

            if (senha.length < 6) {
                mensagem.innerHTML = `<div class="alert alert-danger">Senha deve ter pelo menos 6 caracteres</div>`;
                return;
            }

            if (!termos || !termos.checked) {
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
            .catch((err) => {
                console.error(err);
                mensagem.innerHTML = `<div class="alert alert-danger">Erro na requisição</div>`;
            });

        });
    }

    const cepInput = document.getElementById("cep");

    if(cepInput){
        cepInput.addEventListener("blur", function(){

            const cep = this.value.replace(/\D/g, '');

            if(cep.length !== 8) return;

            fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(res => res.json())
            .then(data => {

                if(data.erro){
                    mensagem.innerHTML = `<div class="alert alert-danger">CEP não encontrado</div>`;
                    return;
                }

                document.getElementById('endereco').value = data.logradouro || "";
                document.getElementById('cidade').value = data.localidade || "";
                document.getElementById('estado').value = data.uf || "";
            })
            .catch(() => {
                mensagem.innerHTML = `<div class="alert alert-danger">Erro ao buscar CEP</div>`;
            });

        });
    }

});