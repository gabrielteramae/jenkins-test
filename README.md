# Task API
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?logo=jenkins&logoColor=white)

API simples de gerenciamento de tarefas, construída em FastAPI, com pipeline CI/CD completo em Jenkins (build, testes, imagem Docker e smoke test).

## Sobre

Projeto criado para praticar a construção de um pipeline Jenkins real, do checkout do código até a validação da imagem Docker via smoke test. A API em si é intencionalmente simples (CRUD de tarefas em memória) — o foco está na automação em torno dela.

## Funcionalidades da API

- Criar tarefa
- Listar tarefas
- Buscar tarefa por ID
- Atualizar status da tarefa (PENDING, IN_PROGRESS, DONE)
- Excluir tarefa
- Endpoint de healthcheck (`/health`)

## Stack

- **Backend:** Python 3.12, FastAPI, Pydantic
- **Testes:** Pytest, httpx (TestClient)
- **Containerização:** Docker
- **CI/CD:** Jenkins (pipeline declarativo via `Jenkinsfile`)

---

## Como rodar localmente

**Pré-requisitos:** Python 3.12+

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
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
3. **Rodar testes** — executa pytest e publica resultados (JUnit XML)
4. **Build da imagem Docker** — constrói a imagem versionada pelo número do build
5. **Smoke test do container** — sobe o container e valida o endpoint `/health`
6. **Deploy (simulado)** — roda apenas na branch `main`, representando onde entraria push pra um registry real

### Como configurar no Jenkins

1. Suba um Jenkins local (ver `04-cicd-gitops/jenkins/pratica.md` do repo `devops-cloud-study` pra instruções de setup via Docker)
2. **New Item → Pipeline**
3. Em Pipeline, escolha **"Pipeline script from SCM"**
4. Aponte pro repositório Git deste projeto e o caminho do `Jenkinsfile`
5. Clique em **Build Now**

> **Nota:** o agente Jenkins precisa ter Python 3 e Docker instalados/acessíveis para rodar todos os estágios do pipeline.

---
© 2026 Gabriel Teramae Chan
