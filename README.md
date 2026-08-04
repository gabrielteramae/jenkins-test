# Task API
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat&logo=jenkins&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)

API REST CRUD para gerenciamento de tarefas, com pipeline de CI/CD completo em Jenkins.

## Sobre

Uma solução simples e bem estruturada para criar, listar, atualizar o status e excluir tarefas. O backend foi construído com **Python** e **FastAPI**, com validação de dados via **Pydantic** e cobertura de testes automatizados via **Pytest**. O projeto inclui um `Jenkinsfile` completo, cobrindo desde a instalação de dependências até o build e validação da imagem Docker.

## Funcionalidades

- Criar tarefa
- Listar tarefas
- Buscar tarefa por ID
- Atualizar status da tarefa (PENDING, IN_PROGRESS, DONE)
- Excluir tarefa
- Endpoint de healthcheck (`/health`) usado pelo pipeline e por monitoramento
- Validação de entrada via Pydantic, com erros padronizados (422)
- Documentação interativa da API com Swagger UI / OpenAPI (`/docs`)
- Pipeline Jenkins: build → testes → imagem Docker → smoke test → deploy (branch `main`)

## Stack

- **Backend:** Python 3.12, FastAPI, Pydantic
- **Testes:** Pytest, httpx (TestClient) — 8 testes cobrindo todos os endpoints
- **Containerização:** Docker
- **CI/CD:** Jenkins (pipeline declarativo via `Jenkinsfile`)
- **Armazenamento:** em memória (propositalmente simples, sem banco de dados — foco do projeto é a automação em volta da API)

---

## Como rodar localmente

**Pré-requisitos:** Python 3.12+

Para rodar a aplicação, execute na raiz do projeto:
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse a documentação interativa em `http://localhost:8000/docs`.

## Rodando os testes

```bash
pytest
```

## Rodando com Docker

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

---

## Pipeline Jenkins

O `Jenkinsfile` define os seguintes estágios:

1. **Checkout** — baixa o código do repositório
2. **Instalar dependências** — cria virtualenv e instala requirements
3. **Rodar testes** — executa Pytest e publica resultados (JUnit XML)
4. **Build da imagem Docker** — constrói a imagem versionada pelo número do build
5. **Smoke test do container** — sobe o container e valida o endpoint `/health`
6. **Deploy (simulado)** — roda apenas na branch `main`

### Como configurar no Jenkins

1. Suba um Jenkins local (via Docker)
2. **New Item → Pipeline**
3. Em Pipeline, escolha **"Pipeline script from SCM"**
4. Aponte pro repositório Git deste projeto e o caminho do `Jenkinsfile`
5. Clique em **Build Now**

> **Nota:** o agente Jenkins precisa ter Python 3 e Docker instalados/acessíveis para rodar todos os estágios do pipeline.

---
© 2026 Gabriel Teramae Chan
