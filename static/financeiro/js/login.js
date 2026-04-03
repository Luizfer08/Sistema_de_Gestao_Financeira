document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById('formLogin');
    const erro = document.getElementById('erro');

    function getCSRFToken(){
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    form.addEventListener('submit', function(e){

        e.preventDefault();

        const formData = new FormData(form);

        fetch("/api/login/", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        })
        .then(res => res.json())
        .then(data => {

            if(data.success){
                window.location.href = "/dashboard/";
            } else {
                erro.classList.remove('d-none');
                erro.innerText = "Login inválido";
            }

        });

    });

});