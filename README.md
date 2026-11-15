# Task API

A small task-management API built with FastAPI. The reference implementation below stores tasks in memory, so data resets when the server restarts.

## Requirements and running

Install the dependencies:

```powershell
python -m pip install fastapi uvicorn
```

From the project directory, run:

```powershell
python -m uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Swagger UI is at `http://127.0.0.1:8000/docs`, and the OpenAPI schema is at `http://127.0.0.1:8000/openapi.json`.

> **Note:** The code below is a Copilot-generated reference implementation in this README only. It has not been copied into or used to change `main.py`. 

## Reference implementation

```python
from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="Task API", version="1.0")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskStatusUpdate(BaseModel):
    done: bool


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


tasks: dict[int, Task] = {}
next_task_id = 1


@app.get("/")
def read_root():
    return {"name": "Task API", "version": app.version}


@app.get("/tasks/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return list(tasks.values())


@app.get("/tasks/search")
def search_tasks(word: str = Query(min_length=1)):
    needle = word.casefold()
    return [
        task for task in tasks.values()
        if needle in task.title.casefold()
    ]


@app.get("/tasks/done")
def list_tasks_by_status(stat_complete: bool):
    return [
        task for task in tasks.values()
        if task.done is stat_complete
    ]


@app.get("/tasks/stats")
def task_stats():
    all_tasks = list(tasks.values())
    done_count = sum(task.done for task in all_tasks)
    return {
        "total": len(all_tasks),
        "done": done_count,
        "open": len(all_tasks) - done_count,
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global next_task_id
    task = Task(id=next_task_id, title=payload.title)
    tasks[task.id] = task
    next_task_id += 1
    return task


@app.put("/tasks/{task_id}")
def replace_task(task_id: int, payload: TaskCreate):
    existing = tasks.get(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = Task(id=task_id, title=payload.title, done=existing.done)
    tasks[task_id] = updated
    return updated


@app.patch("/tasks/{task_id}")
def update_task_status(task_id: int, payload: TaskStatusUpdate):
    existing = tasks.get(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = existing.model_copy(update={"done": payload.done})
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if tasks.pop(task_id, None) is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/tasks")
def delete_all_tasks():
    deleted_count = len(tasks)
    tasks.clear()
    return {"deleted": deleted_count}
```

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Return API information |
| `GET` | `/tasks/health` | Check API health |
| `GET` | `/tasks` | List tasks |
| `GET` | `/tasks/{task_id}` | Retrieve a task; return 404 if missing |
| `POST` | `/tasks` | Create a task |
| `PUT` | `/tasks/{task_id}` | Replace a task's title |
| `PATCH` | `/tasks/{task_id}` | Update a task's completion status |
| `DELETE` | `/tasks/{task_id}` | Delete one task |
| `DELETE` | `/tasks` | Delete all tasks |
| `GET` | `/tasks/search?word={word}` | Search titles, case-insensitively |
| `GET` | `/tasks/done?stat_complete={true\|false}` | Filter by completion status |
| `GET` | `/tasks/stats` | Get task counts |

### Request examples

Create a task with `POST /tasks`:

```json
{
  "title": "Prepare project documentation"
}
```

Set completion status with `PATCH /tasks/{task_id}`:

```json
{
  "done": true
}
```

## Generation details

- **Generator:** Copilot (AI assistant using Copilot SDK in VS Code)
- **Model version:** Not exposed in this session, so an exact model identifier cannot be stated reliably.
