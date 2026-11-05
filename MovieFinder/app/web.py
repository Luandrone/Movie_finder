from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.serviço import pesquisar_filmes_por_nome
from app.excecoes import ErroApi

app = FastAPI(
    title="MovieFinder API",
    description="API para pesquisa e gerenciamento de filmes.",
    version="1.0.0"
)

@app.get("/health")
def verificar_saude():
    return {
        "status": "ok",
        "aplicacao": "MovieFinder"
    }

class FilmeResumo(BaseModel):
    id : int
    titulo : str
    ano : str
    nota : float

@app.get("/filmes/buscar")
def buscar_filmes():
    return {
        "mensagem": "Rota de busca funcionando!"
    }