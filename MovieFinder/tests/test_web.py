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
    resposta = client.get("/filmes/buscar", params={"nome": "The Batman"})

    assert resposta.status_code == 200
    assert resposta.json() == {
        "nome_recebido": "The Batman"
    }

def test_rota_buscar_filmes_sem_nome():
    resposta = client.get("/filmes/buscar")

    assert resposta.status_code == 422