document.addEventListener("DOMContentLoaded", function(){

    // FORMULÁRIO DE LOGIN
    const form = document.getElementById('formLogin');

    // CAMPO DE ERRO
    const erro = document.getElementById('erro');


    // OBTÉM TOKEN CSRF DO DJANGO
    function getCSRFToken(){

        return document.querySelector(
            '[name=csrfmiddlewaretoken]'
        ).value;
    }


    // ENVIO DO FORMULÁRIO
    form.addEventListener('submit', function(e){

        e.preventDefault();

        // Dados do formulário
        const formData = new FormData(form);


        // REQUISIÇÃO PARA API DE LOGIN
        fetch("/api/login/", {

            method: 'POST',

            body: formData,

            headers: {
                'X-CSRFToken': getCSRFToken()
            },

            credentials: 'same-origin'
        })

        // Converte resposta para JSON
        .then(res => res.json())

        .then(data => {

            // Login realizado com sucesso
            if(data.success){

                window.location.href = "/dashboard/";

            } else {

                // Exibe mensagem de erro
                erro.classList.remove('d-none');

                erro.innerText = "Login inválido";
            }

        });

    });

});