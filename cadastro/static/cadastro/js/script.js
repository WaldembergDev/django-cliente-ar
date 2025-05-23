let clienteArrastado = null;

function arrastar(event) {
    clienteArrastado = event.target;
}

function permitirSoltar(event) {
    event.preventDefault();
}

function soltar(event, novoStatus) {
    event.preventDefault();

    let coluna = event.currentTarget;

    if (clienteArrastado && coluna.classList.contains("coluna")) {
        coluna.appendChild(clienteArrastado);

        fetch(atualizarStatusUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                id: clienteArrastado.dataset.id,
                status: novoStatus
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert("Erro ao atualizar status");
            }
        });
    }
}
