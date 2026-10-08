# Task API — CRUD em memória para um pipeline Jenkins

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-8.3.3-0A9EDC?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-Pipeline-D24939?logo=jenkins&logoColor=white)

API de tarefas cujo estado é um `dict` no processo. O ponto do repositório é o `Jenkinsfile`: venv, pytest com JUnit, build da imagem, smoke test de `/health` e um deploy que só imprime na branch `main`.

## Por que memória

| Escolha | Efeito |
| --- | --- |
| `_tasks` em memória, id inteiro crescente | O pipeline não precisa de banco. Restart zera os dados. |
| SQLite ou Postgres | Sobrevive a restart; o Jenkinsfile teria que subir esse serviço. Não está aqui. |

O estágio "Deploy (simulado)" não envia a imagem a registry nenhum. O `post { always }` tenta `docker rmi` da tag `task-api:<BUILD_NUMBER>`.

## Stack

- Python 3.12 (`Dockerfile`: `python:3.12-slim`)
- FastAPI 0.115.0, Uvicorn 0.30.6, Pydantic 2.9.2
- pytest 8.3.3 e httpx 0.27.2 (`TestClient`)
- Docker e Jenkins Pipeline (o agente Jenkins não vem no repositório)

## Estrutura

```
app/
├── main.py       # rotas; dict _tasks
└── models.py     # TaskStatus: PENDING, IN_PROGRESS, DONE
tests/
└── test_main.py
Dockerfile
Jenkinsfile
pytest.ini        # pythonpath = .
requirements.txt
```

## Como rodar

```bash
git clone https://github.com/gabrielteramae/jenkins-test.git
cd jenkins-test
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Imagem, como o `Dockerfile` define (porta 8000):

```bash
docker build -t task-api .
docker run --rm -p 8000:8000 task-api
```

O pipeline espera um agente com `python3`, `pip`, `pytest`, `docker` e `curl`. O smoke sobe o container na porta 8001 do host e chama `/health`.

## Endpoints

| Método | Rota | Resposta |
| --- | --- | --- |
| GET | `/health` | `{"status":"ok"}` |
| POST | `/tasks` | 201. `title` (1–200), `description` opcional (até 1000). Status inicial `PENDING` |
| GET | `/tasks` | lista |
| GET | `/tasks/{task_id}` | 404 se não existe |
| PATCH | `/tasks/{task_id}` | só troca `status` |
| DELETE | `/tasks/{task_id}` | 204 |

Título vazio: 422.

## Testes realizados

`tests/test_main.py` usa `TestClient`. Antes de cada teste limpa `_tasks` (o contador `_next_id` não volta a 1). Cobre health, criação, título vazio, listagem, busca, 404, PATCH para `DONE` e DELETE. Não há teste do `Jenkinsfile` nem do container.

---

© 2026 Gabriel Teramae Chan
