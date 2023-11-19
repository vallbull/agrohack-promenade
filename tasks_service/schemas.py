from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
    is_available: Optional[bool | None] = None
    executor: Optional[str | None] = None
    status: Optional[str| None] = None

    class Config:
        orm_mode = True
