document.addEventListener("DOMContentLoaded", function () {
    const cnpjInput = document.querySelector("#id_cpf_cnpj");

    cnpjInput.addEventListener("blur", function () {
        const cnpj = cnpjInput.value.replace(/\D/g, '');

        if (cnpj.length === 14) {
            fetch(`/cadastro/consulta_cnpj/?cnpj=${cnpj}`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector("#id_nome_razao_social").value = data.razao_social || '';
                    document.querySelector("#id_email").value = data.email || '';
                    document.querySelector("#id_telefone_1").value = data.telefone || '';
                    document.querySelector("#id_cep").value = data.cep || '';
                    document.querySelector("#id_logradouro").value = data.logradouro || '';
                    document.querySelector("#id_numero").value = data.numero || '';
                    document.querySelector("#id_complemento").value = data.complemento || '';
                    document.querySelector("#id_bairro").value = data.bairro || '';
                    document.querySelector("#id_municipio").value = data.municipio || '';
                })
                .catch(error => {
                    console.error("Erro:", error);
                    alert("Erro ao consultar o CNPJ.");
                });
        }
    });
});