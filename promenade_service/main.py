import json
from datetime import date, datetime, timedelta

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url='/promenade/openapi.json', docs_url='/promenade/docs', redoc_url='/promenade/redoc')
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
        speciality=["Посев", "Обработка почвы", "Защита растений"],
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
        speciality=["Посев", "Защита растений"],
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
    db.query(models.Tasks).delete()
    task = models.Tasks(
        place_name="Поле 4",
        type="Обработка почвы",
        long=52.780545,
        lat=41.489458,
        duration=60,
        priority="Низкий",
        processing_area=2,
        description="Техника: К-742 #1254 Агрегат: Catros 6TS2 #1 Глубина: 8-10 см Рабочая скорость, км/ч :12-14",

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
        description="Техника: RSM 3535 #7089 Агрегат: Horsh Pronto NT12 #1 Глубина: 2-3 см Рабочая скорость, км/ч :8-12",
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
        description="Техника: К-742 #1254 Агрегат: Catros 6TS2 #1 Глубина: 8-10 см Рабочая скорость, км/ч :12-14",
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
        description="Техника: Arion 640c #7912 Агрегат: UX5201 36 #3 Рабочая скорость, км/ч :8 Расход рабочего раствора, л/га:200",
    )
    db.add(task)
    task = models.Tasks(
        place_name="Поле 5",
        type="Посев",
        long=52.777981,
        lat=41.473423,
        duration=300,
        priority="Низкий",
        processing_area=2,
        description="Техника: RSM 3535 #7089 Агрегат: Horsh Pronto NT12 #1 Глубина: 2-3 см Рабочая скорость, км/ч :8-12",
    )
    db.add(task)
    db.commit()
    db.close()

@app.get("/")
def read_root():
    return "Welcome to promenade service"

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


@app.get("/tasks/get_by_worker_id/{worker_id}", response_model=list[schemas.Tasks])
def get_by_worker_id(worker_id: str, db: Session = Depends(get_db)):
    worker_name = db.query(models.Worker.name).filter(models.Worker.id == worker_id).first()
    return (
        db.query(models.Tasks)
        .filter(models.Tasks.executor == worker_name[0])
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
    if 'executor' in task and task['executor'] != "Не назначен":
        task['status'] = "Назначена"
    db.query(models.Tasks).filter(models.Tasks.id == id).update(task)
    db.commit()
    return {"status": "ok"}


@app.post("/tasks/add")
def add(task: schemas.Tasks, db: Session = Depends(get_db)):
    db.add(models.Tasks(**task.model_dump()))
    db.commit()
    return {"status": "ok"}


@app.post("/tasks/start/{id}")
def start(id: int, db: Session = Depends(get_db)):
    task = (
        db.query(models.Tasks)
        .filter(models.Tasks.id == id)
        .first()
    )
    start_time = datetime.now() + timedelta(hours=3)
    task.start_time = start_time
    task.status = "В процессе"
    db.add(task)
    db.commit()
    return {"status": "ok"}


@app.post("/tasks/finish/{id}")
def start(id: int, db: Session = Depends(get_db)):
    task = (
        db.query(models.Tasks)
        .filter(models.Tasks.id == id)
        .first()
    )
    finish_time = datetime.now() + timedelta(hours=3)
    task.finish_time = finish_time
    task.status = "Закончена"
    db.add(task)
    db.commit()
    return {"status": "ok"}


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
def update_by_id(id: int, worker= Body(), db: Session = Depends(get_db)):
    db.query(models.Worker).filter(models.Worker.id == id).update(worker)
    db.commit()
    return {"status": "ok"}


@app.post("/worker/add")
def add(worker: schemas.Worker, db: Session = Depends(get_db)):
    db.add(models.Worker(**worker.model_dump()))
    db.commit()
    return {"status": "ok"}


@app.post("/worker/get_worker_for_task")
def get_worker_for_task(spec = Body(), db: Session = Depends(get_db)):
    workers = db.query(models.Worker)
    rez = list()
    for worker in workers:
        worker_spec = worker.speciality
        worker_name = worker.name
        flag = True
        for el in spec:
            if el not in worker_spec:
                flag = False
                break
        if flag:
            rez.append(worker_name)
    return rez
