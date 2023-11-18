from sqlalchemy import Column, Float, Integer, String

from database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    speciality = Column(String)
    lat = Column(Float)
    long = Column(Float)
    kpi = Column(Integer)
