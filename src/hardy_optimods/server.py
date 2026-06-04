from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, select

from hardy_optimods.db import create_db_and_tables, engine
from hardy_optimods.tasks import calc_bmi, celery


class BmiJob(SQLModel, table=True):
    id: str = Field(primary_key=True)
    weight: float
    height: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


class Body(BaseModel):
    weight: float
    height: float


class TaskStatus(BaseModel):
    id: str
    weight: Optional[float] = None
    height: Optional[float] = None
    status: Optional[str] = None
    result: Optional[Any] = None
    created_at: Optional[datetime] = None


class DeletedTask(BaseModel):
    id: str
    deleted: bool


def build_task_status(job: BmiJob) -> TaskStatus:
    result = celery.AsyncResult(job.id)
    return TaskStatus(
        id=job.id,
        weight=job.weight,
        height=job.height,
        status=result.status,
        result=result.result,
        created_at=job.created_at,
    )


@app.post("/bmi", response_model=TaskStatus, response_model_exclude_unset=True)
def calculate_bmi(body: Body) -> TaskStatus:
    task = calc_bmi.delay(weight=body.weight, height=body.height)
    job = BmiJob(id=task.id, weight=body.weight, height=body.height)

    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)

    return TaskStatus(
        id=job.id, weight=job.weight, height=job.height, created_at=job.created_at
    )


@app.get("/bmi", response_model=list[TaskStatus])
def list_bmi_jobs() -> list[TaskStatus]:
    with Session(engine) as session:
        jobs = session.exec(select(BmiJob).order_by(BmiJob.created_at.desc())).all()
        return [build_task_status(job) for job in jobs]


@app.delete("/bmi/{task_id}", response_model=DeletedTask)
def delete_bmi_job(task_id: str) -> DeletedTask:
    with Session(engine) as session:
        job = session.get(BmiJob, task_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(job)
        session.commit()

    result = celery.AsyncResult(task_id)
    try:
        result.revoke(terminate=False)
        result.forget()
    except Exception:
        pass

    return DeletedTask(id=task_id, deleted=True)


@app.get("/bmi/{task_id}", response_model=TaskStatus)
def check_status(task_id: str) -> TaskStatus:
    with Session(engine) as session:
        job = session.get(BmiJob, task_id)

    if job is None:
        result = celery.AsyncResult(task_id)
        if result.status == "PENDING":
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskStatus(id=task_id, status=result.status, result=result.result)

    return build_task_status(job)
