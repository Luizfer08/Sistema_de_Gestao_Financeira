// Este arquivo controla login, mostrar senha e mensagens de erro.
document.addEventListener("DOMContentLoaded", function () {

    // FORMULARIO LOGIN
    const form = document.getElementById("formLogin");

    // MENSAGEM DE ERRO
    const erro = document.getElementById("erro");

    // BOTAO MOSTRAR SENHA
    const toggleSenha = document.querySelector("[data-password-toggle]");

    // INPUT SENHA
    const senha = document.getElementById("loginSenha");

    // MOSTRAR / OCULTAR SENHA
    if (toggleSenha && senha) {
        toggleSenha.addEventListener("click", function () {
            const mostrando = senha.type === "text";
            senha.type = mostrando ? "password" : "text";
            toggleSenha.setAttribute(
                "aria-label",
                mostrando ? "Mostrar senha" : "Ocultar senha"
            );
        });
    }

    // VERIFICA SE O FORMULARIO EXISTE
    if (!form) return;

    // CSRF TOKEN
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    }

    // SUBMIT LOGIN
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        // REQUISICAO LOGIN
        fetch("/api/login/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            credentials: "same-origin",
        })

        .then((res) => res.json())
        .then((data) => {

            // LOGIN SUCESSO
            if (data.success) {
                window.location.href = "/dashboard/";
                return;
            }

            // LOGIN INVALIDO
            erro.classList.remove("d-none");
            erro.innerText = data.error || "Login invÃ¡lido";
        })

        // ERRO REQUISICAO
        .catch(() => {

            erro.classList.remove("d-none");

            erro.innerText = "NÃ£o foi possÃ­vel realizar o login agora.";

        });

    });

});

