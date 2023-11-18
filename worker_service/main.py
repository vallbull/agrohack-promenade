import json
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url='/worker/openapi.json', docs_url='/worker/docs', redoc_url='/worker/redoc')
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
    db.query(models.Worker).delete()
    user = models.Worker(
        name="Иван Иванов",
        speciality=["Посев"],
        lat=41.470956,
        long=52.767565,
        kpi=75,
    )
    db.add(user)
    user = models.Worker(
        name="Александр Петров",
        speciality=["Обработка почвы"],
        lat=41.471952,
        long=52.768468,
        kpi=100,
    )
    db.add(user)
    user = models.Worker(
        name="Екатерина Смирнова",
        speciality=["Защита растений"],
        lat=41.468291,
        long=52.769497,
        kpi=65,
    )
    db.add(user)
    user = models.Worker(
        name="Дмитрий Козлов",
        speciality=["Посев"],
        lat=41.477334,
        long=52.771938,
        kpi=38,
    )
    db.add(user)
    user = models.Worker(
        name="Ольга Морозова",
        speciality=["Обработка почвы"],
        lat=41.476101,
        long=52.772813,
        kpi=65,
    )
    db.add(user)
    db.commit()
    db.close()


@app.get("/worker")
def read_root():
    return "Promenade worker service"


@app.get("/worker/get_all", response_model=list[schemas.Worker])
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Worker).all()


@app.get("/worker/get_by_id/{id}", response_model=schemas.Worker)
def get_by_id(id: int, db: Session = Depends(get_db)):
    worker = db.query(models.Worker).filter(models.Worker.id == id).first()
    if not worker:
        raise HTTPException(status_code=404, detail=f"Worker with id {id} not found")
    return worker


@app.post("/worker/delete_all")
def delete_all(db: Session = Depends(get_db)):
    db.query(models.Worker).delete()
    db.commit()
    return {"status": "ok"}


@app.post("/worker/delete_by_id/{id}")
def delete_by_id(id: int, db: Session = Depends(get_db)):
    db.query(models.Worker).filter(models.Worker.id == id).delete()
    db.commit()
    return {"status": "ok"}


@app.put("/worker/update_by_id/{id}")
def update_by_id(id: int, worker: schemas.Worker, db: Session = Depends(get_db)):
    db.query(models.Worker).filter(models.Worker.id == id).update(worker.model_dump())
    db.commit()
    return {"status": "ok"}


@app.post("/worker/add")
def add(worker: schemas.Worker, db: Session = Depends(get_db)):
    db.add(models.Worker(**worker.model_dump()))
    db.commit()
    return {"status": "ok"}
