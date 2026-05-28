document.addEventListener("DOMContentLoaded", function () {

    // FORMULÁRIO LOGIN
    const form = document.getElementById("formLogin");

    // MENSAGEM DE ERRO
    const erro = document.getElementById("erro");

    // BOTÃO MOSTRAR SENHA
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

    // VERIFICA SE O FORMULÁRIO EXISTE
    if (!form) return;

    // CSRF TOKEN
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    }

    // SUBMIT LOGIN
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        // REQUISIÇÃO LOGIN
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

            // LOGIN INVÁLIDO
            erro.classList.remove("d-none");
            erro.innerText = data.error || "Login inválido";
        })

        // ERRO REQUISIÇÃO
        .catch(() => {

            erro.classList.remove("d-none");

            erro.innerText = "Não foi possível realizar o login agora.";

        });

    });

});