from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Worker(BaseModel):
    id: Optional[int | None] = None
    name: str
    speciality: list[str]
    lat: float
    long: float
    kpi: Optional[int] = 0

    class Config:
        orm_mode = True


class Tasks(BaseModel):
    id: Optional[int | None] = None
    place_name: str
    type: str
    lat: float
    long: float
    duration: int
    priority: str
    processing_area: int
    start_time: Optional[datetime | None] = None
    finish_time: Optional[datetime | None] = None
    # is_available: Optional[bool | None] = None
    executor: Optional[str | None] = None
    status: Optional[str | None] = None
    description: Optional[str | None] = None

    class Config:
        orm_mode = True