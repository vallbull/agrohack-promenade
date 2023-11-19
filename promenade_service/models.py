from sqlalchemy import ARRAY, Column, DateTime, Float, Integer, String

from database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    speciality = Column(ARRAY(String))
    lat = Column(Float)
    long = Column(Float)
    kpi = Column(Integer, default=0)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    place_name = Column(String)
    type = Column(String)
    lat = Column(Float)
    long = Column(Float)
    duration = Column(Integer)
    priority = Column(String)
    processing_area = Column(Integer)
    start_time = Column(DateTime, nullable=True, default=None)
    finish_time = Column(DateTime, nullable=True, default=None)
    # is_available = Column(Boolean, default=True)
    executor = Column(String, default="Не назначен")
    status = Column(String, default="Создана")