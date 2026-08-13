# 🎬 MovieFinder

Aplicação desenvolvida em Python que utiliza a API do TMDB para pesquisar filmes e consultar informações detalhadas e sua disponibilidade no Brasil.

## 🚀 Funcionalidades

- 🔎 Pesquisa de filmes;
- 🎬 Consulta de detalhes;
- 📝 Sinopse, nota, duração e gêneros;
- 📺 Consulta de disponibilidade no Brasil;
- 🛒 Opções de aluguel e compra;
- ⚠️ Tratamento de erros da API.

## 🛠️ Tecnologias

- Python
- Requests
- python-dotenv
- API REST
- TMDB API
- Git

## 🔐 Configuração

O projeto utiliza uma chave da API do TMDB armazenada em uma variável de ambiente.

Crie um arquivo `.env`:

``env
API_KEY=sua_chave_da_api

O arquivo .env não é versionado pelo Git.

📦 Instalação

Clone o projeto e instale as dependências:

git clone URL_DO_REPOSITORIO
cd MovieFinder
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

Configure o .env e execute:

python main.py

📁 Estrutura
MovieFinder/
├── app/
│   ├── api.py
│   ├── config.py
│   ├── excecoes.py
│   ├── filme.py
│   └── serviço.py
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
📚 Objetivo

Projeto desenvolvido para praticar Python, POO, consumo de APIs REST, tratamento de exceções, variáveis de ambiente, organização de código e Git.

🔮 Próximos passos
Testes automatizados;
Melhorias na arquitetura;
Novas funcionalidades para busca e apresentação dos filmes.