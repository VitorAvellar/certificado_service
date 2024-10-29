document.getElementById('certificadoForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const curso = document.getElementById('curso').value;
    const data = document.getElementById('data').value;

    const response = await fetch('http://localhost:5000/emitir_certificado', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, curso, data })
    });

    const result = await response.json();
    if (response.ok) {
        document.getElementById('resultado').innerHTML = `Certificado emitido! <a href="${result.pdf_url}">Baixar PDF</a>`;
    } else {
        document.getElementById('resultado').innerText = 'Erro ao emitir certificado';
    }
});
