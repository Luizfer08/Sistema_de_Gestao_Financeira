document.addEventListener("DOMContentLoaded", function(){

    // FORMULÁRIO DE CADASTRO
    const form = document.getElementById("formCadastro");

    // CAMPO DE MENSAGENS
    const mensagem = document.getElementById("mensagem");

    // ELEMENTOS DO MODAL DE TERMOS
    const modal = document.getElementById("modalTermos");
    const abrir = document.getElementById("abrirTermos");
    const fechar = document.getElementById("fecharTermos");
    const termos = document.getElementById("termos");


    // OBTÉM TOKEN CSRF DO DJANGO
    function getCSRFToken() {

        const input = document.querySelector(
            '[name=csrfmiddlewaretoken]'
        );

        return input ? input.value : "";
    }


    // ABRE MODAL DOS TERMOS
    if(abrir){

        abrir.addEventListener("click", function(e){

            e.preventDefault();

            modal.classList.add("active");
        });
    }


    // FECHA MODAL DOS TERMOS
    if(fechar){

        fechar.addEventListener("click", function(){

            modal.classList.remove("active");
        });
    }


    // ENVIO DO FORMULÁRIO
    if(form){

        form.addEventListener("submit", function(e){

            e.preventDefault();

            // Limpa mensagens anteriores
            mensagem.innerHTML = "";

            // CAMPOS DE SENHA
            const senhaInput = document.getElementById("senha");

            const confirmarInput = document.getElementById(
                "confirmar_senha"
            );

            // Verifica se inputs existem
            if (!senhaInput || !confirmarInput) {

                console.error(
                    "Inputs de senha não encontrados"
                );

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        Erro interno
                    </div>
                `;

                return;
            }

            // Valores digitados
            const senha = senhaInput.value;
            const confirmar = confirmarInput.value;

            // Valida preenchimento da senha
            if (!senha || !confirmar){

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        Preencha a senha
                    </div>
                `;

                return;
            }

            // Verifica se as senhas coincidem
            if (senha !== confirmar) {

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        As senhas não coincidem
                    </div>
                `;

                return;
            }

            // Valida tamanho mínimo da senha
            if (senha.length < 6) {

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        Senha deve ter pelo menos 6 caracteres
                    </div>
                `;

                return;
            }

            // Verifica aceite dos termos
            if (!termos || !termos.checked) {

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        Aceite os termos
                    </div>
                `;

                return;
            }

            // CRIA OBJETO COM DADOS DO FORMULÁRIO
            const formData = new FormData(form);

            // Adiciona campo de aceite
            formData.append("aceitou", "true");

            // ENVIA REQUISIÇÃO DE CADASTRO
            fetch("/api/cadastro/", {

                method: "POST",

                headers: {
                    "X-CSRFToken": getCSRFToken()
                },

                body: formData,

                credentials: "same-origin"
            })

            // Converte resposta para JSON
            .then(res => res.json())

            .then(data => {

                // Cadastro realizado com sucesso
                if(data.success){

                    window.location.href = "/dashboard/";

                } else {

                    // Exibe erro retornado pela API
                    mensagem.innerHTML = `
                        <div class="alert alert-danger">
                            ${data.error}
                        </div>
                    `;
                }

            })

            // Captura erros da requisição
            .catch((err) => {

                console.error(err);

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        Erro na requisição
                    </div>
                `;
            });

        });
    }


    // CAMPO CEP
    const cepInput = document.getElementById("cep");


    // BUSCA ENDEREÇO AUTOMÁTICO PELO CEP
    if(cepInput){

        cepInput.addEventListener("blur", function(){

            // Remove caracteres não numéricos
            const cep = this.value.replace(/\D/g, '');

            // Valida tamanho do CEP
            if(cep.length !== 8) return;

            // CONSULTA API VIACEP
            fetch(`https://viacep.com.br/ws/${cep}/json/`)

            .then(res => res.json())

            .then(data => {

                // CEP não encontrado
                if(data.erro){

                    mensagem.innerHTML = `
                        <div class="alert alert-danger">
                            CEP não encontrado
                        </div>
                    `;

                    return;
                }

                // Preenche campos automaticamente
                document.getElementById('endereco').value =
                    data.logradouro || "";

                document.getElementById('cidade').value =
                    data.localidade || "";

                document.getElementById('estado').value =
                    data.uf || "";
            })

            // Captura erros da API
            .catch(() => {

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        Erro ao buscar CEP
                    </div>
                `;
            });

        });
    }

});