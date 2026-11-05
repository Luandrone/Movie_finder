from fastapi import FastAPI

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