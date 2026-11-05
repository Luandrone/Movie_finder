from fastapi.testclient import TestClient
from app.web import app


client = TestClient(app)


def test_verificar_saude():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "ok",
        "aplicacao": "MovieFinder"
    }

def test_rota_buscar_filmes():
    resposta = client.get("/filmes/buscar")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "mensagem": "Rota de busca funcionando!"
    }