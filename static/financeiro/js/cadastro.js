// Este arquivo controla cadastro, aceite dos termos e busca de CEP.
document.addEventListener("DOMContentLoaded", function(){

    // FORMULARIO DE CADASTRO
    const form = document.getElementById("formCadastro");

    // CAMPO DE MENSAGENS
    const mensagem = document.getElementById("mensagem");

    // ELEMENTOS DO MODAL DE TERMOS
    const modal = document.getElementById("modalTermos");
    const abrir = document.getElementById("abrirTermos");
    const fechar = document.getElementById("fecharTermos");
    const termos = document.getElementById("termos");


    // OBTEM TOKEN CSRF DO DJANGO
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


    // ENVIO DO FORMULARIO
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
                    "Inputs de senha nÃ£o encontrados"
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
                        As senhas nÃ£o coincidem
                    </div>
                `;

                return;
            }

            // Valida tamanho minimo da senha
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

            // CRIA OBJETO COM DADOS DO FORMULARIO
            const formData = new FormData(form);

            // Adiciona campo de aceite
            formData.append("aceitou", "true");

            // ENVIA REQUISICAO DE CADASTRO
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

            // Captura erros da requisicao
            .catch((err) => {

                console.error(err);

                mensagem.innerHTML = `
                    <div class="alert alert-danger">
                        Erro na requisiÃ§Ã£o
                    </div>
                `;
            });

        });
    }


    // CAMPO CEP
    const cepInput = document.getElementById("cep");


    // BUSCA ENDERECO AUTOMATICO PELO CEP
    if(cepInput){

        cepInput.addEventListener("blur", function(){

            // Remove caracteres nao numericos
            const cep = this.value.replace(/\D/g, '');

            // Valida tamanho do CEP
            if(cep.length !== 8) return;

            // CONSULTA API VIACEP
            fetch(`https://viacep.com.br/ws/${cep}/json/`)

            .then(res => res.json())

            .then(data => {

                // CEP nao encontrado
                if(data.erro){

                    mensagem.innerHTML = `
                        <div class="alert alert-danger">
                            CEP nÃ£o encontrado
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

