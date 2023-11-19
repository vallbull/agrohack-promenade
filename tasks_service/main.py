import json
from datetime import date

import sqlalchemy
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url="/tasks/openapi.json", docs_url="/tasks/docs", redoc_url="/tasks/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    db.query(models.Tasks).delete()
    task = models.Tasks(
        place_name="Поле 4",
        type="Обработка почвы",
        long=52.780545,
        lat=41.489458,
        duration=60,
        priority="Низкий",
        processing_area=2,
    )
    db.add(task)
    task = models.Tasks(
        place_name="Поле 1",
        type="Посев",
        long=52.78739,
        lat=41.49144,
        duration=120,
        priority="Высокий",
        processing_area=4,
    )
    db.add(task)
    task = models.Tasks(
        place_name="Поле 2",
        type="Обработка почвы",
        long=52.779057,
        lat=41.49461,
        duration=95,
        priority="Высокий",
        processing_area=3,
    )
    db.add(task)
    task = models.Tasks(
        place_name="Поле 3",
        type="Защита растений",
        long=52.772766,
        lat=41.47425,
        duration=300,
        priority="Средний",
        processing_area=10,
    )
    db.add(task)
    task = models.Tasks(
        place_name="Поле 4",
        type="Посев",
        long=52.777981,
        lat=41.473423,
        duration=300,
        priority="Низкий",
        processing_area=2,
    )
    db.add(task)
    db.commit()
    db.close()


@app.get("/tasks")
def read_root():
    return "Promenade tasks service"


@app.get("/tasks/get_all", response_model=list[schemas.Tasks])
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Tasks).all()


@app.get("/tasks/get_by_id/{id}", response_model=schemas.Tasks)
def get_by_id(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Tasks with id {id} not found")
    return task


def priority_to_num(priority):
    if priority == "Высокий":
        return 1
    elif priority == "Средний":
        return 2
    elif priority == "Низкий":
        return 3


@app.get("/tasks/get_by_worker_name/{worker_name}", response_model=list[schemas.Tasks])
def get_by_worker_name(worker_name: str, db: Session = Depends(get_db)):
    return (
        db.query(models.Tasks)
        .filter(models.Tasks.executor == worker_name)
        .order_by(models.Tasks.priority)
        .all()
    )


@app.post("/tasks/delete_all")
def delete_all(db: Session = Depends(get_db)):
    db.query(models.Tasks).delete()
    db.commit()
    return {"status": "ok"}


@app.post("/tasks/delete_by_id/{id}")
def delete_by_id(id: int, db: Session = Depends(get_db)):
    db.query(models.Tasks).filter(models.Tasks.id == id).delete()
    db.commit()
    return {"status": "ok"}


@app.put("/tasks/update_by_id/{id}")
def update_by_id(id: int, task=Body(), db: Session = Depends(get_db)):
    db.query(models.Tasks).filter(models.Tasks.id == id).update(task)
    db.commit()
    return {"status": "ok"}


@app.post("/tasks/add")
def add(task: schemas.Tasks, db: Session = Depends(get_db)):
    db.add(models.Tasks(**task.model_dump()))
    db.commit()
    return {"status": "ok"}
