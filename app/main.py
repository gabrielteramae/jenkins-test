from fastapi import FastAPI, HTTPException, status
from typing import List

from app.models import Task, TaskCreate, TaskUpdate

app = FastAPI(
    title="Task API",
    description="API simples de gerenciamento de tarefas, construída para praticar CI/CD com Jenkins.",
    version="1.0.0",
)

# Armazenamento em memória (propositalmente simples, sem banco de dados)
_tasks: dict[int, Task] = {}
_next_id: int = 1


@app.get("/health", tags=["Infra"])
def health_check():
    """Endpoint de healthcheck, usado pelo pipeline e por monitoramento."""
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(payload: TaskCreate):
    global _next_id
    task = Task(id=_next_id, title=payload.title, description=payload.description)
    _tasks[task.id] = task
    _next_id += 1
    return task


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def list_tasks():
    return list(_tasks.values())


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int):
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task_status(task_id: int, payload: TaskUpdate):
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task.status = payload.status
    _tasks[task_id] = task
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int):
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    del _tasks[task_id]
