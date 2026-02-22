from typing import Any, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from hardy_optimods.tasks import calc_bmi, celery

app = FastAPI()


class Body(BaseModel):
    weight: float
    height: float


class TaskStatus(BaseModel):
    id: str
    status: Optional[str] = None
    result: Optional[Any] = None


@app.post("/bmi", response_model=TaskStatus, response_model_exclude_unset=True)
def calculate_bmi(body: Body) -> TaskStatus:
    task = calc_bmi.delay(weight=body.weight, height=body.height)
    return TaskStatus(id=task.id)


@app.get("/bmi/{task_id}", response_model=TaskStatus)
def check_status(task_id: str) -> TaskStatus:
    result = celery.AsyncResult(task_id)
    status = TaskStatus(id=task_id, status=result.status, result=result.result)
    return status
