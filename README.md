# 🎬 MovieFinder

Aplicação desenvolvida em Python para pesquisar filmes utilizando a API do [The Movie Database (TMDB)](https://www.themoviedb.org/), consultar detalhes e verificar a disponibilidade para assistir, alugar ou comprar filmes no Brasil.

O projeto utiliza PostgreSQL para persistir os dados e sincronizar as informações obtidas pela API com os registros existentes.

## ✨ Funcionalidades

- **Pesquisa de filmes:** busca títulos utilizando a API do TMDB.
- **Detalhes dos filmes:** consulta sinopse, ano, nota, duração e gêneros.
- **Disponibilidade:** consulta provedores de streaming, aluguel e compra no Brasil.
- **Persistência de dados:** armazena informações dos filmes no PostgreSQL.
- **Sincronização:** compara os dados recebidos da API com os registros existentes e identifica alterações.
- **Gerenciamento de gêneros:** mantém os gêneros relacionados aos filmes salvos.
- **Gerenciamento de favoritos:** permite adicionar e remover filmes dos favoritos e consultar a lista de favoritos.
- **Gerenciamento de filmes salvos:** permite listar e excluir filmes armazenados no banco.
- **Tratamento de erros:** trata falhas de conexão e respostas HTTP da API.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal da aplicação.
- **PostgreSQL:** banco de dados relacional.
- **Requests:** realização de requisições HTTP.
- **Psycopg:** conexão com o PostgreSQL.
- **python-dotenv:** leitura de variáveis de ambiente.
- **pytest:** execução dos testes automatizados.
- **TMDB API:** fonte dos dados dos filmes e de sua disponibilidade.

## 📁 Estrutura do projeto

```text
Movie_finder/
├── MovieFinder/
│   ├── app/
│   │   ├── banco/
│   │   │   ├── comparador.py
│   │   │   ├── conexao.py
│   │   │   ├── consultas.py
│   │   │   ├── mapper.py
│   │   │   └── repositorio.py
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── excecoes.py
│   │   ├── filme.py
│   │   ├── formatador.py
│   │   ├── menu.py
│   │   ├── serviço.py
│   │   └── transformador.py
│   ├── tests/
│   │   ├── banco/
│   │   ├── test_api.py
│   │   ├── test_filme.py
│   │   ├── test_serviço.py
│   │   └── test_transformador.py
│   └── main.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── schema.sql
```

**Principais responsabilidades:**

- `app/api.py`: realiza as requisições à API do TMDB.
- `app/config.py`: centraliza as configurações e os endpoints da API.
- `app/serviço.py`: coordena os fluxos de pesquisa, consulta, salvamento e gerenciamento dos filmes.
- `app/filme.py`: representa os filmes por meio de objetos Python.
- `app/transformador.py`: transforma e organiza os dados recebidos da API.
- `app/formatador.py`: apresenta os resultados no terminal.
- `app/menu.py`: controla as opções e as seleções feitas pelo usuário.
- `app/banco/conexao.py`: estabelece conexões com o PostgreSQL.
- `app/banco/consultas.py`: reúne as consultas SQL.
- `app/banco/repositorio.py`: coordena a persistência, as transações e a sincronização dos registros.
- `app/banco/comparador.py`: identifica diferenças entre os dados da API e os registros armazenados.
- `app/banco/mapper.py`: converte registros do banco em objetos e estruturas utilizados pela aplicação.

## ⚙️ Configuração do ambiente

### 1. Pré-requisitos

Antes de executar o projeto, instale:

- Python.
- PostgreSQL.
- Uma chave de acesso à API do TMDB.

### 2. Clonar o repositório

No terminal, execute:

```bash
git clone https://github.com/Luandrone/Movie_finder.git
cd Movie_finder
```

### 3. Criar e ativar o ambiente virtual

No Windows, utilizando PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

O ambiente virtual isola as dependências Python utilizadas pelo projeto.

### 4. Instalar as dependências

Com o ambiente virtual ativado, execute na raiz do repositório:

```bash
python -m pip install -r requirements.txt
```

### 5. Configurar as variáveis de ambiente

O projeto utiliza variáveis de ambiente para acessar a API do TMDB e o banco PostgreSQL.

Na raiz do repositório, copie o modelo de configuração para o local esperado pela aplicação:

```powershell
Copy-Item .env.example MovieFinder/.env
```

Esse comando pressupõe que você ainda não tenha um arquivo `MovieFinder/.env`. Caso já exista, mantenha o arquivo atual e edite suas configurações, sem substituí-lo.

Preencha `MovieFinder/.env` com suas próprias credenciais:

```dotenv
API_KEY=sua_chave_de_acesso_tmdb

DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

Substitua os valores de exemplo pelos dados da sua instalação. A variável `API_KEY` deve conter uma credencial válida para o cabeçalho de autorização utilizado pela aplicação.

**Importante:** não compartilhe nem envie seu arquivo `.env` ao GitHub. O arquivo `.env.example` contém somente valores fictícios e pode ser versionado.

### 6. Preparar o banco de dados

Crie um banco PostgreSQL vazio para o MovieFinder.

Na raiz do projeto, o arquivo `schema.sql` contém os comandos necessários para criar as tabelas:

- `tblfilmes`
- `tblgeneros`
- `tblfilmegeneros`
- `tbldisponibilidade`

Abra o Query Tool do pgAdmin conectado ao banco recém-criado e execute o conteúdo do arquivo `schema.sql`.

O script cria as tabelas, define seus campos, valores padrão e restrições de integridade. Ele foi validado em um banco de teste separado.

**Atenção:** execute esse script apenas em um banco vazio preparado para o projeto. Ele utiliza comandos `CREATE TABLE` e não foi projetado para recriar tabelas que já existem.

### 7. Executar a aplicação

Na raiz do repositório, execute:

```bash
python MovieFinder/main.py
```

O menu interativo permite pesquisar filmes, consultar os registros salvos, excluir filmes e gerenciar favoritos.

## 🧪 Testes automatizados

O projeto utiliza `pytest` para verificar o comportamento de suas funções e módulos.

Com o ambiente virtual ativado, entre na pasta `MovieFinder`:

```powershell
cd MovieFinder
```

Execute a suíte de testes:

```bash
python -m pytest
```

Para executar os testes de um arquivo específico, por exemplo:

```bash
python -m pytest tests/banco/test_repositorio.py
```

Os testes utilizam dados simulados e mocks em diferentes cenários, permitindo verificar o comportamento da aplicação sem depender de chamadas reais à API para cada teste.

## 📚 Objetivo do projeto

O MovieFinder foi desenvolvido como projeto de estudo e prática de programação em Python, com foco em:

- Consumo de APIs externas.
- Programação orientada a objetos.
- Persistência e consultas SQL.
- Modelagem de relacionamentos em banco de dados relacional.
- Separação de responsabilidades entre módulos.
- Tratamento de erros e transações.
- Testes automatizados.
- Configuração por variáveis de ambiente.
- Utilização do Git e GitHub para versionamento.